#!/usr/bin/env node
// Copy this package's skills (and slash commands) into an agent host's skills directory.
// No dependencies: Node 18+ only.
//
//   npx @targetbay/email-sms-skills            -> ./.claude/skills
//   npx @targetbay/email-sms-skills --global   -> ~/.claude/skills
//   npx @targetbay/email-sms-skills --dest DIR -> DIR

import { cp, mkdir, readdir, access, readFile, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PACKAGE_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const PLUGIN = "targetbay-email-sms";
const VERSION = (await readFile(join(PACKAGE_ROOT, "VERSION"), "utf8")).trim();

const args = process.argv.slice(2);

if (args.includes("--help") || args.includes("-h")) {
  console.log(`targetbay-email-sms-skills — install TargetBay Email & SMS Marketing Skills

  --global        install into ~/.claude/skills (default: ./.claude/skills)
  --dest <dir>    install into <dir> instead
  --force         overwrite skills that are already present
  --help          show this message`);
  process.exit(0);
}

function destination() {
  const flag = args.indexOf("--dest");

  if (flag !== -1) {
    if (!args[flag + 1]) {
      console.error("--dest needs a directory");
      process.exit(1);
    }

    return resolve(args[flag + 1]);
  }

  if (args.includes("--global")) {
    return join(homedir(), ".claude", "skills");
  }

  return resolve(".claude", "skills");
}

async function exists(path) {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
}

// A skill is authored inside the plugin tree, so it cites `../../rules/...`, `../../knowledge/...`
// and the schemas by relative path. Installing flattens `skills/` into the destination, which puts
// those targets out of reach — the citation would resolve to nothing on disk. Rewrite them to the
// full URL, which is what this repository requires of any reference that leaves its own directory.
// Links to sibling skills (`../other-skill/SKILL.md`) still resolve after flattening and are left
// alone.
//
// Prefer the release tag, so a citation matches the skills that were installed. A release is cut by
// pushing that tag, so it exists for every published package and for a release tarball. It does not
// exist in a clone whose VERSION has moved past the newest tag, and pinning to it there rewrites
// every citation to a 404 — so a checkout falls back to the branch.
const REPO = "https://github.com/targetbay360/targetbay-agent-skills";
const REF = (await exists(resolve(PACKAGE_ROOT, "..", "..", ".git")))
  ? "main"
  : `${PLUGIN}@${VERSION}`;
const REPO_BLOB = `${REPO}/blob/${REF}/plugins/${PLUGIN}`;

async function rewriteEscapingLinks(dir) {
  const entries = await readdir(dir, { withFileTypes: true });

  for (const entry of entries) {
    const path = join(dir, entry.name);

    if (entry.isDirectory()) {
      await rewriteEscapingLinks(path);
      continue;
    }

    if (!entry.name.endsWith(".md")) {
      continue;
    }

    const before = await readFile(path, "utf8");
    const after = before
      .replace(/\[\.\.\/\.\.\/([^\]]+)\]\(\.\.\/\.\.\/([^)\s]+)\)/g, `[$1](${REPO_BLOB}/$2)`)
      .replace(/\]\(\.\.\/\.\.\/([^)\s]+)\)/g, `](${REPO_BLOB}/$1)`);

    if (after !== before) {
      await writeFile(path, after);
    }
  }
}

const force = args.includes("--force");
const dest = destination();
const skills = (await readdir(join(PACKAGE_ROOT, "skills"), { withFileTypes: true }))
  .filter((entry) => entry.isDirectory())
  .map((entry) => entry.name);

await mkdir(dest, { recursive: true });

let written = 0;
let skipped = 0;

for (const skill of skills) {
  const target = join(dest, skill);

  if (!force && (await exists(target))) {
    skipped++;
    continue;
  }

  await cp(join(PACKAGE_ROOT, "skills", skill), target, { recursive: true });
  await rewriteEscapingLinks(target);
  written++;
}

console.log(`${written} skill${written === 1 ? "" : "s"} installed into ${dest}`);

if (skipped) {
  console.log(`${skipped} already present, left alone — rerun with --force to overwrite`);
}

// Slash commands are a Claude Code convention; only install them alongside a .claude tree.
if (dest.includes(`${join(".claude", "skills")}`) && (await exists(join(PACKAGE_ROOT, "commands")))) {
  const commands = join(dirname(dest), "commands");
  await cp(join(PACKAGE_ROOT, "commands"), commands, { recursive: true, force });
  console.log(`slash commands installed into ${commands}`);
}

console.log("\nThese skills plan only. They need the TargetBay Email & SMS MCP to read store data,");
console.log("and they never send or activate anything without your explicit approval.");
