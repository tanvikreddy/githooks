#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Get the git hooks directory
function getGitHooksDir() {
  try {
    // Get the git directory from the current working directory
    const gitDir = execSync('git rev-parse --git-dir', { encoding: 'utf-8' }).trim();
    return path.resolve(process.cwd(), gitDir, 'hooks');
  } catch (error) {
    console.error('Error: Not a git repository or git is not installed.');
    process.exit(1);
  }
}

// Install a hook
function installHook(hookName, scriptPath) {
  const hooksDir = getGitHooksDir();
  const hookPath = path.join(hooksDir, hookName);
  
  // Create hooks directory if it doesn't exist
  if (!fs.existsSync(hooksDir)) {
    fs.mkdirSync(hooksDir, { recursive: true });
  }
  
  // Create the hook script
  const hookContent = `#!/bin/sh
# Installed by githooks
node ${scriptPath} "$@"
`;

  fs.writeFileSync(hookPath, hookContent);
  fs.chmodSync(hookPath, '0755');
  
  console.log(`✅ Installed ${hookName} hook`);
}

// Main execution
console.log('📦 Installing git hooks...');

// Install pre-commit hook
const preCommitPath = path.resolve(__dirname, 'hooks', 'pre-commit.js');
installHook('pre-commit', preCommitPath);

console.log('\n🎉 Git hooks installed successfully!');
console.log('Make sure you have ESLint installed in your project:');
console.log('npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin');
