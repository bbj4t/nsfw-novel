# NSFW Novel Generator

A web application for generating NSFW stories using AI language models. This project is designed to run in GitHub Codespaces and can be configured to use various language models for story generation.

## Features

- Web-based UI for generating NSFW stories
- Support for different genres (Romance, Fantasy, Sci-Fi, Contemporary, Historical)
- Adjustable story length and creativity settings
- Flask backend API for story generation
- Designed to work with self-hosted language models

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
3. Run the application: `python app.py`
4. Open your browser to `http://localhost:5000`

## Using with a Real Language Model

By default, the application runs in "mock mode" and generates predefined stories. To use it with a real language model:

1. Download a GGUF format model file (e.g., Kunoichi-7B, Fimbulvetr-10.7B, or another NSFW-tuned model)
2. Update the `app.py` file to initialize the model with the path to your model file:

```python
model = ModelIntegration(model_path="path/to/your/model.gguf")
```

3. Adjust the model parameters in `model_integration.py` as needed

## Project Structure

- `app.py` - Flask application and API endpoints
- `index.html` - Web UI for the application
- `model_integration.py` - Integration with language models
- `requirements.txt` - Python dependencies
- `.devcontainer/` - Configuration for GitHub Codespaces

## Notes on Model Selection

For NSFW story generation, models specifically fine-tuned for creative writing and NSFW content tend to perform best. Some options to consider:

- Kunoichi-7B - Good performance on consumer hardware
- Fimbulvetr-10.7B - Better quality but requires more resources
- Aurelian-70B - High quality but requires significant hardware resources

These models can be found on Hugging Face and other model repositories.

## License

This project is for educational purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations regarding AI-generated content.