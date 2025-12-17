# OpenRouter AI Integration Guide

## What Changed?
The AI Resume Coach now uses **OpenRouter** instead of Hugging Face for AI features. OpenRouter is more reliable and provides access to multiple AI models through a unified API.

## Setup Instructions for Render Deployment

### 1. Get Your OpenRouter API Key
You already have your OpenRouter API key ready!

### 2. Add Environment Variable to Render

Go to your Render backend service and add this environment variable:

```
OPENROUTER_API_KEY=sk-or-v1-YOUR-ACTUAL-KEY-HERE
```

**Important:** Replace the value with your actual OpenRouter API key.

### 3. Current Model Configuration

The app is configured to use:
- **Model:** `meta-llama/llama-3.1-8b-instruct:free`
- **Type:** Free tier (no cost per request)
- **Max Tokens:** 200
- **Temperature:** 0.7

### 4. Alternative Models Available

If you want to switch models, you can change the `AI_MODEL` environment variable on Render:

**Free Models:**
- `meta-llama/llama-3.1-8b-instruct:free` (Current - Recommended)
- `google/gemini-flash-1.5:free`
- `mistralai/mistral-7b-instruct:free`

**Paid Models (Better Quality):**
- `anthropic/claude-3.5-sonnet` (Best quality)
- `openai/gpt-4-turbo`
- `google/gemini-pro-1.5`

### 5. Deployment

After adding the environment variable:
1. Render will automatically redeploy
2. Wait for deployment to complete
3. Test the AI features on your frontend

## Features That Use AI

1. **Resume Bullet Rewriter** (All tiers)
2. **Project Description Generator** (PRO & ULTIMATE)
3. **Resume Summary Generator** (PRO & ULTIMATE)
4. **Tone Variation** (ULTIMATE only)

## Troubleshooting

### If you get errors:
1. Verify the API key is correctly set in Render
2. Check the Render logs for specific error messages
3. Make sure the key starts with `sk-or-v1-`

### Rate Limits:
- Free tier models have rate limits
- If exceeded, consider upgrading on OpenRouter or using paid models

## Cost Considerations

**Free Tier:**
- Completely free
- Has rate limits
- Good for testing and low-volume usage

**Paid Usage:**
- Pay per token
- No rate limits
- Better model quality
- Costs vary by model (check OpenRouter pricing)

## Need Help?

Check OpenRouter documentation: https://openrouter.ai/docs
