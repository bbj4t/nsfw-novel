import requests
import json
import time

class CodespacesConnector:
    """
    A class to connect a Kaggle notebook to a running GitHub Codespaces application.
    This allows you to use the GPU-powered model on Kaggle while connecting to the
    full application running in GitHub Codespaces.
    """
    
    def __init__(self, codespaces_url):
        """
        Initialize the connector with the URL of your GitHub Codespaces application.
        
        Args:
            codespaces_url: The public URL of your GitHub Codespaces application
                           (e.g., "https://yourname-yourrepo-x1y2z3.github.dev")
        """
        self.base_url = codespaces_url.rstrip('/')
        self.health_url = f"{self.base_url}/health"
        self.generate_url = f"{self.base_url}/api/generate"
        self.session = requests.Session()
    
    def check_connection(self):
        """
        Check if the connection to the GitHub Codespaces application is working.
        
        Returns:
            dict: The health check response or an error message
        """
        try:
            response = self.session.get(self.health_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}
    
    def generate_story(self, prompt, genre="romance", length="medium", temperature=0.7):
        """
        Generate a story using the GitHub Codespaces application API.
        
        Args:
            prompt (str): The story prompt
            genre (str): The genre of the story (romance, fantasy, sci-fi, contemporary, historical)
            length (str): The desired length (short, medium, long)
            temperature (float): Creativity parameter (0.0 to 1.0)
            
        Returns:
            dict: The generated story or an error message
        """
        payload = {
            "prompt": prompt,
            "genre": genre,
            "length": length,
            "temperature": temperature
        }
        
        try:
            start_time = time.time()
            response = self.session.post(
                self.generate_url, 
                json=payload,
                timeout=60  # Longer timeout for story generation
            )
            response.raise_for_status()
            generation_time = time.time() - start_time
            
            result = response.json()
            result["generation_time"] = generation_time
            return result
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": str(e)}

# Example usage
if __name__ == "__main__":
    # Replace with your actual GitHub Codespaces URL
    connector = CodespacesConnector("https://yourname-nsfw-novel-x1y2z3.github.dev")
    
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