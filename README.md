# Substack Auto - AI-Powered Content Generation

An automated Substack system that creates and publishes blog entries, images, and videos using exclusively AI-generated content.

## Features

- 🤖 **AI-Generated Content**: All content is created by AI agents with no human input
- 📝 **Blog Post Generation**: Creates comprehensive, engaging blog posts on various topics
- 🖼️ **Image Generation**: Generates featured images and thumbnails using DALL-E
- 🎥 **Video Creation**: Creates slideshow-style videos with title and content slides
- 📅 **Automated Publishing**: Scheduled publishing to Substack with configurable frequency
- 🔍 **Content Validation**: Ensures all published content is AI-generated only
- ✅ **Fact-Checker Agent**: Validates claims, checks statistics, and assesses SEO compliance
- 📊 **Analytics & Logging**: Comprehensive logging and publication tracking

### 🚀 Innovative Features

- 📈 **Analytics Dashboard**: Track performance metrics, engagement trends, and content insights
- 🔮 **Performance Predictor**: AI-powered predictions of content success before publishing
- 🔥 **Topic Trending Agent**: Discover trending topics and timely content opportunities
- 🧪 **A/B Testing Framework**: Test multiple variations and optimize based on real data
- 💡 **Smart Insights**: Automated recommendations for content strategy improvements
- 📉 **Performance Scoring**: Multi-factor analysis of content quality and potential

## Technology Stack

- **Python 3.8+** - Core application
- **OpenAI API** - Text and image generation (GPT-4, DALL-E 3)
- **Substack API** - Automated publishing
- **MoviePy** - Video generation and editing
- **PIL/Pillow** - Image processing
- **Schedule** - Automated task scheduling

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

# View analytics dashboard
python cli.py analytics

# Predict content performance
python cli.py predict

# Get trending topics
python cli.py trends

# Manage A/B tests
python cli.py abtest

# Run innovative features demo
python cli.py innovative
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

### Content Generators

- **TextGenerator**: Creates blog posts using GPT-4
- **ImageGenerator**: Generates featured images using DALL-E 3
- **VideoGenerator**: Creates slideshow videos from images and text

### Agents

- **FactCheckerAgent**: Validates factual claims, assesses SEO value, and generates quality reports
- **AnalyticsAgent**: Tracks content performance metrics and generates actionable insights
- **PerformancePredictorAgent**: Predicts content success probability before publishing
- **TopicTrendingAgent**: Identifies trending topics and suggests timely content ideas
- **ABTestingFramework**: Manages A/B tests for content optimization

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
│   ├── content_generators/
│   │   ├── text_generator.py      # AI text generation
│   │   ├── image_generator.py     # AI image generation
│   │   └── video_generator.py     # Video creation
│   ├── agents/
│   │   ├── __init__.py            # Agent base classes
│   │   ├── fact_checker_agent.py  # Fact-checking and SEO validation
│   │   ├── analytics_agent.py     # Performance analytics and insights
│   │   ├── performance_predictor.py  # Content success prediction
│   │   ├── topic_trending.py      # Trending topic discovery
│   │   └── ab_testing.py          # A/B testing framework
│   ├── publishers/
│   │   └── substack_publisher.py  # Substack integration
│   ├── config/
│   │   └── settings.py            # Configuration management
│   └── main.py                    # Main orchestrator
├── tests/
│   ├── test_substack_auto.py      # Main test suite
│   └── test_fact_checker_agent.py # Fact-checker tests
├── docs/
│   └── fact_checker_agent.md      # Fact-checker documentation
├── cli.py                         # Command-line interface
├── demo.py                        # Interactive demonstration
├── demo_innovative_features.py    # Innovative features demo
├── generated_content/             # Output directory (created automatically)
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## Content Generation Process

1. **Topic Selection**: AI analyzes configured topics and current trends
2. **Content Creation**: GPT-4 generates comprehensive blog posts
3. **Fact-Checking**: FactCheckerAgent validates claims and assesses SEO value
4. **Image Generation**: DALL-E 3 creates relevant featured images
5. **Video Production**: System creates slideshow videos with title and content slides
6. **Content Validation**: Ensures all content meets AI-only requirements
7. **Publishing**: Automated upload and publication to Substack

## Fact-Checker Agent

The Fact-Checker Agent automatically validates content quality and SEO compliance:

### Features
- **Claim Extraction**: Identifies factual claims and statistics
- **Validation**: Cross-references claims with AI knowledge base
- **Confidence Scoring**: Rates each claim from 0.0 to 1.0
- **SEO Assessment**: Evaluates SEO value and featured snippet potential
- **Quality Reports**: Generates detailed reports with recommendations

### Usage Example

```python
from agents.fact_checker_agent import FactCheckerAgent

fact_checker = FactCheckerAgent()

# Check article quality
report = fact_checker.process({
    "title": "AI Market Growth in 2024",
    "content": "The AI market grew 47% to reach $150 billion..."
})

print(f"Claims validated: {report['summary']['valid_claims']}")
print(f"SEO score: {report['seo_report']['seo_score']}")
```

For detailed documentation, see [docs/fact_checker_agent.md](docs/fact_checker_agent.md).

## 🚀 Innovative Features

Substack Auto includes cutting-edge AI agents that take content optimization to the next level.

### 📊 Analytics Dashboard

Track your content performance with comprehensive metrics and insights:

