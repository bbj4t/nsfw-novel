import gradio as gr
import os
import torch
from model_integration_pipeline import ModelIntegrationPipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the model with pipeline support
logger.info("Initializing model...")
model = ModelIntegrationPipeline(
    model_name="UnfilteredAI/NSFW-3B",
    use_mock=False,  # Try to use actual model in Spaces
    use_pipeline=True,  # Use efficient pipeline API
    device="auto"  # Let it auto-detect GPU/CPU
)

def generate_story(prompt, genre, length, temperature, top_p, max_tokens):
    """Generate a story using the model"""
    try:
        if not prompt.strip():
            return "Please provide a prompt to generate a story.", get_model_status()
        
        # Generate the story
        story = model.generate_story(
            prompt=prompt,
            genre=genre,
            length=length,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
        
        # Get model info
        model_info = model.get_model_info()
        status = f"Model: {model_info['model_name']} | Method: {model_info.get('method', 'Unknown')} | Device: {model_info.get('device', 'Unknown')}"
        
        return story, status
        
    except Exception as e:
        logger.error(f"Error generating story: {str(e)}")
        return f"Error: {str(e)}", "Error occurred"

def get_model_status():
    """Get current model status"""
    try:
        model_info = model.get_model_info()
        if model_info['mock_mode']:
            return "⚠️ Running in mock mode - Install model for actual generation"
        else:
            return f"✅ Model loaded: {model_info['model_name']} on {model_info.get('device', 'unknown')}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Define the Gradio interface
with gr.Blocks(title="NSFW Novel Generator", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 📚 NSFW Novel Generator
        
        Generate creative stories using the UnfilteredAI/NSFW-3B model with Hugging Face Pipeline optimization.
        
        **⚠️ Content Warning**: This application generates adult content. Use responsibly.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            # Input controls
            prompt_input = gr.Textbox(
                label="Story Prompt",
                placeholder="Enter your story prompt here... (e.g., 'A romantic evening in Paris')",
                lines=3,
                max_lines=5
            )
            
            with gr.Row():
                genre_input = gr.Dropdown(
                    choices=["romance", "fantasy", "sci-fi", "contemporary", "historical"],
                    value="romance",
                    label="Genre"
                )
                
                length_input = gr.Dropdown(
                    choices=["short", "medium", "long"],
                    value="medium",
                    label="Length"
                )
            
            with gr.Row():
                temperature_input = gr.Slider(
                    minimum=0.1,
                    maximum=1.0,
                    value=0.7,
                    step=0.1,
                    label="Temperature (Creativity)"
                )
                
                top_p_input = gr.Slider(
                    minimum=0.1,
                    maximum=1.0,
                    value=0.9,
                    step=0.1,
                    label="Top-p (Diversity)"
                )
            
            max_tokens_input = gr.Slider(
                minimum=50,
                maximum=500,
                value=200,
                step=50,
                label="Max Tokens"
            )
            
            generate_btn = gr.Button("🎭 Generate Story", variant="primary", size="lg")
            
        with gr.Column(scale=3):
            # Output area
            story_output = gr.Textbox(
                label="Generated Story",
                lines=15,
                max_lines=20,
                show_copy_button=True
            )
            
            status_output = gr.Textbox(
                label="Model Status",
                value=get_model_status(),
                interactive=False
            )
    
    # Examples section
    gr.Markdown("## 💡 Example Prompts")
    
    examples = gr.Examples(
        examples=[
            ["A mysterious stranger enters a cozy bookshop on a rainy evening", "romance", "medium", 0.7, 0.9, 200],
            ["In a world where magic is forbidden, a young mage discovers their powers", "fantasy", "long", 0.8, 0.9, 300],
            ["Two rival scientists are forced to work together on a space station", "sci-fi", "medium", 0.6, 0.8, 250],
            ["A chance encounter at a coffee shop changes everything", "contemporary", "short", 0.7, 0.9, 150],
            ["A forbidden romance blooms in Victorian London", "historical", "medium", 0.8, 0.9, 200]
        ],
        inputs=[prompt_input, genre_input, length_input, temperature_input, top_p_input, max_tokens_input],
        outputs=[story_output, status_output],
        fn=generate_story,
        cache_examples=False
    )
    
    # Information section
    with gr.Accordion("ℹ️ About This Application", open=False):
        gr.Markdown(
            """
            ### Model Information
            - **Model**: UnfilteredAI/NSFW-3B
            - **Method**: Hugging Face Transformers Pipeline
            - **Optimization**: Automatic device mapping and memory management
            
            ### Parameters Guide
            - **Temperature**: Controls randomness (0.1 = conservative, 1.0 = creative)
            - **Top-p**: Controls diversity (0.1 = focused, 1.0 = diverse)
            - **Max Tokens**: Maximum length of generated text
            
            ### Usage Tips
            1. Start with clear, descriptive prompts
            2. Experiment with different temperature settings
            3. Use genre selection to guide the style
            4. Adjust length based on your needs
            
            ### Technical Details
            - Powered by Hugging Face Transformers
            - Optimized for GPU acceleration when available
            - Automatic fallback to CPU if needed
            - Pipeline API for efficient inference
            """
        )
    
    # Event handlers
    generate_btn.click(
        fn=generate_story,
        inputs=[prompt_input, genre_input, length_input, temperature_input, top_p_input, max_tokens_input],
        outputs=[story_output, status_output],
        show_progress=True
    )
    
    # Auto-update status on load
    demo.load(fn=get_model_status, outputs=status_output)

# Launch configuration for Hugging Face Spaces
if __name__ == "__main__":
    logger.info("Starting NSFW Novel Generator for Hugging Face Spaces")
    logger.info(f"Model status: {get_model_status()}")
    
    # Launch the app
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Spaces handles sharing
        show_error=True,
        show_tips=True,
        enable_queue=True,  # Enable queue for better performance
        max_threads=10  # Limit concurrent requests
    )