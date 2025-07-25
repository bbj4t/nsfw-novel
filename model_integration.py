import os
import json
import numpy as np
from typing import Dict, Any, Optional, List

# This file provides the integration point for connecting to LLMs
# Using Hugging Face Transformers with UnfilteredAI/NSFW-3B model

class ModelIntegration:
    def __init__(self, model_name: str = "UnfilteredAI/NSFW-3B", use_mock: bool = False):
        """
        Initialize the model integration.
        
        Args:
            model_name: Name of the Hugging Face model to use. Default is "UnfilteredAI/NSFW-3B".
            use_mock: If True, will use mock responses instead of loading the model.
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.mock_mode = use_mock
        
        # If not in mock mode, try to load the model
        if not self.mock_mode:
            try:
                self._load_model()
            except Exception as e:
                print(f"Error loading model: {e}")
                print("Falling back to mock mode")
                self.mock_mode = True
    
    def _load_model(self):
        """
        Load the LLM model using Hugging Face Transformers.
        """
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            import torch
            
            print(f"Loading model {self.model_name} from Hugging Face...")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,  # Use half-precision to reduce memory usage
                device_map="auto"  # Automatically determine the best device configuration
            )
            
            print(f"Successfully loaded {self.model_name}")
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")

    
    def generate_story(self, prompt: str, genre: str, length: str, temperature: float = 0.7) -> str:
        """
        Generate a story based on the given parameters.
        
        Args:
            prompt: The story prompt
            genre: The genre of the story
            length: The desired length (short, medium, long)
            temperature: Creativity parameter (0.0 to 1.0)
            
        Returns:
            The generated story text
        """
        if self.mock_mode:
            return self._generate_mock_story(prompt, genre, length)
        else:
            return self._generate_with_model(prompt, genre, length, temperature)
    
    def _generate_with_model(self, prompt: str, genre: str, length: str, temperature: float) -> str:
        """
        Generate a story using the loaded Hugging Face Transformers model.
        """
        import torch
        
        # Map length to approximate token counts
        length_to_tokens = {
            "short": 512,
            "medium": 1024,
            "long": 2048
        }
        max_tokens = length_to_tokens.get(length, 1024)
        
        # Create a system prompt that guides the model
        system_prompt = f"You are an expert writer of {genre} NSFW stories. "
        system_prompt += f"Write a {length} story based on the following prompt: {prompt}\n\n"
        
        # Tokenize the input
        inputs = self.tokenizer(system_prompt, return_tensors="pt").to(self.model.device)
        
        # Generate the story
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode the generated text
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the prompt from the generated text
        story = generated_text[len(system_prompt):].strip()
        
        return story
    
    def _generate_mock_story(self, prompt: str, genre: str, length: str) -> str:
        """
        Generate a mock story for testing purposes.
        """
        stories = {
            'romance': f"The moonlight filtered through the ancient oak trees, casting dancing shadows on the garden path. {prompt} as they found themselves alone in this secluded paradise.\n\nTheir hearts raced as they drew closer, the scent of jasmine filling the air. His fingers gently traced her cheek, feeling the softness of her skin under the silver light. She leaned into his touch, her breath catching as his lips found hers.\n\nThe kiss deepened, filled with weeks of unspoken desire. Her hands moved to his chest, feeling the steady rhythm of his heartbeat. He pulled her closer, his hands exploring the curve of her back as passion ignited between them.\n\nTime seemed to stand still in the moonlit garden, where two souls connected in the most intimate way, their love story unfolding under the watchful eyes of the stars.",
            
            'fantasy': f"In the mystical realm of Aethermoor, {prompt} took place in an enchanted grove where ancient magic flowed through the very air.\n\nThe sorceress felt the power surge through her veins as she cast the spell of binding. The warrior's eyes glowed with otherworldly energy as he responded to her magical touch. Runes carved into the ancient stones began to pulse with ethereal light.\n\nTheir connection transcended the physical realm, merging their souls in a dance of arcane energy. The magic intensified, wrapping around them like a cocoon of pure desire. As the spell reached its crescendo, reality itself seemed to bend to their will.\n\nIn this sacred place where magic and passion intertwined, they became one with the ancient forces that governed their world, their union echoing through the mystical planes for eternity.",
            
            "sci-fi": f"Aboard the starship Nebula, {prompt} occurred in the zero-gravity observation deck as they drifted among the stars.\n\nThe advanced neural interface pulsed with energy as their minds connected through the quantum link. Her enhanced senses detected his arousal through bio-scans, while his cybernetic implants responded to her pheromones.\n\nIn the weightless environment, their movements became a graceful ballet of desire. The holographic displays around them flickered as their passion overloaded the ship's sensors. His synthetic skin, designed to mimic human touch, traced patterns across her genetically enhanced form.\n\nAs they reached climax, the artificial gravity briefly malfunctioned, sending waves of pleasure through their enhanced nervous systems. Their union was recorded in the ship's quantum logs as a perfect harmony of human emotion and technological evolution.",
            
            'contemporary': f"In the heart of the city, {prompt} unfolded in a rooftop garden hidden above the bustling streets below.\n\nThe sounds of traffic faded into the background as they found their own private world among the potted plants and string lights. Her fingers worked quickly at the buttons of his shirt, revealing the toned chest beneath.\n\nHe lifted her effortlessly onto the wrought iron table, her legs wrapping around his waist as their lips met hungrily. The cool metal beneath her back contrasted with the heat of his body pressing against hers.\n\nCity lights twinkled around them like distant stars as they explored each other with desperate need. In this secret sanctuary high above the world, they found a moment of pure connection away from the chaos of modern life.",
            
            'historical': f"In the candlelit chambers of the medieval castle, {prompt} transpired during a secret rendezvous between a noble lady and her forbidden lover.\n\nThe tapestries on the stone walls seemed to watch as they embraced with the passion of those who knew their time together was fleeting. Her silk gown pooled around her feet as he lifted her onto the canopied bed.\n\nThe flickering candlelight cast shadows across his face as he kissed her neck, his hands exploring the curves hidden beneath layers of period clothing. She gasped as his fingers found their way past the intricate laces of her bodice.\n\nIn an era where such liaisons could mean death, their love was all the more intense. The heavy wooden door creaked slightly in the night breeze as they lost themselves in each other, knowing that dawn would bring the harsh reality of their separate worlds."
        }
        
        story = stories.get(genre, stories['romance'])
        
        # Adjust length
        if length == 'short':
            paragraphs = story.split('\n\n')
            if len(paragraphs) > 2:
                story = paragraphs[0] + '\n\n' + paragraphs[1]
        elif length == 'long':
            story += '\n\n' + story.replace('their', 'the lovers\'').replace('they', 'the couple')
        
        return story