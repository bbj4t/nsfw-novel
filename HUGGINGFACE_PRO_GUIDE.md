# Hugging Face Pro Account Integration Guide

## Overview

Yes, you can absolutely run inference with the Hugging Face Transformers pipeline! This project now supports both traditional model loading and the more efficient pipeline API, which is especially beneficial for Pro account users.

## Benefits of Using Pipeline with Pro Account

### 🚀 Performance Advantages
- **Faster Downloads**: Priority access to model repositories
- **Optimized Loading**: Pipeline API handles model optimization automatically
- **Better Memory Management**: Automatic device mapping and memory optimization
- **Rate Limit Benefits**: Higher API limits for gated models

### 💎 Pro Account Features
- **Priority Access**: Faster model downloads during high traffic
- **Gated Models**: Access to restricted models (with approval)
- **Enhanced Support**: Better customer support for technical issues
- **Advanced Features**: Early access to new Hugging Face features

## Quick Start with Pipeline

### 1. Using the New Pipeline Integration

```python
from model_integration_pipeline import ModelIntegrationPipeline

# Initialize with pipeline (recommended for Pro accounts)
model = ModelIntegrationPipeline(
    model_name="UnfilteredAI/NSFW-3B",
    use_mock=False,  # Use actual model
    use_pipeline=True  # Enable pipeline API
)

# Generate a story
story = model.generate_story(
    prompt="A romantic evening in Paris",
    genre="romance",
    length="medium",
    temperature=0.7
)
```

### 2. Running the Pipeline-Optimized App

```bash
# Use the new pipeline-optimized Flask app
python app_pipeline.py
```

### 3. Testing the Pipeline

```bash
# Run the example script
python example_pipeline_usage.py
```

## Configuration Options

### Basic Configuration

```python
# Standard configuration
model = ModelIntegrationPipeline(
    model_name="UnfilteredAI/NSFW-3B",
    use_pipeline=True,
    use_mock=False
)
```

### Advanced Configuration

```python
# Advanced configuration with custom parameters
model = ModelIntegrationPipeline(
    model_name="UnfilteredAI/NSFW-3B",
    use_pipeline=True,
    use_mock=False,
    device="cuda",  # Force GPU usage
    torch_dtype="float16",  # Memory optimization
    trust_remote_code=True  # For custom models
)
```

## Supported Models

### Recommended Models for Pro Accounts

1. **UnfilteredAI/NSFW-3B** (Default)
   - Size: ~3GB
   - Good balance of quality and performance
   - Well-optimized for pipeline usage

2. **NeverSleep/Noromaid-3B-v0.1.1**
   - Size: ~3GB
   - Alternative NSFW-focused model
   - Good for variety in outputs

3. **PygmalionAI/pygmalion-6b**
   - Size: ~6GB
   - Excellent for character-based storytelling
   - Requires more GPU memory

4. **Undi95/ReMM-NSFW**
   - Variable size
   - Specialized for NSFW content
   - May require approval for access

### Switching Models

```python
# Switch to a different model
model = ModelIntegrationPipeline(
    model_name="PygmalionAI/pygmalion-6b",
    use_pipeline=True
)
```

## API Endpoints (Pipeline Version)

### Generate Story
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A mysterious encounter",
    "genre": "fantasy",
    "length": "medium",
    "temperature": 0.8
  }'
```

### Check Model Status
```bash
curl http://localhost:5000/health
```

### List Available Models
```bash
curl http://localhost:5000/api/models
```

### Switch Model (Pro Feature)
```bash
curl -X POST http://localhost:5000/api/switch-model \
  -H "Content-Type: application/json" \
  -d '{"model_name": "PygmalionAI/pygmalion-6b"}'
```

## Authentication Setup

### 1. Set Your Hugging Face Token

```bash
# Option 1: Environment variable
export HUGGINGFACE_HUB_TOKEN="your_token_here"

# Option 2: Login via CLI
huggingface-cli login
```

### 2. Verify Pro Account Status

```python
from huggingface_hub import whoami

# Check your account status
user_info = whoami()
print(f"Username: {user_info['name']}")
print(f"Pro Account: {user_info.get('isPro', False)}")
```

## Performance Optimization

### Memory Optimization

```python
# For limited GPU memory
model = ModelIntegrationPipeline(
    model_name="UnfilteredAI/NSFW-3B",
    use_pipeline=True,
    torch_dtype="float16",  # Reduce memory usage
    device_map="auto",     # Automatic device placement
    low_cpu_mem_usage=True # Optimize CPU memory
)
```

### Speed Optimization

```python
# For maximum speed
model = ModelIntegrationPipeline(
    model_name="UnfilteredAI/NSFW-3B",
    use_pipeline=True,
    torch_dtype="float16",
    device="cuda",
    use_cache=True  # Enable KV cache
)
```

## Troubleshooting

### Common Issues

1. **Model Download Slow**
   - Verify Pro account status
   - Check internet connection
   - Try different model mirror

2. **GPU Memory Error**
   - Use `torch_dtype="float16"`
   - Enable `device_map="auto"`
   - Try smaller model

3. **Authentication Error**
   - Verify Hugging Face token
   - Check model access permissions
   - Ensure Pro account is active

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check model info
model_info = model.get_model_info()
print(f"Debug info: {model_info}")
```

## Comparison: Traditional vs Pipeline

| Feature | Traditional | Pipeline |
|---------|-------------|----------|
| Setup Complexity | High | Low |
| Memory Usage | Manual optimization | Automatic |
| Performance | Good | Better |
| Pro Account Benefits | Limited | Full |
| Code Simplicity | Complex | Simple |
| Error Handling | Manual | Built-in |

## Migration Guide

### From Traditional to Pipeline

```python
# Old way (traditional)
from model_integration import ModelIntegration
model = ModelIntegration("UnfilteredAI/NSFW-3B")

# New way (pipeline)
from model_integration_pipeline import ModelIntegrationPipeline
model = ModelIntegrationPipeline(
    "UnfilteredAI/NSFW-3B", 
    use_pipeline=True
)
```

### App Migration

```python
# Replace in your app.py
# from model_integration import ModelIntegration
from model_integration_pipeline import ModelIntegrationPipeline

# Update initialization
model = ModelIntegrationPipeline(
    model_name="UnfilteredAI/NSFW-3B",
    use_pipeline=True,  # Enable pipeline
    use_mock=False      # Use actual model
)
```

## Next Steps

1. **Test the Pipeline**: Run `python example_pipeline_usage.py`
2. **Start the App**: Run `python app_pipeline.py`
3. **Explore Models**: Try different models via the API
4. **Optimize Settings**: Adjust parameters for your hardware
5. **Monitor Performance**: Use the health endpoint to track status

## Support

For issues specific to:
- **Pipeline Integration**: Check the example files and debug logs
- **Pro Account Features**: Contact Hugging Face support
- **Model Access**: Verify permissions and authentication
- **Performance**: Review optimization settings

Your Pro account gives you access to priority support and advanced features - make sure to leverage these benefits!