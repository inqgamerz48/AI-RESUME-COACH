# OpenRouter Free Models - Verified Working

## Working Free Tier Models (as of Dec 2024)

Use these model identifiers in your `AI_MODEL` environment variable:

### Recommended (Fast & Reliable):
- `mistralai/mistral-7b-instruct:free` ⭐ **CURRENT DEFAULT**
- `google/gemini-flash-1.5:free`
- `meta-llama/llama-3.2-3b-instruct:free`

### Alternative Options:
- `nousresearch/hermes-3-llama-3.1-405b:free`
- `microsoft/phi-3-mini-128k-instruct:free`
- `qwen/qwen-2-7b-instruct:free`

## How to Change Models

### Option 1: Environment Variable (Recommended for Production)
Add to your Render environment:
```
AI_MODEL=mistralai/mistral-7b-instruct:free
```

### Option 2: Code Change (if you want a different default)
Edit `backend/app/core/config.py`:
```python
AI_MODEL: str = "google/gemini-flash-1.5:free"
```

## Model Comparison

| Model | Speed | Quality | Context | Best For |
|-------|-------|---------|---------|----------|
| `mistral-7b-instruct:free` | ⚡⚡⚡ | ⭐⭐⭐⭐ | 32K | General use (default) |
| `gemini-flash-1.5:free` | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 1M | Best quality |
| `llama-3.2-3b-instruct:free` | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | 128K | Fastest |

## Troubleshooting

### Getting 404 Errors?
- Model identifier is wrong or model was removed
- Try one of the verified models above
- Check https://openrouter.ai/docs#models for latest free models

### Getting 402 Errors?
- Your OpenRouter account needs credits
- Free models should not require credits, but check your account status

### Getting 429 Errors?
- You've hit the rate limit
- Wait a few minutes and try again
- Free tier has lower rate limits than paid

## Checking Available Models

Visit: https://openrouter.ai/docs#models

Look for models with:
- `:free` suffix
- "Free" badge in the UI
- $0.00 pricing

## Note on Model Names

OpenRouter uses specific suffixes:
- `:free` - Free tier version (rate limited)
- No suffix - Standard paid version
- `:extended` - Extended context version (paid)

Always use the `:free` suffix for zero-cost usage!