```python
from main import ContentOrchestrator

orchestrator = ContentOrchestrator()
dashboard = orchestrator.get_analytics_dashboard()

# Access metrics
metrics = dashboard['metrics']
print(f"Total posts: {metrics['total_posts']}")
print(f"Average word count: {metrics['avg_word_count']}")

# Get insights and recommendations
insights = dashboard['insights']
for rec in insights['recommendations']:
    print(f"[{rec['priority']}] {rec['message']}")
```

**Features:**
- Performance metrics (posts, word counts, scores)
- Trend analysis by topic and date
- Automated recommendations
- Quality alerts
- Exportable reports

**CLI Usage:**
```bash
python cli.py analytics
```

### 🔮 Performance Predictor

Predict content success before publishing using AI analysis:

```python
prediction = orchestrator.predict_content_performance(post_data)

print(f"Overall score: {prediction['overall_score']:.2f}")
print(f"Success probability: {prediction['overall_prediction']['success_probability']:.2f}")

# Get factor-specific scores
factors = prediction['factors']
print(f"Title appeal: {factors['title_appeal']['score']:.2f}")
print(f"SEO potential: {factors['seo_potential']['score']:.2f}")

# Get improvement suggestions
for improvement in prediction['recommendations']['improvements']:
    print(f"- {improvement}")
```

**Prediction Factors:**
- Title appeal and catchiness
- Topic relevance and timeliness
- Content readability
- Engagement potential
- SEO optimization
- Content depth and value

**CLI Usage:**
```bash
python cli.py predict
```

### 🔥 Topic Trending Agent

Discover trending topics and get content suggestions:

```python
# Get trending topics
suggestions = orchestrator.suggest_trending_topics(count=5)

for suggestion in suggestions:
    print(f"Title: {suggestion['title_suggestion']}")
    print(f"Priority: {suggestion['priority']}")
    print(f"Relevance: {suggestion['relevance_score']:.2f}")
```

**Features:**
- AI-powered trend discovery
- Content angle suggestions
- Topic competition analysis
- Evergreen topic identification
- Keyword and hashtag recommendations

**CLI Usage:**
```bash
python cli.py trends
```

### 🧪 A/B Testing Framework

Test content variations and optimize based on real data:

```python
# Create a title test
variations = [
    {"title": "5 AI Trends That Will Transform Your Business",
     "content": base_content},
    {"title": "How AI Is Revolutionizing Business: A Complete Guide",
     "content": base_content},
    {"title": "The Ultimate AI Business Strategy for 2024",
     "content": base_content}
]

test = orchestrator.create_ab_test(
    test_name="title_optimization",
    variations=variations,
    test_type="title"
)

# Record results
orchestrator.ab_testing.record_result(
    test['test_id'],
    variation_id,
    {"views": 200, "engagement": 75, "conversions": 22}
)

# Analyze and get winner
analysis = orchestrator.ab_testing.analyze_test(test['test_id'])
print(f"Winner: {analysis['winner']['variation_name']}")
print(f"Confidence: {analysis['confidence']:.2%}")
```

**Test Types:**
- Title variations
- Subtitle variations
- Content style variations
- Full post variations

**CLI Usage:**
```bash
python cli.py abtest
```

### 💡 Integrated Workflow

Combine all features for optimal results:

1. **Analytics**: Review past performance and identify what works
2. **Trending**: Discover timely topics with high potential
3. **Prediction**: Forecast success and get improvement suggestions
4. **A/B Testing**: Test variations and optimize
5. **Generate**: Create data-driven, optimized content
6. **Publish**: Release with confidence

```python
# Example integrated workflow
orchestrator = ContentOrchestrator()

# Step 1: Get insights from analytics
dashboard = orchestrator.get_analytics_dashboard()
insights = dashboard['insights']

# Step 2: Get trending topic suggestions
topics = orchestrator.suggest_trending_topics(count=5)
best_topic = topics[0]

# Step 3: Generate content
content = orchestrator.generate_with_prediction()

# Step 4: Check prediction
prediction = content['performance_prediction']
if prediction['overall_score'] >= 0.7:
    # Step 5: Publish high-potential content
    result = orchestrator.publish_content(content)
else:
    print("Consider regenerating with improvements")
```

**Benefits:**
- Data-driven content strategy
- Higher engagement rates  
- Continuous optimization
- Reduced guesswork
- Better ROI on content creation

For detailed documentation, see [docs/fact_checker_agent.md](docs/fact_checker_agent.md).

## AI-Only Content Validation

The system implements several measures to ensure content is AI-generated only:

- All content is flagged with `ai_generated: true`
- Content validation checks prevent publishing of non-AI content
- Comprehensive logging tracks the generation process
- No human input is accepted during content creation

## Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

Or run individual test modules:

```bash
python tests/test_substack_auto.py
```

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

### ✅ Completed
- [x] AI-powered content generation (text, images, video)
- [x] Automated publishing to Substack
- [x] Fact-checking and SEO validation
- [x] Analytics dashboard with insights
- [x] Performance prediction AI
- [x] Topic trending agent
- [x] A/B testing framework
- [x] Comprehensive CLI interface

### 🚧 In Progress
- [ ] Real-time trend monitoring
- [ ] Advanced analytics visualizations
- [ ] Multi-platform publishing (Medium, WordPress, LinkedIn)

### 📋 Planned
- [ ] Social media auto-posting integration
- [ ] Voice/audio content generation (podcasts)
- [ ] Interactive content elements (polls, quizzes)
- [ ] Email newsletter segmentation
- [ ] Content calendar AI with smart scheduling
- [ ] Plagiarism detection
- [ ] Multi-agent collaboration workflows
- [ ] Custom AI model fine-tuning
- [ ] Advanced video generation with narration
- [ ] Community engagement automation