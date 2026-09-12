#!/usr/bin/env node
// Copy this package's skills (and slash commands) into an agent host's skills directory.
// No dependencies: Node 18+ only.
//
//   npx @targetbay/reviews-skills            -> ./.claude/skills
//   npx @targetbay/reviews-skills --global   -> ~/.claude/skills
//   npx @targetbay/reviews-skills --dest DIR -> DIR

import { cp, mkdir, readdir, access } from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PACKAGE_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");

const args = process.argv.slice(2);

if (args.includes("--help") || args.includes("-h")) {
  console.log(`targetbay-reviews-skills — install TargetBay Reviews Skills

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
  written++;
}

console.log(`${written} skill${written === 1 ? "" : "s"} installed into ${dest}`);

if (skipped) {
  console.log(`${skipped} already present, left alone — rerun with --force to overwrite`);
}

// Slash commands are a Claude Code convention; only install them alongside a .claude tree.
if (dest.includes(`${join(".claude", "skills")}`)) {
  const commands = join(dirname(dest), "commands");
  await cp(join(PACKAGE_ROOT, "commands"), commands, { recursive: true, force });
  console.log(`slash commands installed into ${commands}`);
}

console.log("\nThese skills plan only. They need the TargetBay Reviews MCP to read store data,");
console.log("and they never send or activate anything without your explicit approval.");
