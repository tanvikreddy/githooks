#!/usr/bin/env pwsh
# Exit immediately if a command fails
$ErrorActionPreference = "Stop"

Write-Host "Checking for ESLint..."

# Check if ESLint is installed
$eslintPath = Get-Command eslint -ErrorAction SilentlyContinue

if (-not $eslintPath) {
    Write-Host "ESLint could not be found, attempting to use project's ESLint..."
    if (Test-Path "./node_modules/.bin/eslint.cmd") {
        $ESLINT = "./node_modules/.bin/eslint.cmd"
    } else {
        Write-Host "Error: ESLint is not installed. Please install it globally or in your project."
        exit 1
    }
} else {
    $ESLINT = "eslint"
}

# Get staged TypeScript files
$files = git diff --cached --name-only --diff-filter=ACMR | Where-Object { $_ -match '\.tsx?$' }

if (-not $files) {
    Write-Host "No TypeScript files staged for commit."
    exit 0
}

Write-Host "Running ESLint on staged TypeScript files..."

# Run ESLint with auto-fix on each file
foreach ($file in $files) {
    & $ESLINT --fix $file
}

# Add fixed files back to staging
foreach ($file in $files) {
    git add $file
}

Write-Host "ESLint check passed!"
exit 0
