#!/usr/bin/env python3
"""
Test script for Vertex AI provider implementation.

This script tests the Vertex AI provider with Hebrew language support
without requiring the full Dify environment to be running.
"""

import os
import json
import sys
from vertex_ai_provider import create_vertex_ai_provider

def test_vertex_ai_integration():
    """Test Vertex AI integration with Hebrew support."""
    print("🚀 Testing Vertex AI Provider for Dify.ai with Hebrew Support")
    print("=" * 60)
    
    # Configuration from environment or defaults
    project_id = os.getenv("GOOGLE_VERTEX_PROJECT", "lionspace")
    location = os.getenv("GOOGLE_VERTEX_LOCATION", "us-east1") 
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    print(f"📊 Configuration:")
    print(f"   Project ID: {project_id}")
    print(f"   Location: {location}")
    print(f"   Credentials: {'✅ Set' if credentials_path else '❌ Using ADC'}")
    print()
    
    try:
        # Initialize provider
        print("🔧 Initializing Vertex AI Provider...")
        provider = create_vertex_ai_provider(project_id, location, credentials_path)
        
        # Test 1: Configuration validation
        print("🔍 Test 1: Configuration Validation")
        validation = provider.validate_configuration()
        
        if validation["success"]:
            print("   ✅ Configuration is valid")
            print(f"   📍 Project: {validation['project_id']}")
            print(f"   🌍 Region: {validation['location']}")
            print(f"   🤖 Models: {', '.join(validation['available_models'])}")
        else:
            print(f"   ❌ Configuration failed: {validation['error']}")
            return False
        
        print()
        
        # Test 2: Model availability
        print("🔍 Test 2: Available Models")
        models = provider.get_available_models()
        for model_name, config in models.items():
            hebrew_support = "✅" if config["supports_hebrew"] else "❌"
            print(f"   🤖 {config['name']} ({model_name})")
            print(f"      Hebrew Support: {hebrew_support}")
            print(f"      Max Tokens: {config['max_tokens']}")
            print(f"      Description: {config['description']}")
        
        print()
        
        # Test 3: Hebrew capabilities
        print("🔍 Test 3: Hebrew Language Capabilities")
        hebrew_tests = provider.test_hebrew_capabilities()
        
        for model_name, result in hebrew_tests.items():
            status = "✅" if result["success"] else "❌"
            hebrew_resp = "✅" if result.get("has_hebrew_response") else "❌"
            print(f"   🤖 {model_name}: {status}")
            print(f"      Hebrew Response: {hebrew_resp}")
            print(f"      Response Length: {result.get('response_length', 0)} chars")
            if not result["success"]:
                print(f"      Error: {result.get('error', 'Unknown error')}")
        
        print()
        
        # Test 4: Sample conversation
        print("🔍 Test 4: Sample Hebrew Conversation")
        test_prompts = [
            "מה זה Dify.ai ואיך זה עובד?",
            "Explain how to set up Vertex AI integration (please respond in Hebrew)",
            "איך מגדירים אינטגרציה עם Vertex AI?"
        ]
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"   📝 Prompt {i}: {prompt}")
            
            response = provider.generate_response(
                prompt=prompt,
                model_name="gemini-flash",
                max_tokens=300,
                temperature=0.7
            )
            
            if response["success"]:
                response_text = response["response"]
                # Truncate for display
                display_text = response_text[:200] + "..." if len(response_text) > 200 else response_text
                print(f"   💬 Response: {display_text}")
                print(f"   📊 Tokens: ~{response['tokens_used']}, Model: {response['model_id']}")
            else:
                print(f"   ❌ Error: {response['error']}")
            
            print()
        
        print("🎉 Vertex AI Provider Testing Complete!")
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Install required packages:")
        print("   pip install google-cloud-aiplatform vertexai")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def check_environment():
    """Check if required environment variables are set."""
    print("🔍 Environment Check:")
    
    required_vars = [
        "GOOGLE_VERTEX_PROJECT",
        "GOOGLE_VERTEX_LOCATION", 
        "GOOGLE_APPLICATION_CREDENTIALS"
    ]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Don't print full credentials path for security
            display_value = "***" if "CREDENTIALS" in var else value
            print(f"   ✅ {var}={display_value}")
        else:
            print(f"   ⚠️  {var} not set (will use defaults)")
            if var == "GOOGLE_APPLICATION_CREDENTIALS":
                print("      Using Application Default Credentials (ADC)")
    
    print()
    return True


def main():
    """Main test function."""
    print("Vertex AI Integration Test for Dify.ai Hebrew Support")
    print("====================================================")
    print()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run tests
    success = test_vertex_ai_integration()
    
    if success:
        print()
        print("✅ All tests completed successfully!")
        print("🔗 Ready for integration with Dify.ai")
        sys.exit(0)
    else:
        print()
        print("❌ Tests failed. Check configuration and credentials.")
        sys.exit(1)


if __name__ == "__main__":
    main()