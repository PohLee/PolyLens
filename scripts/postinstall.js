#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const isWindows = process.platform === 'win32';

const agents = {
  opencode: isWindows
    ? path.join(os.homedir(), '.config', 'opencode', 'skills', 'polylens')
    : path.join(os.homedir(), '.config', 'opencode', 'skills', 'polylens'),
  'claude-code': isWindows
    ? path.join(os.homedir(), '.claude', 'skills', 'polylens')
    : path.join(os.homedir(), '.claude', 'skills', 'polylens'),
  codex: isWindows
    ? path.join(os.homedir(), '.codex', 'skills', 'polylens')
    : path.join(os.homedir(), '.codex', 'skills', 'polylens'),
  roocode: isWindows
    ? path.join(os.homedir(), '.roo', 'skills', 'polylens')
    : path.join(os.homedir(), '.roo', 'skills', 'polylens'),
};

const skillsDir = path.join(__dirname, '..', 'skills');

function symlink(target, link) {
  const parent = path.dirname(link);
  if (!fs.existsSync(parent)) {
    fs.mkdirSync(parent, { recursive: true });
  }
  if (fs.existsSync(link) || fs.lstatSync(link)?.isSymbolicLink()) {
    fs.rmSync(link, { recursive: true, force: true });
  }
  if (isWindows) {
    // Windows: use junction for directories
    fs.symlinkSync(target, link, 'junction');
  } else {
    fs.symlinkSync(target, link);
  }
}

console.log('PolyLens: Setting up skill symlinks...\n');

let linked = 0;
for (const [agent, target] of Object.entries(agents)) {
  try {
    symlink(skillsDir, target);
    console.log(`  ✅ ${agent} → ${target}`);
    linked++;
  } catch (err) {
    console.log(`  ⚠️  ${agent} — could not link: ${err.message}`);
  }
}

console.log(`\nPolyLens: Linked ${linked}/${Object.keys(agents).length} agents.`);
console.log('Verify by asking your agent: "What skills do you have available?"');
