# Substack Auto

Substack Auto is an automation tool for Substack newsletter platform operations. This repository contains the source code and tooling for automating various Substack-related tasks.

**Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Environment Setup
The development environment includes:
- **Python 3.12.3** - Primary development language
- **Node.js v20.19.4** - For JavaScript tooling and dependencies  
- **npm 10.8.2** - Package manager for Node.js dependencies
- **pip 24.0** - Python package manager
- **Git 2.51.0** - Version control
- **curl 8.5.0** - HTTP client for API testing

### Initial Repository Setup
- Clone the repository: `git clone https://github.com/becominggiantcollective/substack_auto.git`
- Navigate to repository: `cd substack_auto`
- Check repository status: `git status`
- View current branch: `git branch -a`

### Development Workflow
Since this is a minimal repository, most development commands will be established as the project grows. However, here are the standard practices:

#### Python Development (when Python code is added)
- Create virtual environment: `python3 -m venv venv`
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt` (when requirements.txt exists)
- Install development dependencies: `pip install -r requirements-dev.txt` (when dev requirements exist)
- Run tests: `python -m pytest` (when tests are added)
- Run linting: `python -m flake8` or `python -m pylint` (when configured)
- Format code: `python -m black .` (when configured)

#### Node.js Development (when JavaScript/TypeScript code is added)
- Install dependencies: `npm install` (when package.json exists)
- Run tests: `npm test` (when test scripts are configured)
- Run linting: `npm run lint` (when lint scripts are configured)
- Format code: `npm run format` (when format scripts are configured)
- Build project: `npm run build` (when build scripts are configured)

### Validation Procedures
- **ALWAYS** run the full test suite after making changes: Set timeout to 30+ minutes. NEVER CANCEL.
- **ALWAYS** run linting before committing: `git status && git diff` to review changes
- **ALWAYS** validate that basic commands work:
  - `python3 --version` should return Python 3.12.3
  - `node --version` should return v20.19.4
  - `git status` should show repository state
- When testing API interactions in full environments, use: `curl -I https://substack.com` to verify connectivity
- **Note**: In sandboxed environments, external connectivity may be limited

### Build and Test Timing Expectations
- **CRITICAL**: Since this is a new repository, build and test times will be established as code is added
- **NEVER CANCEL** any build or test commands - wait for completion
- Initial setup commands typically take under 5 minutes
- When package installations are added, expect:
  - Python `pip install` operations: 2-10 minutes depending on packages
  - Node.js `npm install` operations: 3-15 minutes depending on packages
  - Set timeouts to at least 30 minutes for any installation commands

## Repository Structure and Navigation

### Current Repository Contents
```
/home/runner/work/substack_auto/substack_auto/
├── .git/                    # Git version control
├── .github/                 # GitHub configuration and workflows
│   └── copilot-instructions.md  # This file
└── README.md               # Project overview
```

### Expected Future Structure (as project develops)
```
/home/runner/work/substack_auto/substack_auto/
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies (if applicable)
├── .gitignore             # Git ignore rules
├── .github/               # GitHub workflows and configuration
└── README.md              # Project documentation
```

## Common Development Tasks

### Starting a New Feature
1. Create a new branch: `git checkout -b feature/feature-name`
2. Make your changes following the project structure
3. Test your changes thoroughly
4. Commit with descriptive messages: `git commit -m "feat: add new feature"`
5. Push branch: `git push origin feature/feature-name`
6. Create pull request via GitHub UI

### Working with Substack APIs (when implemented)
- Substack API documentation: https://substack.com/
- Test API connectivity: `curl -I https://substack.com`
- Always validate API responses and handle errors gracefully
- Use environment variables for API keys and sensitive data

### Debugging and Troubleshooting
- Check Python environment: `python3 --version && pip --version`
- Check Node.js environment: `node --version && npm --version`
- View repository status: `git status && git log --oneline -5`
- Check for uncommitted changes: `git diff`

## Validation Scenarios
After making any changes, always perform these validation steps:

### Basic Environment Validation
1. Verify Python works: `python3 -c "print('Python environment OK')"`
2. Verify Node.js works: `node -e "console.log('Node.js environment OK')"`
3. Verify Git works: `git status`
4. Check repository integrity: `git log --oneline -3`

### Future Code Validation (when code is added)
- **Python projects**: Run `python -m pytest -v` for comprehensive testing
- **Node.js projects**: Run `npm test` for test suite execution
- **API integration**: Test with sample API calls using curl or Python requests
- **CLI tools**: Execute `--help` commands and test basic functionality

### Manual Testing Requirements
- When Substack integration is added, manually test:
  1. Authentication flow with Substack
  2. Basic newsletter operations (list, create, update)
  3. Error handling for invalid credentials
  4. Rate limiting compliance

## Critical Development Notes
- **NEVER CANCEL** long-running operations - Substack API calls may take time
- **ALWAYS** use environment variables for sensitive data (API keys, tokens)
- **ALWAYS** validate API responses before processing
- **ALWAYS** implement proper error handling for network operations
- **ALWAYS** test with sample data before using real newsletter content

## CI/CD Considerations (for future implementation)
- GitHub Actions workflows should be placed in `.github/workflows/`
- Include steps for: dependency installation, testing, linting, security scanning
- Set appropriate timeouts (60+ minutes) for comprehensive test suites
- Include manual testing steps in PR templates

## Quick Reference Commands
```bash
# Environment check
python3 --version && node --version && git --version

# Repository status
git status && git branch -a

# Basic connectivity test (when external access available)
curl -I https://substack.com || echo "External connectivity limited in sandboxed environments"

# Clean repository state
git clean -fd  # Use with caution - removes untracked files
```

This repository is in early development. As code is added, update these instructions with specific build, test, and deployment procedures. Always validate that every command works before updating the instructions.