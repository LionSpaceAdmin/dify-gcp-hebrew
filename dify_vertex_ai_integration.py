"""
Dify.ai Vertex AI Integration Module

This module provides a complete integration between Dify.ai and Google Cloud Vertex AI,
following Dify's model provider architecture and supporting Hebrew language processing.
"""

import os
import json
import logging
from typing import Any, Dict, List, Optional, Generator
from dataclasses import dataclass
from vertex_ai_provider import VertexAIProvider

logger = logging.getLogger(__name__)


@dataclass
class DifyModelConfig:
    """Configuration for Dify model integration."""
    provider_name: str
    model_name: str
    model_type: str
    credentials: Dict[str, Any]
    parameters: Dict[str, Any]


class DifyVertexAIIntegration:
    """
    Integration layer between Dify.ai and Vertex AI provider.
    
    This class implements the interface expected by Dify's model runtime system
    while providing Hebrew language support and RTL text processing.
    """
    
    def __init__(self):
        """Initialize the Dify Vertex AI integration."""
        self.provider_name = "vertex_ai"
        self.supported_model_types = ["llm", "chat", "text-generation"]
        self.vertex_provider: Optional[VertexAIProvider] = None
        
        # Model configurations for Dify
        self.model_configs = {
            "gemini-pro": {
                "model_name": "gemini-pro",
                "model_type": "llm",
                "mode": "chat",
                "context_size": 30720,
                "max_chunks": 1,
                "chunk_size": 4000,
                "credentials": ["project_id", "location", "service_account_key"],
                "parameters": {
                    "temperature": {"type": "float", "min": 0.0, "max": 1.0, "default": 0.7},
                    "max_tokens": {"type": "int", "min": 1, "max": 8192, "default": 1024},
                    "top_p": {"type": "float", "min": 0.0, "max": 1.0, "default": 0.95},
                    "top_k": {"type": "int", "min": 1, "max": 100, "default": 40}
                }
            },
            "gemini-flash": {
                "model_name": "gemini-flash",
                "model_type": "llm",
                "mode": "chat",
                "context_size": 30720,
                "max_chunks": 1,
                "chunk_size": 4000,
                "credentials": ["project_id", "location", "service_account_key"],
                "parameters": {
                    "temperature": {"type": "float", "min": 0.0, "max": 1.0, "default": 0.3},
                    "max_tokens": {"type": "int", "min": 1, "max": 8192, "default": 1024},
                    "top_p": {"type": "float", "min": 0.0, "max": 1.0, "default": 0.95},
                    "top_k": {"type": "int", "min": 1, "max": 100, "default": 40}
                }
            }
        }
    
    def initialize_provider(self, credentials: Dict[str, Any]) -> bool:
        """
        Initialize the Vertex AI provider with credentials.
        
        Args:
            credentials: Dictionary containing GCP credentials
            
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            project_id = credentials.get("project_id")
            location = credentials.get("location", "us-east1")
            service_account_key = credentials.get("service_account_key")
            
            if not project_id:
                raise ValueError("project_id is required")
            
            # Handle service account key
            credentials_path = None
            if service_account_key:
                # If it's a JSON string, write to temp file
                if isinstance(service_account_key, str) and service_account_key.startswith('{'):
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                        f.write(service_account_key)
                        credentials_path = f.name
                else:
                    credentials_path = service_account_key
            
            self.vertex_provider = VertexAIProvider(
                project_id=project_id,
                location=location,
                credentials_path=credentials_path
            )
            
            # Validate the provider
            validation = self.vertex_provider.validate_configuration()
            if not validation["success"]:
                logger.error(f"Vertex AI provider validation failed: {validation['error']}")
                return False
            
            logger.info("Vertex AI provider initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Vertex AI provider: {str(e)}")
            return False
    
    def get_provider_schema(self) -> Dict[str, Any]:
        """
        Get the provider schema for Dify configuration.
        
        Returns:
            Provider schema dictionary
        """
        return {
            "provider": self.provider_name,
            "label": {
                "en_US": "Google Vertex AI",
                "he": "Google Vertex AI"
            },
            "description": {
                "en_US": "Google Cloud Vertex AI with Gemini models and Hebrew support",
                "he": "Google Cloud Vertex AI עם מודלי Gemini ותמיכה בעברית"
            },
            "icon_small": {
                "en_US": "google.svg",
                "he": "google.svg"
            },
            "icon_large": {
                "en_US": "google.svg",
                "he": "google.svg"
            },
            "supported_model_types": self.supported_model_types,
            "configurate_methods": ["predefined-model"],
            "provider_credential_schema": {
                "credential_form_schemas": [
                    {
                        "variable": "project_id",
                        "label": {
                            "en_US": "GCP Project ID",
                            "he": "מזהה פרויקט GCP"
                        },
                        "type": "text-input",
                        "required": True,
                        "placeholder": {
                            "en_US": "Enter your GCP project ID",
                            "he": "הכנס את מזהה הפרויקט שלך ב-GCP"
                        }
                    },
                    {
                        "variable": "location",
                        "label": {
                            "en_US": "Region",
                            "he": "אזור"
                        },
                        "type": "text-input",
                        "required": False,
                        "default": "us-east1",
                        "placeholder": {
                            "en_US": "GCP region (default: us-east1)",
                            "he": "אזור GCP (ברירת מחדל: us-east1)"
                        }
                    },
                    {
                        "variable": "service_account_key",
                        "label": {
                            "en_US": "Service Account Key",
                            "he": "מפתח חשבון שירות"
                        },
                        "type": "secret-input",
                        "required": False,
                        "placeholder": {
                            "en_US": "Service account JSON key or file path",
                            "he": "מפתח JSON של חשבון שירות או נתיב קובץ"
                        }
                    }
                ]
            }
        }
    
    def get_model_schemas(self) -> List[Dict[str, Any]]:
        """
        Get model schemas for all supported models.
        
        Returns:
            List of model schema dictionaries
        """
        schemas = []
        
        for model_name, config in self.model_configs.items():
            schema = {
                "model": model_name,
                "label": {
                    "en_US": config["model_name"].title(),
                    "he": config["model_name"].title()
                },
                "model_type": config["model_type"],
                "features": ["agent-thought", "stream-tool-call"],
                "fetch_from": "predefined-model",
                "model_properties": {
                    "context_size": config["context_size"],
                    "max_chunks": config["max_chunks"],
                    "chunk_size": config["chunk_size"],
                    "mode": config["mode"]
                },
                "parameter_rules": []
            }
            
            # Add parameter rules
            for param_name, param_config in config["parameters"].items():
                rule = {
                    "name": param_name,
                    "use_template": param_name,
                    "label": {
                        "en_US": param_name.replace('_', ' ').title(),
                        "he": param_name.replace('_', ' ').title()
                    },
                    "type": param_config["type"],
                    "default": param_config["default"]
                }
                
                if "min" in param_config:
                    rule["min"] = param_config["min"]
                if "max" in param_config:
                    rule["max"] = param_config["max"]
                
                schema["parameter_rules"].append(rule)
            
            schemas.append(schema)
        
        return schemas
    
    def generate_response(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        parameters: Dict[str, Any],
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Generate response using Vertex AI.
        
        Args:
            model: Model name
            messages: List of message dictionaries
            parameters: Generation parameters
            stream: Whether to stream the response
            
        Returns:
            Response dictionary or generator if streaming
        """
        if not self.vertex_provider:
            raise RuntimeError("Vertex AI provider not initialized")
        
        if model not in self.model_configs:
            raise ValueError(f"Model {model} not supported")
        
        # Convert messages to prompt
        prompt = self._messages_to_prompt(messages)
        
        # Extract parameters
        temperature = parameters.get("temperature", 0.7)
        max_tokens = parameters.get("max_tokens", 1024)
        
        # Generate response
        response = self.vertex_provider.generate_response(
            prompt=prompt,
            model_name=model,
            max_tokens=max_tokens,
            temperature=temperature,
            enable_hebrew=True
        )
        
        if not response["success"]:
            raise RuntimeError(f"Generation failed: {response['error']}")
        
        return {
            "model": model,
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": response["tokens_used"],
                "total_tokens": len(prompt.split()) + response["tokens_used"]
            },
            "message": {
                "role": "assistant",
                "content": response["response"]
            }
        }
    
    def _messages_to_prompt(self, messages: List[Dict[str, Any]]) -> str:
        """
        Convert Dify message format to prompt string.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Formatted prompt string
        """
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        return "\n\n".join(prompt_parts)
    
    def validate_credentials(self, credentials: Dict[str, Any]) -> bool:
        """
        Validate provider credentials.
        
        Args:
            credentials: Credentials dictionary
            
        Returns:
            True if valid, False otherwise
        """
        return self.initialize_provider(credentials)
    
    def test_hebrew_integration(self) -> Dict[str, Any]:
        """
        Test Hebrew language integration.
        
        Returns:
            Test results
        """
        if not self.vertex_provider:
            return {"success": False, "error": "Provider not initialized"}
        
        # Test Hebrew capabilities
        hebrew_test = self.vertex_provider.test_hebrew_capabilities()
        
        # Test Dify integration with Hebrew
        test_messages = [
            {"role": "user", "content": "מה זה Dify.ai?"}
        ]
        
        try:
            response = self.generate_response(
                model="gemini-flash",
                messages=test_messages,
                parameters={"temperature": 0.7, "max_tokens": 200}
            )
            
            return {
                "success": True,
                "hebrew_capabilities": hebrew_test,
                "integration_test": {
                    "response_length": len(response["message"]["content"]),
                    "has_hebrew": self._contains_hebrew(response["message"]["content"]),
                    "tokens_used": response["usage"]["total_tokens"]
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "hebrew_capabilities": hebrew_test
            }
    
    def _contains_hebrew(self, text: str) -> bool:
        """Check if text contains Hebrew characters."""
        return any('\u0590' <= char <= '\u05FF' for char in text)


def create_dify_vertex_ai_integration() -> DifyVertexAIIntegration:
    """
    Factory function to create Dify Vertex AI integration.
    
    Returns:
        DifyVertexAIIntegration instance
    """
    return DifyVertexAIIntegration()


# Configuration helper for Dify environment
def setup_dify_vertex_ai_environment():
    """
    Setup environment variables for Dify Vertex AI integration.
    
    This function reads from various sources and sets up the environment
    for seamless integration with Dify.ai.
    """
    # Set up environment variables from docker-compose if available
    env_vars = {
        "GOOGLE_VERTEX_PROJECT": os.getenv("GOOGLE_VERTEX_PROJECT", "lionspace"),
        "GOOGLE_VERTEX_LOCATION": os.getenv("GOOGLE_VERTEX_LOCATION", "us-east1"),
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/app/gcp-key.json")
    }
    
    # Update environment
    for key, value in env_vars.items():
        if value:
            os.environ[key] = value
    
    return env_vars


if __name__ == "__main__":
    # Test the integration
    print("🚀 Testing Dify Vertex AI Integration")
    print("=" * 50)
    
    # Setup environment
    env = setup_dify_vertex_ai_environment()
    print("Environment setup:")
    for key, value in env.items():
        display_value = "***" if "CREDENTIALS" in key else value
        print(f"  {key}: {display_value}")
    
    # Create integration
    integration = create_dify_vertex_ai_integration()
    
    # Test credentials (mock for testing)
    test_credentials = {
        "project_id": env["GOOGLE_VERTEX_PROJECT"],
        "location": env["GOOGLE_VERTEX_LOCATION"],
        # "service_account_key": env["GOOGLE_APPLICATION_CREDENTIALS"]  # Uncomment if available
    }
    
    print("\n🔧 Initializing provider...")
    if integration.initialize_provider(test_credentials):
        print("✅ Provider initialized successfully")
        
        print("\n🔍 Testing Hebrew integration...")
        hebrew_test = integration.test_hebrew_integration()
        print(json.dumps(hebrew_test, indent=2, ensure_ascii=False))
    else:
        print("❌ Provider initialization failed")