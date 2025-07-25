#!/usr/bin/env python3
"""
Example script showing how to use Hugging Face Transformers Pipeline
with the NSFW Novel Generator - optimized for Pro accounts

This script demonstrates:
1. Using the pipeline API (recommended)
2. Leveraging Pro account benefits
3. Optimized inference settings
4. Error handling and fallbacks
"""

import os
from model_integration_pipeline import ModelIntegrationPipeline

def main():
    print("=== NSFW Novel Generator - Pipeline Example ===")
    print("Optimized for Hugging Face Pro accounts\n")
    
    # Configuration for Pro account users
    # Pro accounts get:
    # - Faster model downloads
    # - Priority access to models
    # - Better rate limits
    # - Access to gated models (if approved)
    
    # Option 1: Use the pipeline approach (RECOMMENDED)
    print("1. Initializing with Pipeline API (recommended for Pro accounts)...")
    model_pipeline = ModelIntegrationPipeline(
        model_name="UnfilteredAI/NSFW-3B",
        use_mock=False,  # Set to True for testing without GPU
        use_pipeline=True  # Use the efficient pipeline API
    )
    
    # Check model info
    info = model_pipeline.get_model_info()
    print(f"Model Info: {info}\n")
    
    if not info['mock_mode']:
        print("✅ Model loaded successfully with pipeline!")
        
        # Test story generation
        print("\n=== Testing Story Generation ===")
        
        test_cases = [
            {
                "prompt": "Two strangers meet at a masquerade ball",
                "genre": "romance",
                "length": "short",
                "temperature": 0.7
            },
            {
                "prompt": "A space explorer discovers an alien artifact",
                "genre": "sci-fi",
                "length": "medium",
                "temperature": 0.8
            }
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\n--- Test Case {i} ---")
            print(f"Prompt: {test['prompt']}")
            print(f"Genre: {test['genre']}, Length: {test['length']}, Temperature: {test['temperature']}")
            
            try:
                story = model_pipeline.generate_story(
                    prompt=test['prompt'],
                    genre=test['genre'],
                    length=test['length'],
                    temperature=test['temperature']
                )
                print(f"\nGenerated Story:\n{story[:200]}...")
                print(f"Story length: {len(story)} characters")
                
            except Exception as e:
                print(f"❌ Error generating story: {e}")
    
    else:
        print("⚠️  Model is in mock mode. Set use_mock=False to use actual model.")
        
        # Show mock story example
        mock_story = model_pipeline.generate_story(
            prompt="Two strangers meet at a coffee shop",
            genre="romance",
            length="short"
        )
        print(f"\nMock Story Example:\n{mock_story[:200]}...")
    
    print("\n=== Pro Account Benefits ===")
    print("""
    With your Hugging Face Pro account, you get:
    
    🚀 Performance Benefits:
    - Faster model downloads and loading
    - Priority access during high traffic
    - Better rate limits for API calls
    
    🔐 Access Benefits:
    - Access to gated models (with approval)
    - Early access to new model releases
    - Premium model variants
    
    💡 Usage Tips:
    - Use pipeline API for better performance
    - Enable device_map="auto" for multi-GPU setups
    - Use torch.float16 for memory efficiency
    - Consider model quantization for even better performance
    """)
    
    print("\n=== Advanced Configuration Options ===")
    print("""
    For Pro users, you can also try:
    
    1. Different models:
       - "NeverSleep/Noromaid-3B-v0.1.1"
       - "PygmalionAI/pygmalion-6b"
       - "Undi95/ReMM-NSFW"
    
    2. Quantization for better performance:
       from transformers import BitsAndBytesConfig
       quantization_config = BitsAndBytesConfig(
           load_in_4bit=True,
           bnb_4bit_compute_dtype=torch.float16
       )
    
    3. Custom generation parameters:
       - temperature: 0.1-1.0 (creativity)
       - top_p: 0.1-1.0 (nucleus sampling)
       - top_k: 1-100 (top-k sampling)
       - repetition_penalty: 1.0-1.2 (avoid repetition)
    """)

def test_different_models():
    """
    Example of testing different models available to Pro users
    """
    models_to_test = [
        "UnfilteredAI/NSFW-3B",
        "NeverSleep/Noromaid-3B-v0.1.1",
        # Add more models as needed
    ]
    
    for model_name in models_to_test:
        print(f"\n=== Testing {model_name} ===")
        try:
            model = ModelIntegrationPipeline(
                model_name=model_name,
                use_mock=False,
                use_pipeline=True
            )
            
            info = model.get_model_info()
            if not info['mock_mode']:
                print(f"✅ {model_name} loaded successfully")
                
                # Quick test
                story = model.generate_story(
                    prompt="A quick test",
                    genre="romance",
                    length="short",
                    temperature=0.7
                )
                print(f"Sample output: {story[:100]}...")
            else:
                print(f"❌ Failed to load {model_name}")
                
        except Exception as e:
            print(f"❌ Error with {model_name}: {e}")

if __name__ == "__main__":
    # Set your Hugging Face token if needed
    # os.environ["HUGGINGFACE_HUB_TOKEN"] = "your_token_here"
    
    main()
    
    # Uncomment to test different models
    # test_different_models()