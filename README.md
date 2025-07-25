# NSFW Novel Generator

A web application for generating NSFW stories using AI language models. This project is designed to run in GitHub Codespaces and uses the Hugging Face Transformers library with the UnfilteredAI/NSFW-3B model for story generation.

## Features

- Web-based UI for generating NSFW stories
- Support for different genres (Romance, Fantasy, Sci-Fi, Contemporary, Historical)
- Adjustable story length and creativity settings
- Flask backend API for story generation
- Integration with Hugging Face Transformers for using the UnfilteredAI/NSFW-3B model
- Designed to work with both local and cloud-hosted language models

## Getting Started with GitHub Codespaces

1. Click the "Code" button on the GitHub repository page
2. Select the "Codespaces" tab
3. Click "Create codespace on main"
4. Wait for the codespace to initialize

The application will automatically start and be available on port 5000. GitHub Codespaces will provide a link to open the application in your browser.

## Local Development

If you want to run the application locally instead of in Codespaces:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
   - Note: If you encounter issues with package installation, try installing without version constraints: `pip install flask numpy requests transformers torch accelerate sentencepiece`
3. Run the application: `python app.py`
4. Open your browser to `http://localhost:5000`

## Using with the UnfilteredAI/NSFW-3B Model

By default, the application runs in "mock mode" and generates predefined stories to save resources. To use it with the actual UnfilteredAI/NSFW-3B model:

1. Update the `app.py` file to initialize the model with `use_mock=False`:

```python
model = ModelIntegration(model_name="UnfilteredAI/NSFW-3B", use_mock=False)
```

2. The model will be automatically downloaded from Hugging Face the first time you run the application
3. Note that this requires significant RAM and disk space as the model is approximately 3GB in size

### Using with Other Hugging Face Models

You can also use other Hugging Face models by changing the `model_name` parameter:

```python
model = ModelIntegration(model_name="YourPreferredModel/model-name", use_mock=False)
```

## Project Structure

- `app.py` - Flask application and API endpoints
- `index.html` - Web UI for the application
- `model_integration.py` - Integration with language models
- `requirements.txt` - Python dependencies
- `.devcontainer/` - Configuration for GitHub Codespaces

## Notes on Model Selection

This application is configured to use the UnfilteredAI/NSFW-3B model from Hugging Face, which is specifically designed for NSFW content generation. Other models you might consider:

- UnfilteredAI/NSFW-3B - The default model, good balance of quality and resource usage
- NeverSleep/Noromaid-3B-v0.1.1 - Another NSFW-focused model
- PygmalionAI/pygmalion-6b - Good for character-based storytelling
- Undi95/ReMM-NSFW - Specialized for NSFW content

All these models can be found on Hugging Face and can be used by changing the `model_name` parameter in the application.

## Running on Kaggle

If you want to leverage Kaggle's free GPU resources to run the model:

1. Check the `KAGGLE_USAGE.md` file for detailed instructions on setting up and running the model on Kaggle
2. You can either run the model directly on Kaggle using the provided notebook templates or set up an API connection between GitHub Codespaces and Kaggle
3. The Kaggle notebooks (`kaggle_notebook_template.ipynb` and `kaggle_api_notebook.ipynb`) are configured to use the T4 GPU available in Kaggle's free tier

## Troubleshooting

### Package Installation Issues

- If you encounter errors with `accelerators` package, use `accelerate` instead. The requirements.txt has been updated to reflect this.
- For Windows users, some packages might require Microsoft Visual C++ Build Tools. Install the [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) with the "Desktop development with C++" workload.
- If you're having issues with specific package versions, try installing without version constraints as mentioned in the Local Development section.

### Model Loading Issues

- If you encounter out-of-memory errors when loading the model, consider using the Kaggle option described in `KAGGLE_USAGE.md`.
- The application will automatically fall back to mock mode if there are issues loading the model.

## License

This project is for educational purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations regarding AI-generated content.