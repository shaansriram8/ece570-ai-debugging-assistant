# Model Migration to Code-Specific Models

## Overview
Migrated from general-purpose models (Llama-3.2-1B/3B) to code-specific models for better code analysis accuracy.

## Changes Made

### 1. Updated `backend/config.py`
- **Primary Model**: Changed to `Qwen/Qwen2.5-Coder-1.5B-Instruct`
  - Code-specific model optimized for code understanding
  - 1.5B parameters
  - Better at syntax analysis, language-specific rules
  
- **Secondary Model**: Changed to `Qwen/Qwen2.5-Coder-7B-Instruct`
  - Code-specific model with better quality
  - 7B parameters
  - More accurate for complex code analysis

### 2. Updated `backend/env.example`
- Added examples for code-specific models
- Included fallback options if code models don't work

## Model Comparison

| Model | Type | Parameters | Code-Specific | Status |
|-------|------|------------|---------------|--------|
| `meta-llama/Llama-3.2-1B-Instruct` | General | 1B | ❌ | ✅ Works |
| `meta-llama/Llama-3.2-3B-Instruct` | General | 3B | ❌ | ✅ Works |
| `Qwen/Qwen2.5-Coder-1.5B-Instruct` | Code | 1.5B | ✅ | ⚠️ Testing |
| `Qwen/Qwen2.5-Coder-7B-Instruct` | Code | 7B | ✅ | ⚠️ Testing |
| `deepseek-ai/DeepSeek-Coder-1.3B-Instruct` | Code | 1.3B | ✅ | ⚠️ Testing |

## Router API Compatibility

**Important**: The Hugging Face router API (`https://router.huggingface.co/v1/chat/completions`) may have limited model support. 

### Testing Status
- Models are being called (latency recorded)
- Some models may not produce valid JSON responses
- Need to test each model individually

### If Code Models Don't Work
If the code-specific models fail to produce valid responses, you can:

1. **Use environment variables** to override:
   ```bash
   PRIMARY_MODEL=meta-llama/Llama-3.2-1B-Instruct
   SECONDARY_MODEL=meta-llama/Llama-3.2-3B-Instruct
   ```

2. **Update config.py** directly with known working models

3. **Test models individually** to find which ones work with router API

## Expected Improvements

With code-specific models, you should see:
- ✅ Better syntax error detection (e.g., missing semicolons)
- ✅ More accurate language-specific analysis
- ✅ Better understanding of code structure
- ✅ Reduced hallucination of non-existent errors

## Next Steps

1. **Test the new models** with actual code examples
2. **Monitor for errors** - if models don't work, use fallback
3. **Update models** in `.env` file if needed
4. **Document which models work** for future reference

## Troubleshooting

If you see "All models failed to produce valid responses":
1. Check if models are available on router API
2. Try fallback models (Llama-3.2-1B/3B)
3. Check backend logs for specific error messages
4. Verify HF_API_KEY is set correctly

