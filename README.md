# Substack Auto - AI-Powered Content Generation

An automated Substack system that creates and publishes blog entries, images, and videos using exclusively AI-generated content.

## Features

- 🤖 **AI-Generated Content**: All content is created by AI agents with no human input
- 📝 **Blog Post Generation**: Creates comprehensive, engaging blog posts on various topics
- 🖼️ **Image Generation**: Generates featured images and thumbnails using DALL-E
- 🎥 **Video Creation**: Creates slideshow-style videos with title and content slides
- 📅 **Automated Publishing**: Scheduled publishing to Substack with configurable frequency
- 🔍 **Content Validation**: Ensures all published content is AI-generated only
- 📊 **Analytics & Logging**: Comprehensive logging and publication tracking

## Technology Stack

- **Python 3.12.3** - Core application
- **OpenAI API** - Text and image generation (GPT-4, DALL-E 3)
- **CrewAI** - Multi-agent AI framework for advanced content workflows
- **Substack API** - Automated publishing
- **MoviePy** - Video generation and editing
- **PIL/Pillow** - Image processing
- **Schedule** - Automated task scheduling
- **SEO Tools** - python-slugify, BeautifulSoup4 for content optimization

## CrewAI and SEO Integration

This project leverages **CrewAI** for sophisticated multi-agent AI workflows and includes comprehensive **SEO optimization** tools to ensure content is search-engine friendly.

### CrewAI Framework

CrewAI enables the creation of AI agents that can work together to accomplish complex tasks:

- **SEO Analysis Agent**: Analyzes content for SEO best practices
- **Multi-Agent Workflows**: Coordinate multiple AI agents for complex content tasks
- **Task Orchestration**: Define and execute multi-step content optimization workflows

### SEO Optimization Features

The SEO module (`src/agents/seo_agent.py`) provides:

- **Title Optimization**: Analyzes and optimizes titles for search engines
- **Content Analysis**: Evaluates content length, structure, and readability
- **Slug Generation**: Creates SEO-friendly URL slugs
- **Meta Descriptions**: Generates optimized meta descriptions
- **Keyword Extraction**: Identifies and analyzes top keywords
- **HTML Metadata**: Extracts and validates SEO metadata from HTML
- **SEO Scoring**: Provides overall SEO score with actionable recommendations

### Using the SEO Agent

```python
from agents.seo_agent import SEOAnalyzer

# Create analyzer
analyzer = SEOAnalyzer()

# Analyze a title
title_analysis = analyzer.analyze_title("Your Blog Post Title")
print(f"Slug: {title_analysis['slug']}")
print(f"Recommendations: {title_analysis['recommendations']}")

# Analyze content
content_analysis = analyzer.analyze_content(your_content, title)
print(f"Word count: {content_analysis['word_count']}")
print(f"Top keywords: {content_analysis['top_keywords']}")

# Generate full SEO report
seo_report = analyzer.generate_seo_report(title, content)
print(f"SEO Score: {seo_report['overall_score']}/100")
print(f"Meta Description: {seo_report['meta_description']}")
```

### CrewAI Agent Usage (Advanced)

```python
from agents.seo_agent import create_seo_agent, run_seo_crew

# Create and run an SEO agent crew
result = run_seo_crew(
    title="Your Blog Post Title",
    content=your_content
)
print(result)
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/becominggiantcollective/substack_auto.git
   cd substack_auto
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## Configuration

Configure the system by editing the `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Substack Configuration
SUBSTACK_EMAIL=your_substack_email@example.com
SUBSTACK_PASSWORD=your_substack_password
SUBSTACK_PUBLICATION=your_publication_name

# Content Generation Settings
MAX_POSTS_PER_DAY=3
CONTENT_TOPICS=technology,AI,innovation,science
IMAGE_STYLE=digital art,modern,professional
VIDEO_DURATION=30

# Publishing Schedule (cron format)
PUBLISH_SCHEDULE=0 9,15,21 * * *
```

### Configuration Options

- **OPENAI_API_KEY**: Your OpenAI API key for content generation
- **SUBSTACK_***: Substack account credentials and publication details
- **MAX_POSTS_PER_DAY**: Maximum number of posts to publish per day
- **CONTENT_TOPICS**: Comma-separated list of topics for content generation
- **IMAGE_STYLE**: Preferred styles for AI-generated images
- **VIDEO_DURATION**: Duration in seconds for generated videos
- **PUBLISH_SCHEDULE**: Cron-style schedule for automated publishing

### AI Content Shaping Options

Customize how the AI generates content to match your brand voice and audience:

- **CONTENT_TONE**: The tone of voice for content (e.g., "professional and engaging", "casual and humorous")
- **TARGET_AUDIENCE**: Who the content is written for (e.g., "intelligent general audience", "beginner developers")
- **CONTENT_STYLE**: The style of content (e.g., "informative and thought-provoking", "practical and actionable")  
- **CUSTOM_INSTRUCTIONS**: Additional specific instructions for AI content generation

#### Example Configurations

**Tech Blog for Beginners:**
```env
CONTENT_TONE=friendly and encouraging
TARGET_AUDIENCE=coding beginners
CONTENT_STYLE=step-by-step and practical
CUSTOM_INSTRUCTIONS=Always include code examples and explain jargon
```

**Professional Business Blog:**
```env
CONTENT_TONE=professional and authoritative
TARGET_AUDIENCE=business executives
CONTENT_STYLE=strategic and insightful
CUSTOM_INSTRUCTIONS=Focus on ROI and business impact
```

## Usage

### Quick Start with CLI

The easiest way to get started is using the built-in CLI:

```bash
# Run the interactive demo
python cli.py demo

