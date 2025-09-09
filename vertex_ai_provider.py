"""
Vertex AI provider implementation for Dify.ai with Hebrew support.

This module provides integration with Google Cloud Vertex AI using Gemini models
with specific support for Hebrew language and RTL text processing.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Union
from google.cloud import aiplatform
from google.oauth2 import service_account
import vertexai
from vertexai.generative_models import GenerativeModel, Part

logger = logging.getLogger(__name__)


class VertexAIProvider:
    """
    Google Cloud Vertex AI provider for Dify.ai with Hebrew language support.
    
    Supports Gemini Pro and Gemini Flash models with Hebrew RTL text processing.
    """
    
    def __init__(self, project_id: str, location: str = "us-east1", credentials_path: Optional[str] = None):
        """
        Initialize Vertex AI provider.
        
        Args:
            project_id: GCP project ID
            location: GCP region (default: us-east1)
            credentials_path: Path to service account JSON file (optional)
        """
        self.project_id = project_id
        self.location = location
        
        # Initialize Vertex AI
        if credentials_path:
            credentials = service_account.Credentials.from_service_account_file(credentials_path)
            vertexai.init(project=project_id, location=location, credentials=credentials)
        else:
            # Use Application Default Credentials (ADC)
            vertexai.init(project=project_id, location=location)
        
        # Available models
        self.available_models = {
            "gemini-pro": {
                "name": "Gemini Pro",
                "model_id": "gemini-1.5-pro",
                "max_tokens": 8192,
                "supports_hebrew": True,
                "description": "Advanced multimodal model with Hebrew RTL support"
            },
            "gemini-flash": {
                "name": "Gemini Flash", 
                "model_id": "gemini-1.5-flash",
                "max_tokens": 8192,
                "supports_hebrew": True,
                "description": "Fast, efficient model optimized for Hebrew conversations"
            }
        }
        
        logger.info(f"Vertex AI provider initialized for project {project_id} in {location}")
    
    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        """Get list of available models."""
        return self.available_models
    
    def _prepare_hebrew_prompt(self, prompt: str) -> str:
        """
        Prepare prompt for Hebrew language processing.
        
        Args:
            prompt: Input prompt text
            
        Returns:
            Enhanced prompt with Hebrew language instructions
        """
        hebrew_instructions = """אנא השב בעברית בצורה ברורה ומדויקת. 
