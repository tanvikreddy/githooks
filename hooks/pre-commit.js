#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Get all staged TypeScript files
function getStagedTypeScriptFiles() {
  try {
    const output = execSync('git diff --cached --name-only --diff-filter=ACMR "*.ts" "*.tsx"', { encoding: 'utf-8' });
    return output.split('\n').filter(Boolean);
  } catch (error) {
    console.error('Error getting staged TypeScript files:', error.message);
    return [];
  }
}

// Run ESLint on staged files
function runEslintOnFiles(files) {
  if (files.length === 0) {
    console.log('No TypeScript files to lint.');
    return true;
  }

  try {
    // Check if project has ESLint config
    const eslintConfigFiles = [
      '.eslintrc.js',
      '.eslintrc.json',
      '.eslintrc.yml',
      '.eslintrc.yaml',
      '.eslintrc',
      'package.json' // For eslintConfig field
    ];

    let hasEslintConfig = false;
    for (const configFile of eslintConfigFiles) {
      if (fs.existsSync(path.resolve(process.cwd(), configFile))) {
        hasEslintConfig = true;
        break;
      }
    }

    if (!hasEslintConfig) {
      console.warn('\x1b[33mNo ESLint configuration found. Skipping lint.\x1b[0m');
      console.warn('\x1b[33mCreate an ESLint configuration file to enable linting.\x1b[0m');
      return true;
    }

    console.log('\nLinting TypeScript files:');
    files.forEach(file => console.log(`  - ${file}`));

    // Run ESLint with auto-fix option
    const eslintBin = path.resolve(process.cwd(), 'node_modules', '.bin', 'eslint');
    const eslintCmd = fs.existsSync(eslintBin) ? eslintBin : 'eslint';
    
    execSync(`${eslintCmd} --fix ${files.join(' ')}`, { stdio: 'inherit' });
    
    // If we reach here without error, add any fixes back to staging
    execSync(`git add ${files.join(' ')}`);
    
    console.log('\x1b[32mESLint passed successfully!\x1b[0m');
    return true;
  } catch (error) {
    console.error('\x1b[31mESLint found issues that need to be fixed:\x1b[0m');
    return false;
  }
}

// Main execution
try {
  const stagedFiles = getStagedTypeScriptFiles();
  const lintSuccess = runEslintOnFiles(stagedFiles);
  
  if (!lintSuccess) {
    console.error('\x1b[31mCommit aborted due to linting errors. Fix the issues and try again.\x1b[0m');
    process.exit(1);
  }
} catch (error) {
  console.error('\x1b[31mAn error occurred during pre-commit hook:\x1b[0m', error.message);
  process.exit(1);
}