# Set up your configuration
python cli.py setup

# Generate and publish one blog post
python cli.py generate

# Start the automated scheduler
python cli.py schedule

# Check system status
python cli.py status
```

### Manual Usage

### Single Post Generation

Generate and publish one blog post:

```bash
python src/main.py --mode once
```

### Scheduled Publishing

Run the automated scheduler:

```bash
python src/main.py --mode schedule
```

### Check System Status

View current system status and statistics:

```bash
python src/main.py --status
```

## Architecture

The system is organized into several key components:

### AI Agents (CrewAI)

- **SEOAnalyzer**: Analyzes and optimizes content for search engines
- **CrewAI Integration**: Enables multi-agent workflows for complex tasks

### Content Generators

- **TextGenerator**: Creates blog posts using GPT-4
- **ImageGenerator**: Generates featured images using DALL-E 3
- **VideoGenerator**: Creates slideshow videos from images and text

### Publishers

- **SubstackPublisher**: Handles authentication and publishing to Substack

### Configuration

- **Settings**: Centralized configuration management using Pydantic

### Orchestration

- **ContentOrchestrator**: Main coordinator that manages the complete workflow

## Project Structure

```
substack_auto/
├── src/
│   ├── agents/
│   │   ├── __init__.py            # Agents module
│   │   └── seo_agent.py           # SEO analysis and optimization agent
│   ├── content_generators/
│   │   ├── text_generator.py      # AI text generation
│   │   ├── image_generator.py     # AI image generation
│   │   └── video_generator.py     # Video creation
│   ├── publishers/
│   │   └── substack_publisher.py  # Substack integration
│   ├── config/
│   │   └── settings.py            # Configuration management
│   └── main.py                    # Main orchestrator
├── tests/
│   ├── test_substack_auto.py      # Core test suite
│   └── test_agents.py             # Agent tests (CrewAI & SEO)
├── cli.py                         # Command-line interface
├── demo.py                        # Interactive demonstration
├── generated_content/             # Output directory (created automatically)
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## Content Generation Process

1. **Topic Selection**: AI analyzes configured topics and current trends
2. **Content Creation**: GPT-4 generates comprehensive blog posts
3. **Image Generation**: DALL-E 3 creates relevant featured images
4. **Video Production**: System creates slideshow videos with title and content slides
5. **Content Validation**: Ensures all content meets AI-only requirements
6. **Publishing**: Automated upload and publication to Substack

## AI-Only Content Validation

The system implements several measures to ensure content is AI-generated only:

- All content is flagged with `ai_generated: true`
- Content validation checks prevent publishing of non-AI content
- Comprehensive logging tracks the generation process
- No human input is accepted during content creation

## Testing

Run the full test suite:

```bash
python -m pytest tests/ -v
```

Or run individual test modules:

```bash
# Test core functionality
python tests/test_substack_auto.py

# Test CrewAI agents and SEO functionality
python tests/test_agents.py
```

### Test Coverage

- **Core System Tests** (`test_substack_auto.py`): Content generation, publishing, orchestration
- **Agent Tests** (`test_agents.py`): SEO analysis, CrewAI integration, agent workflows

The test suite includes:
- Unit tests for all major components
- Integration tests for end-to-end workflows
- SEO analyzer functionality tests
- CrewAI agent creation and task tests

## Monitoring and Logging

The system provides comprehensive logging and monitoring:

- **Activity Logs**: All generation and publishing activities
- **Error Tracking**: Detailed error logs for troubleshooting
- **Publication Records**: JSON records of all published content
- **Content Metadata**: Detailed metadata for generated content

Log files are stored in the project directory and content metadata is saved in the `generated_content` folder.

## Extensibility

The system is designed for easy extension:

- **New Content Types**: Add new generators by implementing the base interface
- **Additional Platforms**: Extend publishers for Medium, WordPress, etc.
- **Custom AI Models**: Easily swap AI models and providers
- **Advanced Scheduling**: Enhance scheduling with more complex rules

## Compliance and Ethics

- **Substack ToS**: Ensure compliance with Substack's Terms of Service
- **API Limits**: Respects OpenAI API rate limits and usage guidelines
- **Content Disclosure**: All AI-generated content is properly labeled
- **Quality Control**: Built-in validation ensures content quality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the logs in `substack_auto.log`
2. Review the generated content metadata
3. Open an issue on GitHub
4. Check the documentation for troubleshooting tips

## Roadmap

- [ ] Integration with additional AI models
- [ ] Support for more content types (podcasts, newsletters)
- [ ] Advanced analytics and performance tracking
- [ ] Integration with additional publishing platforms
- [ ] Enhanced video generation with audio
- [ ] Custom AI model fine-tuning capabilities