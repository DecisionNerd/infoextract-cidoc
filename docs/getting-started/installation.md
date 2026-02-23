# Installation

## Requirements

- Python 3.13+
- An LLM API key (Google Gemini, OpenAI, Anthropic, or any LiteLLM-compatible provider)

## Install

```bash
pip install infoextract-cidoc
```

### With GraphForge support

```bash
pip install infoextract-cidoc[graphforge]
```

### Development install

```bash
git clone https://github.com/decisionnerd/infoextract-cidoc.git
cd infoextract-cidoc
pip install uv
uv sync
```

## Configuration

Set your LLM API key as an environment variable:

```bash
# Google Gemini (default)
export GOOGLE_API_KEY="your-key-here"

# Or use a .env file
echo "GOOGLE_API_KEY=your-key-here" > .env
```

The default model is `gemini/gemini-2.5-flash`. Override with:

```bash
export LANGSTRUCT_DEFAULT_MODEL="openai/gpt-4o-mini"
```
