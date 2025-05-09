# GitHub Hooks

A collection of pre-commit hooks for validating and linting code in repositories.

## Prerequisites

Before using these hooks, ensure you have:

1. **Python** installed and available in your PATH
2. **pre-commit** package installed (`pip install pre-commit` or `python -m pip install pre-commit`)

You can automate the setup with the following PowerShell/CMD script in your init.cmd:

```batch
echo Setting up pre-commit hooks..
==========================================================
if [%LocalBuild%] == [true] (
	echo Checking if Python is installed...
	python --version >nul 2>&1
	if errorlevel 1 (
		echo ERROR: Python is not installed or not in PATH
		echo Please install Python and try again.
		echo Skipping pre-commit setup.
	) else (
		echo Python is installed. Checking if pre-commit is installed...
		python -m pip show pre-commit >nul 2>&1
		if errorlevel 1 (
			echo Installing pre-commit...
			python -m pip install pre-commit
		) else (
			echo pre-commit is already installed.
		)
		
		echo Creating git hooks directory if it doesn't exist
		if not exist %WSRoot%\.git\hooks mkdir %WSRoot%\.git\hooks
		
		echo Installing pre-commit hooks...
		python -m pre_commit install --allow-missing-config
		echo Pre-commit hooks setup complete.
	)
)
==========================================================
```

## Installation

1. Create a `.pre-commit-config.yaml` file in the root of your repository.

2. Add this repository to your pre-commit configuration:

```yaml
repos:
  - repo: https://github.com/tanvikreddy/githooks
    rev: 8452d53  # Use the latest commit hash or tag
    hooks:
      # Add hooks you want to use here
      # See "Available Hooks" section below
```

3. If the init.cmd script didn't already automate this step, run:
   ```powershell
   pre-commit install
   ```
   This sets up the git hook scripts in your repository.

4. Now pre-commit will run automatically on `git commit`.

## Available Hooks

### Security Hooks

#### `check-customapi-privilege`

Validates that all Custom API XML files have the required security privilege configuration.

**What it does:**
- Scans all added/modified `customapi.xml` files in your commits
- Verifies that each file contains the required `<executeprivilegename>prv*</executeprivilegename>` tag
- Fails the commit if any files are missing this security configuration

**Configuration:**

Add this to your `.pre-commit-config.yaml` file:

```yaml
repos:
  - repo: https://github.com/tanvikreddy/githooks
    rev: 8452d53  # Use the latest commit hash or tag
    hooks:
      - id: check-customapi-privilege
```

**Advanced configuration:**

You can exclude specific files or patterns from being checked:

```yaml
- repo: https://github.com/tanvikreddy/githooks
  rev: 8452d53
  hooks:
    - id: check-customapi-privilege
      exclude: (msdyn_SalesAgents_IsOwnerAssigned|another_path)/customapi\.xml$
```

The `exclude` parameter uses regular expression patterns to match against file paths:
- `(pattern1|pattern2)` - matches either pattern1 or pattern2
- Use `|` to separate multiple patterns
- Escape dots with a backslash: `\.`

**Common exclude patterns:**

```yaml
# Exclude specific files
exclude: customapis/specific_file/customapi\.xml$

# Exclude files under a specific directory
exclude: customapis/legacy_apis/.*$

# Exclude multiple file patterns
exclude: (pattern1|pattern2|pattern3)/customapi\.xml$
```

### Planned Hooks (Coming Soon)

#### Code Quality Hooks

- **`check-code-formatting`** - Ensure code follows formatting standards
- **`check-typescript-imports`** - Validate import ordering and structure
- **`check-web-resources`** - Verify web resources follow organization standards

#### Security Hooks

- **`check-plugin-privilege`** - Validate plugin step security configurations
- **`check-web-resource-privilege`** - Verify web resource security settings
- **`check-sensitive-data`** - Scan for accidentally committed sensitive data

#### Performance Hooks

- **`check-query-performance`** - Identify potentially slow queries
- **`check-js-bundle-size`** - Monitor and limit JavaScript bundle sizes

## Complete Configuration Example

Here's a complete example of a `.pre-commit-config.yaml` file with multiple hooks:

```yaml
# pre-commit configuration
# Save this file as .pre-commit-config.yaml in your repository root
repos:
  # Standard pre-commit hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      
  # Custom hooks from tanvikreddy/githooks
  - repo: https://github.com/tanvikreddy/githooks
    rev: 8452d53
    hooks:
      - id: check-customapi-privilege
        exclude: (legacy-apis|test-apis)/customapi\.xml$
```

## Contributing

1. Clone this repository
2. Create a new branch for your feature
3. Create your hook in the `pre_commit_hooks` directory
4. Add your hook to `.pre-commit-hooks.yaml`
5. Add documentation to this README
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.