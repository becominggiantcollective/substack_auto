# Substack Auto - Copilot Instructions

Substack Auto is an AI-powered content generation system for Substack newsletter automation. This repository contains a complete Python application that uses OpenAI's GPT-4 and DALL-E 3 to generate blog posts, images, and videos, with automated publishing to Substack.

**Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Environment Setup
The development environment includes:
- **Python 3.12.3** - Primary development language
- **pip 24.0** - Python package manager
- **Git 2.51.0** - Version control
- **unittest** - Testing framework (part of Python standard library)

### Initial Repository Setup
```bash
git clone https://github.com/becominggiantcollective/substack_auto.git
cd substack_auto
pip install -r requirements.txt
```

### Development Workflow

#### Installing Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

Dependencies include:
- `openai>=1.3.0` - OpenAI API client for GPT-4 and DALL-E 3
- `requests>=2.31.0` - HTTP library
- `python-dotenv>=1.0.0` - Environment variable management
- `Pillow>=10.0.0` - Image processing
- `moviepy>=1.0.3` - Video generation
- `schedule>=1.2.0` - Task scheduling
- `pydantic>=2.0.0` - Data validation
- `pydantic-settings>=2.0.0` - Settings management
- `tenacity>=9.0.0` - Retry logic

#### Running Tests
Tests use Python's built-in `unittest` framework. **IMPORTANT**: Tests require environment variables to be set.

```bash
# Run all tests with environment variables
OPENAI_API_KEY=test SUBSTACK_EMAIL=test@test.com SUBSTACK_PASSWORD=test SUBSTACK_PUBLICATION=test python3 -m unittest discover -s tests -v

# Or run specific test file
OPENAI_API_KEY=test SUBSTACK_EMAIL=test@test.com SUBSTACK_PASSWORD=test SUBSTACK_PUBLICATION=test python3 -m unittest tests.test_substack_auto -v
```

**Test Execution Notes:**
- Tests take approximately 1-2 seconds to run
- All 28 tests should pass when dependencies are installed
- Environment variables are required even for tests (they use mocking)
- Never cancel test runs

#### Running the Application

The application provides a CLI interface with multiple commands:

```bash
# Run setup wizard (creates .env file)
python3 cli.py setup

# Run interactive demonstration
python3 cli.py demo

# Generate a single post
python3 cli.py generate

# Start automated scheduler
python3 cli.py schedule

# Show system status
python3 cli.py status
```

#### Configuration

The application uses environment variables configured in a `.env` file:

```bash
# Copy template
cp .env.example .env

# Edit with your credentials
# Required: OPENAI_API_KEY, SUBSTACK_EMAIL, SUBSTACK_PASSWORD, SUBSTACK_PUBLICATION
# Optional: MAX_POSTS_PER_DAY, CONTENT_TOPICS, IMAGE_STYLE, CONTENT_TONE, etc.
```

### Validation Procedures
- **ALWAYS** run the full test suite after making changes: Set timeout to 5+ minutes
- **NEVER CANCEL** any build or test commands - wait for completion
- **ALWAYS** validate that basic commands work:
  - `python3 --version` should return Python 3.12.3
  - `python3 cli.py --help` should show CLI options
  - Tests should run with environment variables set
- **ALWAYS** review git changes before committing: `git status && git diff`

### Build and Test Timing Expectations
- **Dependency installation**: 2-5 minutes (one-time setup)
- **Test execution**: 1-2 seconds for all 28 tests
- **Code generation**: Varies based on OpenAI API response times (typically 5-30 seconds per generation)
- **NEVER CANCEL** any operations - always wait for completion

## Repository Structure and Navigation

### Current Repository Contents
```
/home/runner/work/substack_auto/substack_auto/
├── .git/                           # Git version control
├── .github/                        # GitHub configuration and workflows
│   └── copilot-instructions.md     # This file
├── src/                            # Source code
│   ├── __init__.py
│   ├── main.py                     # ContentOrchestrator - main workflow coordinator
│   ├── agents/                     # AI agents
│   │   ├── __init__.py
│   │   └── fact_checker_agent.py   # Fact-checking and SEO validation
│   ├── config/                     # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py             # Pydantic settings with environment variables
│   ├── content_generators/         # Content generation modules
│   │   ├── __init__.py
│   │   ├── text_generator.py       # GPT-4 blog post generation
│   │   ├── image_generator.py      # DALL-E 3 image generation
│   │   └── video_generator.py      # MoviePy slideshow video creation
│   └── publishers/                 # Publishing integrations
│       ├── __init__.py
│       └── substack_publisher.py   # Substack API integration
├── tests/                          # Test suite
│   ├── test_substack_auto.py       # Main test suite (settings, generators, publisher)
│   └── test_fact_checker_agent.py  # Fact-checker agent tests
├── docs/                           # Documentation
│   └── fact_checker_agent.md       # Fact-checker documentation
├── cli.py                          # Command-line interface
├── demo.py                         # Interactive demonstration
├── demo_fact_checker.py            # Fact-checker demonstration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore rules
├── IMPLEMENTATION_SUMMARY.md       # Fact-checker implementation notes
└── README.md                       # Project documentation
```