שים לב לכיווניות הטקסט (RTL) ולתקינות הדקדוק העברי.
"""
        
        # Check if prompt already contains Hebrew
        has_hebrew = any('\u0590' <= char <= '\u05FF' for char in prompt)
        
        if has_hebrew:
            return f"{hebrew_instructions}\n\n{prompt}"
        else:
            # For English prompts, add Hebrew response instruction
            return f"{prompt}\n\n{hebrew_instructions}"
    
    def generate_response(
        self, 
        prompt: str, 
        model_name: str = "gemini-pro",
        max_tokens: int = 1024,
        temperature: float = 0.7,
        enable_hebrew: bool = True
    ) -> Dict[str, Any]:
        """
        Generate response using Vertex AI Gemini models.
        
        Args:
            prompt: Input prompt
            model_name: Model to use (gemini-pro or gemini-flash)
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0.0-1.0)
            enable_hebrew: Whether to optimize for Hebrew language
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            if model_name not in self.available_models:
                raise ValueError(f"Model {model_name} not available. Choose from: {list(self.available_models.keys())}")
            
            model_config = self.available_models[model_name]
            model_id = model_config["model_id"]
            
            # Initialize the model
            model = GenerativeModel(model_id)
            
            # Prepare prompt for Hebrew if enabled
            if enable_hebrew:
                enhanced_prompt = self._prepare_hebrew_prompt(prompt)
            else:
                enhanced_prompt = prompt
            
            # Generation configuration
            generation_config = {
                "max_output_tokens": min(max_tokens, model_config["max_tokens"]),
                "temperature": temperature,
                "top_p": 0.95,
                "top_k": 40
            }
            
            # Generate response
            response = model.generate_content(
                enhanced_prompt,
                generation_config=generation_config
            )
            
            # Extract response text
            response_text = response.text if response.text else ""
            
            return {
                "success": True,
                "response": response_text,
                "model": model_name,
                "model_id": model_id,
                "tokens_used": len(response_text.split()) if response_text else 0,
                "supports_hebrew": model_config["supports_hebrew"],
                "metadata": {
                    "project_id": self.project_id,
                    "location": self.location,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "model": model_name,
                "response": None
            }
    
    def test_hebrew_capabilities(self) -> Dict[str, Any]:
        """
        Test Hebrew language capabilities of the provider.
        
        Returns:
            Test results with Hebrew processing validation
        """
        hebrew_test_prompt = "בדוק את יכולות העיבוד שלך בעברית. ספר לי על היתרונות של בינה מלאכותית."
        
        test_results = {}
        
        for model_name in self.available_models.keys():
            logger.info(f"Testing Hebrew capabilities for {model_name}")
            
            result = self.generate_response(
                prompt=hebrew_test_prompt,
                model_name=model_name,
                max_tokens=200,
                enable_hebrew=True
            )
            
            test_results[model_name] = {
                "success": result["success"],
                "has_hebrew_response": self._contains_hebrew(result.get("response", "")),
                "response_length": len(result.get("response", "")),
                "error": result.get("error")
            }
        
        return test_results
    
    def _contains_hebrew(self, text: str) -> bool:
        """Check if text contains Hebrew characters."""
        return any('\u0590' <= char <= '\u05FF' for char in text)
    
    def validate_configuration(self) -> Dict[str, Any]:
        """
        Validate Vertex AI configuration and credentials.
        
        Returns:
            Validation results
        """
        try:
            # Test basic API access
            client = aiplatform.gapic.ModelServiceClient(
                client_options={"api_endpoint": f"{self.location}-aiplatform.googleapis.com"}
            )
            
            # Try to list models (basic permission test)
            parent = f"projects/{self.project_id}/locations/{self.location}"
            
            return {
                "success": True,
                "project_id": self.project_id,
                "location": self.location,
                "available_models": list(self.available_models.keys()),
                "status": "Vertex AI configuration is valid"
            }
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "status": "Vertex AI configuration failed"
            }


def create_vertex_ai_provider(
    project_id: str, 
    location: str = "us-east1", 
    credentials_path: Optional[str] = None
) -> VertexAIProvider:
    """
    Factory function to create Vertex AI provider instance.
    
    Args:
        project_id: GCP project ID
        location: GCP region
        credentials_path: Path to service account JSON file
        
    Returns:
        VertexAIProvider instance
    """
    return VertexAIProvider(project_id, location, credentials_path)


# Example usage and testing
if __name__ == "__main__":
    import os
    
    # Configuration (would come from environment variables in production)
    PROJECT_ID = os.getenv("GOOGLE_VERTEX_PROJECT", "lionspace")
    LOCATION = os.getenv("GOOGLE_VERTEX_LOCATION", "us-east1")
    CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # Initialize provider
    provider = create_vertex_ai_provider(PROJECT_ID, LOCATION, CREDENTIALS_PATH)
    
    # Validate configuration
    validation = provider.validate_configuration()
    print("Configuration validation:", json.dumps(validation, indent=2, ensure_ascii=False))
    
    # Test Hebrew capabilities
    if validation["success"]:
        hebrew_test = provider.test_hebrew_capabilities()
        print("Hebrew capabilities test:", json.dumps(hebrew_test, indent=2, ensure_ascii=False))
        
        # Example conversation
        test_prompt = "מה זה Dify.ai ואיך זה עובד?"
        response = provider.generate_response(
            prompt=test_prompt,
            model_name="gemini-flash",
            max_tokens=500
        )
        print("Example response:", json.dumps(response, indent=2, ensure_ascii=False))