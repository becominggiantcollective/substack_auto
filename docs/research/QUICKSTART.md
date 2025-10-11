# Quick Start Guide: Multi-Agent Framework Evaluation

**Goal:** Get up and running with the CrewAI vs AutoGen demos in 5 minutes.

## Prerequisites

```bash
# Check Python version (3.8+ required)
python --version

# Check you have pip
pip --version
```

## Installation (2 minutes)

```bash
# Navigate to repository
cd substack_auto

# Install both frameworks
pip install crewai crewai-tools pyautogen

# Optional: Install original requirements if not already done
pip install -r requirements.txt
```

## Setup API Keys (1 minute)

```bash
# Required for demos
export OPENAI_API_KEY="sk-..."

# Optional (for web search in CrewAI)
export SERPER_API_KEY="..."
```

**Where to get API keys:**
- OpenAI: https://platform.openai.com/api-keys
- Serper (optional): https://serper.dev/api-key

## Run Your First Demo (2 minutes)

### Option 1: CrewAI Demo (Recommended)

```bash
cd demos/crewai
python content_seo_demo.py
```

**What you'll see:**
- 4 agents working sequentially
- SEO research → Content writing → Optimization → Review
- Complete blog post with SEO elements
- Execution time: ~45 seconds

### Option 2: AutoGen Demo

```bash
cd demos/autogen
python content_demo.py
```

**What you'll see:**
- Conversational agent workflow
- Content generation with reviews
- Execution time: ~65 seconds

### Option 3: Side-by-Side Comparison

```bash
cd demos
python comparison_demo.py --framework both
```

**What you'll see:**
- Both frameworks running same task
- Performance comparison
- Cost analysis
- Recommendation summary

## What's Next?

### Read the Full Evaluation
```bash
# Executive summary (5 min read)
cat docs/research/EXECUTIVE_SUMMARY.md

# Full evaluation (20 min read)
cat docs/research/crewai_vs_autogen_evaluation.md

# Demo documentation
cat demos/README.md
```

### Try Custom Topics
```bash
cd demos
python comparison_demo.py --topic "Your Custom Topic Here" --framework crewai
```

### Review Integration Example
```bash
# See how CrewAI integrates with existing code
cat demos/crewai/integration_example.py
```

## Understanding the Output

### CrewAI Output Structure
```
SEO Research Brief:
- Keywords: [list]
- Structure: [headers]
- Questions: [list]

Blog Post Content:
- Title
- Subtitle  
- Body (1000+ words)

SEO Optimization:
- Meta description
- Tags
- Image suggestions

Editorial Review:
- Quality notes
- Approval status
```

### Cost Estimation

**Per article with GPT-4:**
- CrewAI: $0.30-0.50
- AutoGen: $0.45-0.75

**For 100 articles/month:**
- CrewAI: $30-50
- AutoGen: $45-75
- **Savings with CrewAI: $15-25/month**

## Troubleshooting

### API Key Issues
```bash
# Check if key is set
echo $OPENAI_API_KEY

# Set key for current session
export OPENAI_API_KEY="your-key"

# Persist key (add to ~/.bashrc or ~/.zshrc)
echo 'export OPENAI_API_KEY="your-key"' >> ~/.bashrc
```

### Import Errors
```bash
# Reinstall packages
pip install --upgrade crewai crewai-tools pyautogen

# Check installations
pip list | grep -E "crewai|autogen"
```

### Rate Limiting
If you hit rate limits:
```bash
# Use GPT-3.5 for testing (cheaper, faster)
# Edit demo files to use "gpt-3.5-turbo" instead of "gpt-4"
```

### Connection Issues
```bash
# Test OpenAI connection
python -c "import openai; print('OpenAI module loaded')"

# Check internet connectivity
ping -c 3 api.openai.com
```

## Key Files Reference

| File | Purpose | Read Time |
|------|---------|-----------|
| `docs/research/EXECUTIVE_SUMMARY.md` | Decision overview | 5 min |
| `docs/research/crewai_vs_autogen_evaluation.md` | Full evaluation | 20 min |
| `demos/README.md` | Demo documentation | 10 min |
| `demos/crewai/content_seo_demo.py` | CrewAI demo code | 5 min |
| `demos/autogen/content_demo.py` | AutoGen demo code | 5 min |
| `demos/comparison_demo.py` | Comparison tool | 3 min |
| `demos/crewai/integration_example.py` | Integration guide | 8 min |

## Common Commands

```bash
# Quick test CrewAI
cd demos/crewai && python content_seo_demo.py

# Quick test AutoGen
cd demos/autogen && python content_demo.py

# Compare both
cd demos && python comparison_demo.py --framework both

# Custom topic test
cd demos && python comparison_demo.py --topic "AI in Healthcare" --framework crewai

# View evaluation
less docs/research/crewai_vs_autogen_evaluation.md

# View summary
less docs/research/EXECUTIVE_SUMMARY.md
```

## Demo Topics

Pre-configured topics you can use:
1. "The Future of AI-Powered Content Creation"
2. "SEO Strategies for 2025: What's Changed"
3. "Building Multi-Agent Systems with Python"

Or use your own:
```bash
python comparison_demo.py --topic "Your Topic" --framework both
```

## Expected Results

### CrewAI (Recommended)
✅ Faster execution (~45s)  
✅ Lower cost (~$0.40)  
✅ More predictable  
✅ Better SEO integration  
✅ Production-ready  

### AutoGen
✅ More flexible conversations  
⚠️ Slower (~65s)  
⚠️ Higher cost (~$0.60)  
⚠️ Less predictable  
ℹ️ Better for code generation  

## Decision Summary

**Recommendation: CrewAI** 

**Why:**
- 30-40% cost savings
- Purpose-built for content workflows
- Superior SEO capabilities
- Faster implementation
- More predictable behavior

**Full rationale:** See `docs/research/crewai_vs_autogen_evaluation.md`

## Questions?

1. **Which demo should I run first?**  
   → Run `demos/comparison_demo.py --framework both` to see both

2. **How much will this cost me to test?**  
   → ~$1-2 for a few test runs with GPT-4

3. **Can I use GPT-3.5 instead?**  
   → Yes, edit demo files to use "gpt-3.5-turbo"

4. **What if I don't have SERPER_API_KEY?**  
   → Demos will work without it, just no web search

5. **How do I integrate this into my project?**  
   → See `demos/crewai/integration_example.py`

## Next Steps After Testing

1. ✅ Run demos
2. ✅ Review evaluation documents
3. ⏭️ Discuss with team
4. ⏭️ Plan integration timeline
5. ⏭️ Begin Phase 1 implementation

---

**Time to complete this guide:** 5 minutes  
**Time to understand evaluation:** +25 minutes  
**Total time investment:** 30 minutes

**Value gained:** Clear decision on multi-agent framework backed by working code and comprehensive analysis.

---

**Questions or issues?** Check `demos/README.md` for detailed troubleshooting.