## Module Overview

### Core Modules

#### `src/main.py` - ContentOrchestrator
The main workflow coordinator that orchestrates content generation, validation, and publishing:
- `generate_complete_content()` - Generates topic, blog post, image, video, and fact-check report
- `publish_content()` - Publishes content to Substack
- Integrates all generators, agents, and publishers

#### `src/agents/fact_checker_agent.py` - FactCheckerAgent
AI-powered fact-checking and SEO validation:
- Extracts factual claims from content
- Validates claims with confidence scores (0.0-1.0)
- Assesses SEO impact and featured snippet potential
- Generates detailed reports with recommendations
- See `docs/fact_checker_agent.md` for full API documentation

#### `src/config/settings.py` - Settings
Pydantic-based configuration management:
- Loads environment variables from `.env` file
- Validates required settings (API keys, credentials)
- Provides typed access to all configuration
- Properties for parsing comma-separated values (topics_list, image_styles_list)

#### `src/content_generators/text_generator.py` - TextGenerator
GPT-4 powered blog post generation:
- `generate_topic()` - Creates engaging blog topics
- `generate_blog_post()` - Generates full blog posts with introduction, sections, and conclusion
- Respects CONTENT_TONE, TARGET_AUDIENCE, CONTENT_STYLE, and CUSTOM_INSTRUCTIONS settings
- Uses retry logic with exponential backoff

#### `src/content_generators/image_generator.py` - ImageGenerator
DALL-E 3 image generation:
- `generate_image()` - Creates featured images based on blog topic
- Supports multiple image styles (digital art, modern, professional)
- Downloads and saves generated images locally

#### `src/content_generators/video_generator.py` - VideoGenerator
MoviePy-based slideshow video creation:
- `generate_video()` - Creates videos from blog content and images
- `create_title_slide()` - Generates title slide
- `create_content_slides()` - Creates content slides with key points
- Configurable video duration

#### `src/publishers/substack_publisher.py` - SubstackPublisher
Substack platform integration:
- `authenticate()` - Handles Substack login
- `create_draft_post()` - Creates draft posts
- `publish_post()` - Publishes posts immediately
- `validate_content()` - Ensures content meets requirements

## Common Development Tasks

### Adding a New Content Generator
1. Create new file in `src/content_generators/`
2. Implement generation methods with retry logic
3. Add integration to `ContentOrchestrator` in `src/main.py`
4. Create tests in `tests/test_substack_auto.py`
5. Update documentation in README.md

### Adding a New Agent
1. Create new file in `src/agents/`
2. Implement processing methods with error handling
3. Add integration to `ContentOrchestrator`
4. Create comprehensive tests in `tests/test_<agent_name>.py`
5. Document API in `docs/<agent_name>.md`

### Modifying Settings
1. Update `src/config/settings.py` with new field
2. Add default value and environment variable name
3. Update `.env.example` with new variable
4. Document in README.md Configuration section
5. Add tests in `tests/test_substack_auto.py`

### Working with OpenAI APIs
- All OpenAI calls should use retry logic (tenacity library)
- Handle API errors gracefully with fallback mechanisms
- Use environment variable `OPENAI_API_KEY` for authentication
- Log all API calls for debugging
- Mock OpenAI responses in tests

### Working with Substack APIs
- Substack integration uses custom HTTP requests (requests library)
- Always validate content before publishing
- Handle authentication errors gracefully
- Use environment variables for credentials
- Test with Substack's sandbox/draft features when available

### Debugging and Troubleshooting
```bash
# Check Python environment
python3 --version && pip --version

# View repository status
git status && git log --oneline -5

# Check for uncommitted changes
git diff

# Run specific test
OPENAI_API_KEY=test SUBSTACK_EMAIL=test@test.com SUBSTACK_PASSWORD=test SUBSTACK_PUBLICATION=test python3 -m unittest tests.test_substack_auto.TestTextGenerator -v

# View logs (when application is running)
tail -f substack_auto.log
```

