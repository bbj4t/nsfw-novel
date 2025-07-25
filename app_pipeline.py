from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from model_integration_pipeline import ModelIntegrationPipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the model with pipeline support (optimized for Pro accounts)
# Set use_pipeline=True for better performance with Hugging Face Pro accounts
model = ModelIntegrationPipeline(
    model_name="UnfilteredAI/NSFW-3B", 
    use_mock=True,  # Set to False to use actual model
    use_pipeline=True  # Use efficient pipeline API
)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate_story():
    """Generate a story based on the provided parameters"""
    try:
        data = request.get_json()
        
        # Extract parameters from request
        prompt = data.get('prompt', '')
        genre = data.get('genre', 'romance')
        length = data.get('length', 'medium')
        temperature = float(data.get('temperature', 0.7))
        
        # Validate inputs
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        if genre not in ['romance', 'fantasy', 'sci-fi', 'contemporary', 'historical']:
            return jsonify({'error': 'Invalid genre'}), 400
        
        if length not in ['short', 'medium', 'long']:
            return jsonify({'error': 'Invalid length'}), 400
        
        if not 0.0 <= temperature <= 1.0:
            return jsonify({'error': 'Temperature must be between 0.0 and 1.0'}), 400
        
        # Generate the story
        story = model.generate_story(prompt, genre, length, temperature)
        
        # Get model info for response
        model_info = model.get_model_info()
        
        return jsonify({
            'story': story,
            'model_info': model_info,
            'parameters': {
                'prompt': prompt,
                'genre': genre,
                'length': length,
                'temperature': temperature
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    model_info = model.get_model_info()
    
    return jsonify({
        'status': 'healthy',
        'model_loaded': not model_info['mock_mode'],
        'model_info': model_info,
        'pipeline_enabled': model_info.get('use_pipeline', False)
    })

@app.route('/api/models')
def list_models():
    """List available models for Pro account users"""
    available_models = [
        {
            'name': 'UnfilteredAI/NSFW-3B',
            'description': 'Default NSFW model, good balance of quality and performance',
            'size': '~3GB',
            'recommended': True
        },
        {
            'name': 'NeverSleep/Noromaid-3B-v0.1.1',
            'description': 'Alternative NSFW-focused model',
            'size': '~3GB',
            'recommended': False
        },
        {
            'name': 'PygmalionAI/pygmalion-6b',
            'description': 'Good for character-based storytelling',
            'size': '~6GB',
            'recommended': False
        },
        {
            'name': 'Undi95/ReMM-NSFW',
            'description': 'Specialized for NSFW content',
            'size': 'Variable',
            'recommended': False
        }
    ]
    
    return jsonify({
        'available_models': available_models,
        'current_model': model.model_name,
        'pro_account_benefits': [
            'Faster model downloads',
            'Priority access during high traffic',
            'Better rate limits',
            'Access to gated models (with approval)',
            'Pipeline API optimizations'
        ]
    })

@app.route('/api/switch-model', methods=['POST'])
def switch_model():
    """Switch to a different model (Pro account feature)"""
    try:
        data = request.get_json()
        new_model_name = data.get('model_name')
        
        if not new_model_name:
            return jsonify({'error': 'model_name is required'}), 400
        
        # Create new model instance
        global model
        model = ModelIntegrationPipeline(
            model_name=new_model_name,
            use_mock=False,  # Try to load actual model
            use_pipeline=True
        )
        
        model_info = model.get_model_info()
        
        return jsonify({
            'message': f'Switched to {new_model_name}',
            'model_info': model_info,
            'success': not model_info['mock_mode']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_model():
    """Optimize model settings for Pro account users"""
    try:
        data = request.get_json()
        optimization_level = data.get('level', 'balanced')  # 'speed', 'balanced', 'quality'
        
        optimizations = {
            'speed': {
                'torch_dtype': 'float16',
                'device_map': 'auto',
                'use_cache': True,
                'low_cpu_mem_usage': True
            },
            'balanced': {
                'torch_dtype': 'float16',
                'device_map': 'auto',
                'use_cache': True
            },
            'quality': {
                'torch_dtype': 'float32',
                'device_map': 'auto',
                'use_cache': False
            }
        }
        
        selected_optimizations = optimizations.get(optimization_level, optimizations['balanced'])
        
        return jsonify({
            'message': f'Optimization level set to {optimization_level}',
            'optimizations': selected_optimizations,
            'note': 'Restart the application to apply optimizations'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=== NSFW Novel Generator - Pipeline Version ===")
    print("Optimized for Hugging Face Pro accounts")
    print(f"Model: {model.model_name}")
    print(f"Pipeline enabled: {model.use_pipeline}")
    print(f"Mock mode: {model.mock_mode}")
    
    model_info = model.get_model_info()
    print(f"Model info: {model_info}")
    
    if model_info['mock_mode']:
        print("\n⚠️  Running in mock mode. To use actual model:")
        print("   1. Set use_mock=False in the ModelIntegrationPipeline initialization")
        print("   2. Ensure you have sufficient GPU memory")
        print("   3. Make sure your Hugging Face token is set (if needed)")
    else:
        print("\n✅ Model loaded successfully!")
        print(f"   Method: {model_info.get('method', 'unknown')}")
        print(f"   Device: {model_info.get('device', 'unknown')}")
    
    print("\n🚀 Pro Account Benefits:")
    print("   - Faster model downloads and loading")
    print("   - Priority access during high traffic")
    print("   - Better rate limits for API calls")
    print("   - Access to gated models (with approval)")
    print("   - Pipeline API optimizations")
    
    print("\nStarting server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)