# NSFW Novel Generator - Hugging Face Spaces Deployment

🚀 **Deploy this NSFW novel generator on Hugging Face Spaces with GPU acceleration and pipeline optimization!**

## 🎯 Quick Deploy to Hugging Face Spaces

### Option 1: Direct Upload

1. **Create a new Space**:
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Gradio" as the SDK
   - Select "Docker" as the deployment method
   - Choose GPU hardware (recommended: T4 small or better)

2. **Upload files**:
   ```
   Dockerfile
   app_spaces.py
   model_integration_pipeline.py
   requirements.txt
   README_SPACES.md
   ```

3. **Configure Space**:
   - Set visibility (Private recommended for NSFW content)
   - Enable GPU if available
   - Add appropriate content warnings

### Option 2: Git Repository

1. **Clone and push to Hugging Face**:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/nsfw-novel-generator
   cd nsfw-novel-generator
   
   # Copy files from this project
   cp /path/to/this/project/{Dockerfile,app_spaces.py,model_integration_pipeline.py,requirements.txt} .
   
   git add .
   git commit -m "Initial deployment"
   git push
   ```

## 🔧 Configuration

### Hardware Requirements

| Hardware | Model Support | Performance | Cost |
|----------|---------------|-------------|----- |
| CPU Basic | Mock mode only | Slow | Free |
| CPU Upgrade | Limited | Moderate | Low |
| T4 Small | Full support | Good | Medium |
| T4 Medium | Full support | Better | Higher |
| A10G Small | Full support | Excellent | Highest |

**Recommended**: T4 Small for best balance of performance and cost.

### Environment Variables

Optional environment variables you can set in your Space:

```bash
# Hugging Face token (for private models)
HUGGINGFACE_HUB_TOKEN=your_token_here

# Model configuration
MODEL_NAME=UnfilteredAI/NSFW-3B
USE_PIPELINE=true
DEVICE=auto

# Performance tuning
TORCH_DTYPE=float16
MAX_MEMORY_GB=8
```

### Space Configuration (spaces/config.yaml)

```yaml
title: NSFW Novel Generator
sdk: gradio
sdk_version: 4.0.0
app_file: app_spaces.py
pinned: false
license: mit
short_description: AI-powered NSFW novel generator using UnfilteredAI/NSFW-3B
tags:
  - text-generation
  - creative-writing
  - nsfw
  - transformers
  - pipeline
models:
  - UnfilteredAI/NSFW-3B
hardware: t4-small
suggest_hardware: t4-small
```

## 🚀 Features

### Core Functionality
- **Pipeline Optimization**: Uses Hugging Face pipeline for efficient inference
- **GPU Acceleration**: Automatic GPU detection and utilization
- **Memory Management**: Optimized memory usage with automatic device mapping
- **Interactive UI**: Clean Gradio interface with real-time generation

### Advanced Features
- **Parameter Control**: Temperature, top-p, max tokens adjustment
- **Genre Selection**: Multiple genre options for guided generation
- **Length Control**: Short, medium, long story options
- **Example Prompts**: Pre-built examples for quick testing
- **Status Monitoring**: Real-time model status and performance metrics

## 📋 File Structure

```
.
├── Dockerfile                    # Docker configuration for Spaces
├── app_spaces.py                 # Main Gradio application
├── model_integration_pipeline.py # Pipeline-optimized model integration
├── requirements.txt              # Python dependencies
├── README_SPACES.md             # This file
└── spaces/
    └── config.yaml              # Space configuration (optional)
```

## 🔒 Content Policy & Safety

### Important Considerations

1. **Content Warnings**: This application generates adult content
2. **Age Restrictions**: Ensure compliance with platform policies
3. **Privacy**: Consider making your Space private
4. **Moderation**: Monitor generated content for policy compliance

### Recommended Settings

```python
# In app_spaces.py, add content filtering if needed
def filter_content(text):
    # Add your content filtering logic here
    return text
```

## 🛠️ Customization

### Change Model

To use a different model, modify `app_spaces.py`:

```python
model = ModelIntegrationPipeline(
    model_name="YOUR_MODEL_NAME",  # Change this
    use_mock=False,
    use_pipeline=True
)
```

### Adjust UI

Customize the Gradio interface in `app_spaces.py`:

```python
# Modify theme
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    # Your customizations
```

### Performance Tuning

Optimize for your hardware:

```python
# For limited memory
model = ModelIntegrationPipeline(
    model_name="UnfilteredAI/NSFW-3B",
    use_pipeline=True,
    torch_dtype="float16",  # Reduce memory
    device_map="auto"
)
```

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Fails**
   - Check GPU availability
   - Verify model name
   - Ensure sufficient memory

2. **Slow Performance**
   - Upgrade to GPU hardware
   - Enable pipeline optimization
   - Reduce max_tokens

3. **Out of Memory**
   - Use `torch_dtype="float16"`
   - Enable `device_map="auto"`
   - Reduce batch size

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Health Check

Monitor your Space:

```python
# Check model status
model_info = model.get_model_info()
print(f"Status: {model_info}")
```

## 📊 Performance Metrics

### Expected Performance

| Hardware | Load Time | Generation Speed | Memory Usage |
|----------|-----------|------------------|-------------|
| CPU | 2-5 min | 30-60s per story | 4-8 GB |
| T4 Small | 30-60s | 5-15s per story | 6-12 GB |
| T4 Medium | 20-40s | 3-10s per story | 8-16 GB |
| A10G | 15-30s | 2-5s per story | 10-20 GB |

### Optimization Tips

1. **Use Pipeline**: Always enable `use_pipeline=True`
2. **GPU Memory**: Monitor usage with `nvidia-smi`
3. **Batch Processing**: Process multiple requests efficiently
4. **Caching**: Enable model caching for faster subsequent loads

## 🔗 Related Resources

- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://gradio.app/docs/)
- [Transformers Pipeline Guide](https://huggingface.co/docs/transformers/main_classes/pipelines)
- [UnfilteredAI/NSFW-3B Model](https://huggingface.co/UnfilteredAI/NSFW-3B)

## 📝 License

MIT License - See LICENSE file for details.

## ⚠️ Disclaimer

This application generates fictional adult content. Users are responsible for:
- Compliance with local laws and regulations
- Appropriate use of generated content
- Respecting platform terms of service
- Age verification where required

Use responsibly and ethically.