# GitHooks

A collection of reusable git hooks for TypeScript projects.

## Available Hooks

- **pre-commit**: Runs ESLint on staged TypeScript files and automatically fixes issues when possible.
- **check-customapi-privilege**: Validates that customapi.xml files have the required privilege tags for security.

## Usage

You can use these git hooks in your project in multiple ways:

### Option 1: Using with pre-commit framework

Add the following to your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/yourusername/githooks
    rev: v1.0.0  # Replace with the latest version
    hooks:
      - id: eslint
      - id: check-customapi-privilege
        files: customapi\.xml$
        exclude: |
          (?x)^(
              customapi/myallowedapi1\.xml|
              customapi/myallowedapi2\.xml
          )$
```

### Option 2: Manual Installation

1. Install the package:

```bash
npm install --save-dev githooks
```

2. Create a pre-commit hook in your `.git/hooks/pre-commit` file:

```bash
#!/bin/sh
# Run ESLint pre-commit hook
node node_modules/githooks/hooks/pre-commit.js
```

3. Make the hook executable:

```bash
chmod +x .git/hooks/pre-commit
```

### Option 3: Using Husky

1. Install husky:

```bash
npm install --save-dev husky
```

2. Add the following to your package.json:

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "node node_modules/githooks/hooks/pre-commit.js"
    }
  }
}
```

## Configuration

The ESLint pre-commit hook respects your project's ESLint configuration. Make sure you have one of the following files in your project:

- `.eslintrc.js`
- `.eslintrc.json`
- `.eslintrc.yml`
- `.eslintrc.yaml`
- `.eslintrc`
- `eslintConfig` field in your `package.json`

## Requirements

- Node.js 14 or higher
- ESLint installed in your project
- TypeScript (for TypeScript projects)

## License

MIT
