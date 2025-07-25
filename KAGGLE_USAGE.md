# Running NSFW-3B Model on Kaggle

This guide explains how to run the UnfilteredAI/NSFW-3B model on Kaggle's free GPU tier and how to connect it to your GitHub Codespaces application.

## Why Use Kaggle?

Kaggle offers free GPU resources that are perfect for running the NSFW-3B model:

- **Free T4 GPU** with approximately 16GB VRAM (the NSFW-3B model requires about 10.6GB)
- **30 hours per week** of free GPU usage
- **Python notebook environment** with pre-installed ML libraries
- **No credit card required** for GPU access

## Option 1: Standalone Model Testing on Kaggle

Use the provided `kaggle_notebook_template.ipynb` notebook to run the model directly on Kaggle:

### Step 1: Set Up Your Kaggle Environment

1. Create a free Kaggle account at [kaggle.com](https://www.kaggle.com) if you don't have one
2. Go to "Code" > "New Notebook" to create a new notebook
3. Upload the `kaggle_notebook_template.ipynb` file or copy its contents

### Step 2: Configure GPU and Internet Access

1. Click on the "..." menu in the top-right corner
2. Select "Settings"
3. Under "Accelerator", select "GPU T4 x1"
4. Enable "Internet" under the Internet section
5. Click "Save"

### Step 3: Run the Notebook

1. Run the notebook cells sequentially
2. The model will be downloaded from Hugging Face and loaded into GPU memory
3. Use the interactive UI to test different story generation parameters

### Key Features of the Notebook Template

- Loads the UnfilteredAI/NSFW-3B model using Hugging Face Transformers
- Implements the same `ModelIntegration` class used in the main application
- Provides an interactive UI for testing different story generation parameters
- Includes memory management techniques for optimizing GPU usage

## Option 2: Create an API Server on Kaggle

If you want to use Kaggle's GPU for model inference while accessing it from other applications, you can set up an API server using the provided `kaggle_api_notebook.ipynb`:

### Step 1: Set Up the API Server on Kaggle

1. Create a new Kaggle notebook
2. Upload the `kaggle_api_notebook.ipynb` file or copy its contents
3. Configure GPU and internet access as described in Option 1
4. Sign up for a free [ngrok](https://ngrok.com) account and get your authtoken
5. Update the ngrok authtoken in the notebook:
   ```python
   ngrok.set_auth_token("YOUR_AUTHTOKEN")
   ```
6. Run the notebook cells to start the Flask API server and expose it via ngrok
7. Copy the public ngrok URL that is displayed (e.g., `https://a1b2c3d4.ngrok.io`)

### Step 2: Connect to the API from Your Application

You can now connect to this API from any application. To use it with this project:

1. Modify the `app.py` file to use the `KaggleModelConnector` class instead of the local model:

```python
# Add this import at the top of app.py
import requests

class KaggleModelConnector:
    def __init__(self, api_url):
        self.api_url = api_url
        self.mock_mode = False
        
    def generate_story(self, prompt, genre, length, temperature):
        payload = {
            "prompt": prompt,
            "genre": genre,
            "length": length,
            "temperature": temperature
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result.get('story', 'Error generating story')
        except Exception as e:
            print(f"Error connecting to Kaggle API: {e}")
            # Fall back to mock mode if API is unavailable
            self.mock_mode = True
            return "API connection error. Falling back to mock mode."

# Replace the model initialization
# model = ModelIntegration(model_name="UnfilteredAI/NSFW-3B", use_mock=True)

# With this:
kaggle_api_url = "https://YOUR-NGROK-URL.ngrok.io/api/generate"  # Replace with your actual ngrok URL
model = KaggleModelConnector(kaggle_api_url)
```

## Option 3: Connect GitHub Codespaces to Kaggle

If you're using GitHub Codespaces for your application but want to leverage Kaggle's GPU for model inference:

### Step 1: Make Your GitHub Codespaces Application Accessible

1. In GitHub Codespaces, make sure your application is running (`python app.py`)
2. Set the port visibility to "Public" (right-click on the port in the PORTS tab)
3. Copy the public URL (e.g., `https://yourname-nsfw-novel-x1y2z3.github.dev`)

### Step 2: Use the API Connector in Kaggle

1. Create a new Kaggle notebook
2. Copy the contents of `kaggle_api_connector.py` into a code cell
3. Update the `CodespacesConnector` initialization with your Codespaces URL:

```python
connector = CodespacesConnector("https://yourname-nsfw-novel-x1y2z3.github.dev")
```

4. Test the connection and generate stories through the API:

```python
# Check connection
health = connector.check_connection()
print(f"Connection status: {health}")

# Generate a story
if health.get("status") == "healthy":
    story_result = connector.generate_story(
        prompt="Two strangers meet at a masquerade ball",
        genre="romance",
        length="short",
        temperature=0.7
    )
    
    if story_result.get("status") == "success":
        print(f"\nGenerated in {story_result.get('generation_time', 0):.2f} seconds:\n")
        print(story_result.get("story", "No story generated"))
    else:
        print(f"Error: {story_result.get('message')}")
```

## Memory Management Tips

- The NSFW-3B model requires approximately 10.6GB of VRAM
- Kaggle's T4 GPU has around 16GB of VRAM, which is sufficient
- The code already uses half-precision (float16) to reduce memory usage
- To free up GPU memory when needed, add this code:
  ```python
  import torch
  torch.cuda.empty_cache()
  ```
- Monitor memory usage with:
  ```python
  print(f"GPU memory allocated: {torch.cuda.memory_allocated() / 1024**3:.2f} GB")
  print(f"GPU memory reserved: {torch.cuda.memory_reserved() / 1024**3:.2f} GB")
  ```

## Important Limitations

### Time Limitations

- Kaggle's free tier limits GPU usage to **30 hours per week**
- Notebooks will automatically terminate after 12 hours of inactivity
- Save your work frequently to avoid losing progress

### API Limitations

- The ngrok free tier has limitations on connections and bandwidth
- The ngrok URL will change each time you restart the notebook
- For persistent API access, consider upgrading to a paid ngrok plan

## Troubleshooting

### Common Issues

1. **Out of Memory Errors**: 
   - Try reducing batch size or max_tokens in the generation parameters
   - Restart the kernel to clear GPU memory
   - Use `torch.cuda.empty_cache()` to free up memory

2. **Connection Errors**: 
   - Ensure your ngrok authtoken is correct
   - Check that your GitHub Codespaces URL is correct and the port is set to public
   - Verify that your Kaggle notebook has internet access enabled

3. **Model Loading Failures**: 
   - Check that you have internet access enabled in your Kaggle notebook
   - Ensure you have enough GPU memory available
   - Try restarting the kernel and running the cells again

4. **Slow Generation Times**:
   - The first generation after loading the model is typically slower
   - Subsequent generations should be faster as the model is cached
   - Consider reducing the max_tokens parameter for faster generation

## Additional Resources

- [Hugging Face Model Card for UnfilteredAI/NSFW-3B](https://huggingface.co/UnfilteredAI/NSFW-3B)
- [Kaggle Documentation on GPU Usage](https://www.kaggle.com/docs/efficient-gpu-usage)
- [Transformers Documentation](https://huggingface.co/docs/transformers/index)
- [ngrok Documentation](https://ngrok.com/docs)
- [Flask API Documentation](https://flask.palletsprojects.com/)