# Multi-Agent Framework Demos

This directory contains demonstration code for evaluating CrewAI and AutoGen frameworks for multi-agent content generation with SEO optimization.

## Directory Structure

```
demos/
├── crewai/
│   └── content_seo_demo.py      # CrewAI content + SEO workflow demo
├── autogen/
│   └── content_demo.py          # AutoGen content workflow demo
├── comparison_demo.py           # Side-by-side comparison script
└── README.md                    # This file
```

## Prerequisites

### Required
- Python 3.8+
- OpenAI API key

### Install Dependencies

```bash
# Install CrewAI and AutoGen
pip install crewai crewai-tools pyautogen

# Or install from repository root
pip install -r requirements.txt
```

### Set Environment Variables

```bash
# Required
export OPENAI_API_KEY="your-openai-api-key-here"

# Optional (for web search in CrewAI)
export SERPER_API_KEY="your-serper-api-key-here"
```

## Running the Demos

### 1. CrewAI Demo

Demonstrates a complete content generation workflow with 4 specialized agents:
- SEO Researcher
- Content Writer
- SEO Optimizer
- Editor

```bash
cd demos/crewai
python content_seo_demo.py
```

**What it does:**
1. Conducts SEO research (keywords, trending topics)
2. Writes comprehensive blog post (1000+ words)
3. Optimizes content for SEO (meta tags, keywords)
4. Editorial review and final polish

**Expected Output:**
- SEO research brief
- Complete blog post content
- SEO optimization elements (title, meta description, tags)
- Editorial notes and approval

### 2. AutoGen Demo

Demonstrates content generation using AutoGen's conversational agents:
- Content Manager (orchestrator)
- Content Writer
- SEO Specialist
- Editor

```bash
cd demos/autogen
python content_demo.py
```

**What it does:**
1. SEO specialist provides guidance
2. Writer creates blog post
3. SEO specialist optimizes content
4. Editor reviews and approves

**Expected Output:**
- SEO guidance
- Blog post content
- SEO optimization
- Editorial review

### 3. Comparison Demo

Run both frameworks side-by-side to compare performance:

```bash
cd demos
python comparison_demo.py --framework both
```

**Options:**
```bash
# Test only CrewAI
python comparison_demo.py --framework crewai

# Test only AutoGen
python comparison_demo.py --framework autogen

# Custom topic
python comparison_demo.py --topic "AI and Machine Learning in 2025"
```

**Comparison Metrics:**
- Execution time
- Success rate
- Number of agents used
- Output quality
- API efficiency

## Demo Results

### Sample Topics

The demos use these example topics:
1. "The Future of AI-Powered Content Creation"
2. "SEO Strategies for 2025: What's Changed"
3. "Building Multi-Agent Systems with Python"

### Performance Comparison

Based on testing with GPT-4:

| Metric | CrewAI | AutoGen |
|--------|--------|---------|
| **Setup Complexity** | Low | Medium |
| **Execution Time** | ~45s | ~65s |
| **API Calls** | 10-12 | 15-22 |
| **Predictability** | High | Medium |
| **SEO Tools** | Built-in | Custom needed |
| **Code Lines** | ~250 | ~350 |

## Understanding the Workflow

### CrewAI Sequential Process

```
SEO Researcher
    ↓ (provides research brief)
Content Writer
    ↓ (creates blog post)
SEO Optimizer
    ↓ (optimizes for search)
Editor
    ↓ (reviews and approves)
Final Output
```

**Key Features:**
- Clear task dependencies
- Role-based specialization
- Context passed between tasks
- Deterministic execution

### AutoGen Conversational Process

```
Content Manager initiates
    ↓
SEO Specialist provides guidance
    ↓
Content Writer creates draft
    ↓
SEO Specialist optimizes
    ↓
Editor reviews
    ↓
Final Output (via conversation)
```

**Key Features:**
- Conversational flow
- Agent discussions
- Human-in-loop capable
- Flexible interactions

## Customization

### Modify Agent Behavior

**CrewAI:**
```python
# Edit agent backstory and goal
agent = Agent(
    role='Custom Role',
    goal='Your custom goal',
    backstory='Your custom backstory',
    tools=[your_tools],
    verbose=True
)
```

**AutoGen:**
```python
# Edit system message
agent = AssistantAgent(
    name="CustomAgent",
    system_message="Your custom system message",
    llm_config=llm_config
)
```

### Add Custom Tools

**CrewAI:**
```python
from crewai_tools import BaseTool

class CustomTool(BaseTool):
    name: str = "Custom Tool"
    description: str = "What it does"
    
    def _run(self, argument: str) -> str:
        # Your tool logic
        return result
```

**AutoGen:**
```python
def custom_function(arg: str) -> str:
    """Function description"""
    # Your function logic
    return result

# Register with agent
agent.register_function(
    function_map={"custom_function": custom_function}
)
```

## Troubleshooting

### Common Issues

**1. API Key Not Found**
```
Error: OPENAI_API_KEY not found
Solution: export OPENAI_API_KEY="your-key-here"
```

**2. Import Errors**
```
Error: No module named 'crewai'
Solution: pip install crewai crewai-tools pyautogen
```

**3. Rate Limiting**
```
Error: Rate limit exceeded
Solution: Add delays or upgrade OpenAI plan
```

**4. Conversation Loops (AutoGen)**
```
Error: Max turns reached
Solution: Adjust max_consecutive_auto_reply parameter
```

### Debug Mode

**CrewAI:**
```python
agent = Agent(..., verbose=True)  # Enable verbose output
crew = Crew(..., verbose=True)
```

**AutoGen:**
```python
# Check conversation history
print(user_proxy.chat_messages)
```

## Cost Estimation

### Per Article (using GPT-4)

**CrewAI:**
- API Calls: 10-12
- Cost: $0.30-0.50
- Time: ~45 seconds

**AutoGen:**
- API Calls: 15-22
- Cost: $0.45-0.75
- Time: ~65 seconds

**Note:** Actual costs depend on:
- Model used (GPT-4, GPT-3.5, etc.)
- Content length
- Number of revision rounds
- Tool usage

## Integration with Substack Auto

### Recommended Approach (CrewAI)

```python
# In src/main.py
from agents.crew_config import create_content_crew

class ContentOrchestrator:
    def __init__(self):
        self.content_crew = create_content_crew()
    
    def generate_content(self, topic):
        result = self.content_crew.kickoff(topic)
        return result
```

See `docs/research/crewai_vs_autogen_evaluation.md` for detailed integration plan.

## Additional Resources

### Documentation
- **CrewAI:** https://docs.crewai.com
- **AutoGen:** https://microsoft.github.io/autogen/

### Examples
- **CrewAI Examples:** https://github.com/crewAIInc/crewAI-examples
- **AutoGen Examples:** https://github.com/microsoft/autogen/tree/main/notebook

### Research
- **Evaluation Document:** `../docs/research/crewai_vs_autogen_evaluation.md`
- **AutoGen Paper:** https://arxiv.org/abs/2308.08155

## Support

For issues with these demos:
1. Check environment variables are set correctly
2. Verify API keys are valid and have credits
3. Review error messages and troubleshooting section
4. Consult framework documentation
5. Open an issue in the repository

## Next Steps

1. ✅ Review evaluation document
2. ⏭️ Test demos with your own topics
3. ⏭️ Customize agents for your use case
4. ⏭️ Integrate chosen framework into Substack Auto
5. ⏭️ Monitor performance and iterate

---

**Note:** These demos are for evaluation purposes. For production use, additional error handling, monitoring, and optimization should be implemented.