## Validation Scenarios

After making any changes, always perform these validation steps:

### 1. Basic Environment Validation
```bash
# Verify Python works
python3 -c "print('Python environment OK')"

# Verify Git works
git status

# Check repository integrity
git log --oneline -3
```

### 2. Code Validation
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
OPENAI_API_KEY=test SUBSTACK_EMAIL=test@test.com SUBSTACK_PASSWORD=test SUBSTACK_PUBLICATION=test python3 -m unittest discover -s tests -v

# Verify CLI works
python3 cli.py --help
```

### 3. Manual Testing
When making significant changes, test manually:

```bash
# Set up environment (if not already done)
cp .env.example .env
# Edit .env with your credentials

# Run demonstration
python3 cli.py demo

# Run fact-checker demo
python3 demo_fact_checker.py

# Generate a single post
python3 cli.py generate
```

### 4. Integration Testing
- Test the complete workflow: topic generation → blog post → image → video → fact-check
- Verify draft post creation in Substack (without publishing)
- Test error handling with invalid credentials or API keys
- Verify all output files are created in `generated_content/`

## Critical Development Notes

### API Usage and Rate Limits
- **OpenAI API**: Has rate limits - implement exponential backoff
- **Substack API**: May have undocumented rate limits - be conservative
- **NEVER CANCEL** long-running operations - OpenAI API calls may take 10-30 seconds
- Always implement retry logic for external API calls

### Security Best Practices
- **ALWAYS** use environment variables for sensitive data (API keys, passwords)
- **NEVER** commit `.env` file or hardcode credentials
- **ALWAYS** validate and sanitize user input
- **ALWAYS** handle authentication errors gracefully

### Testing Best Practices
- **ALWAYS** mock external API calls in tests
- **ALWAYS** use environment variables in tests (even though mocked)
- **ALWAYS** test error handling and edge cases
- **ALWAYS** run full test suite before committing

### Code Quality
- Follow existing code style and patterns
- Use type hints where appropriate
- Add docstrings to all public methods
- Handle errors gracefully with logging
- Use retry logic for external API calls

## Linting and Formatting

Currently, the repository does not have formal linting/formatting tools configured. When adding linting:

```bash
# Install linting tools (if adding them)
pip install flake8 black pylint

# Run linter
flake8 src/ tests/ --max-line-length=120

# Format code
black src/ tests/

# Run type checker
mypy src/
```

## CI/CD Considerations

For future GitHub Actions workflows:
- Place workflows in `.github/workflows/`
- Include these steps:
  1. Set up Python 3.12.3
  2. Install dependencies: `pip install -r requirements.txt`
  3. Run tests with environment variables set
  4. Run linting (if configured)
  5. Check for security vulnerabilities
- Set appropriate timeouts (10+ minutes for full workflow)
- Use GitHub Secrets for API keys and credentials

## Quick Reference Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
OPENAI_API_KEY=test SUBSTACK_EMAIL=test@test.com SUBSTACK_PASSWORD=test SUBSTACK_PUBLICATION=test python3 -m unittest discover -s tests -v

# Run specific test file
OPENAI_API_KEY=test SUBSTACK_EMAIL=test@test.com SUBSTACK_PASSWORD=test SUBSTACK_PUBLICATION=test python3 -m unittest tests.test_fact_checker_agent -v

# Check Python version
python3 --version

# Repository status
git status && git branch -a

# View recent commits
git log --oneline -10

# CLI commands
python3 cli.py setup       # Setup wizard
python3 cli.py demo        # Interactive demo
python3 cli.py generate    # Generate one post
python3 cli.py schedule    # Start scheduler
python3 cli.py status      # Show status
```

## Additional Resources

- **README.md**: Project overview, installation, and usage
- **docs/fact_checker_agent.md**: Complete fact-checker API documentation
- **IMPLEMENTATION_SUMMARY.md**: Fact-checker implementation notes
- **.env.example**: Environment variable template
- **demo.py**: Interactive demonstration of content generation
- **demo_fact_checker.py**: Interactive fact-checker demonstration

## Support and Maintenance

When issues arise:
1. Check logs in `substack_auto.log` (when running)
2. Review generated content metadata in `generated_content/`
3. Verify environment variables are set correctly
4. Run tests to identify failing components
5. Check OpenAI API status and rate limits
6. Review Substack API responses for errors