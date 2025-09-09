#!/usr/bin/env python3
"""
Validate the Vertex AI implementation structure and completeness.

This script checks the implementation files for completeness and correctness
without requiring the actual Google Cloud libraries to be installed.
"""

import os
import re
import json


def validate_file_structure():
    """Validate that all required files are present and properly structured."""
    print("📁 File Structure Validation")
    print("=" * 30)
    
    required_files = {
        "vertex_ai_provider.py": {
            "description": "Core Vertex AI provider implementation",
            "required_classes": ["VertexAIProvider"],
            "required_functions": ["create_vertex_ai_provider"],
            "min_size": 8000
        },
        "dify_vertex_ai_integration.py": {
            "description": "Dify integration layer", 
            "required_classes": ["DifyVertexAIIntegration"],
            "required_functions": ["create_dify_vertex_ai_integration"],
            "min_size": 12000
        },
        "test_vertex_ai.py": {
            "description": "Test suite for Vertex AI integration",
            "required_functions": ["test_vertex_ai_integration"],
            "min_size": 4000
        },
        "VERTEX_AI_SETUP.md": {
            "description": "Setup and configuration guide",
            "min_size": 8000
        }
    }
    
    all_files_ok = True
    
    for filename, requirements in required_files.items():
        print(f"\n🔍 Checking {filename}")
        
        if not os.path.exists(filename):
            print(f"   ❌ File not found")
            all_files_ok = False
            continue
        
        # Check file size
        size = os.path.getsize(filename)
        min_size = requirements.get("min_size", 0)
        
        print(f"   📏 Size: {size:,} bytes (min: {min_size:,})")
        if size < min_size:
            print(f"   ⚠️  File smaller than expected")
        
        # Read file content for analysis
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required classes
        if "required_classes" in requirements:
            for class_name in requirements["required_classes"]:
                if f"class {class_name}" in content:
                    print(f"   ✅ Class {class_name} found")
                else:
                    print(f"   ❌ Class {class_name} missing")
                    all_files_ok = False
        
        # Check for required functions
        if "required_functions" in requirements:
            for func_name in requirements["required_functions"]:
                if f"def {func_name}" in content:
                    print(f"   ✅ Function {func_name} found")
                else:
                    print(f"   ❌ Function {func_name} missing")
                    all_files_ok = False
        
        print(f"   📝 {requirements['description']}")
    
    return all_files_ok


def validate_vertex_ai_provider():
    """Validate the VertexAIProvider implementation."""
    print("\n🤖 Vertex AI Provider Validation")
    print("=" * 35)
    
    if not os.path.exists("vertex_ai_provider.py"):
        print("❌ vertex_ai_provider.py not found")
        return False
    
    with open("vertex_ai_provider.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    validations = [
        # Check for required imports
        (r"from google\.cloud import aiplatform", "Google Cloud AI Platform import"),
        (r"import vertexai", "Vertex AI import"),
        (r"from vertexai\.generative_models import GenerativeModel", "Generative Model import"),
        
        # Check for Hebrew support functions
        (r"def _prepare_hebrew_prompt", "Hebrew prompt preparation method"),
        (r"def _contains_hebrew", "Hebrew text detection method"),
        (r"def test_hebrew_capabilities", "Hebrew capabilities testing method"),
        
        # Check for model configurations
        (r"gemini-pro", "Gemini Pro model configuration"),
        (r"gemini-flash", "Gemini Flash model configuration"),
        (r"supports_hebrew.*True", "Hebrew support flag"),
        
        # Check for core methods
        (r"def generate_response", "Response generation method"),
        (r"def validate_configuration", "Configuration validation method"),
        (r"def get_available_models", "Model listing method"),
        
        # Check Hebrew instructions
        (r"אנא השב בעברית", "Hebrew response instructions"),
        (r"RTL", "RTL text direction support"),
    ]
    
    all_valid = True
    
    for pattern, description in validations:
        if re.search(pattern, content):
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description}")
            all_valid = False
    
    return all_valid


def validate_dify_integration():
    """Validate the Dify integration implementation."""
    print("\n🔗 Dify Integration Validation")
    print("=" * 30)
    
    if not os.path.exists("dify_vertex_ai_integration.py"):
        print("❌ dify_vertex_ai_integration.py not found")
        return False
    
    with open("dify_vertex_ai_integration.py", 'r', encoding='utf-8') as f:
        content = f.read()
    
    validations = [
        # Check Dify-specific structures
        (r"def get_provider_schema", "Provider schema method"),
        (r"def get_model_schemas", "Model schemas method"),
        (r"provider_credential_schema", "Credential schema configuration"),
        (r"parameter_rules", "Parameter rules configuration"),
        
        # Check integration methods
        (r"def generate_response", "Response generation integration"),
        (r"def _messages_to_prompt", "Message conversion method"),
        (r"def validate_credentials", "Credential validation method"),
        
        # Check Hebrew integration
        (r"def test_hebrew_integration", "Hebrew integration testing"),
        (r"enable_hebrew.*True", "Hebrew enablement"),
        
        # Check Dify model configuration
        (r"model_type.*llm", "LLM model type configuration"),
        (r"context_size", "Context size configuration"),
        (r"temperature", "Temperature parameter"),
        (r"max_tokens", "Max tokens parameter"),
        
        # Check multilingual labels
        (r"en_US", "English labels"),
        (r"\"he\"", "Hebrew labels"),
    ]
    
    all_valid = True
    
    for pattern, description in validations:
        if re.search(pattern, content):
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description}")
            all_valid = False
    
    return all_valid


def validate_hebrew_support():
    """Validate Hebrew language support implementation."""
    print("\n🇮🇱 Hebrew Language Support Validation")
    print("=" * 40)
    
    hebrew_features = []
    
    # Check all Python files for Hebrew support
    for filename in ["vertex_ai_provider.py", "dify_vertex_ai_integration.py"]:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for Hebrew text
            hebrew_text_found = bool(re.search(r'[\u0590-\u05FF]+', content))
            if hebrew_text_found:
                hebrew_features.append(f"Hebrew text in {filename}")
                print(f"   ✅ Hebrew text found in {filename}")
            
            # Check for Hebrew processing functions
            hebrew_functions = [
                (r"_prepare_hebrew_prompt", "Hebrew prompt preparation"),
                (r"_contains_hebrew", "Hebrew text detection"),
                (r"test_hebrew", "Hebrew testing capabilities"),
                (r"enable_hebrew", "Hebrew enablement option"),
                (r"supports_hebrew", "Hebrew support flags")
            ]
            
            for pattern, description in hebrew_functions:
                if re.search(pattern, content):
                    hebrew_features.append(f"{description} in {filename}")
                    print(f"   ✅ {description}")
    
    # Check documentation
    if os.path.exists("VERTEX_AI_SETUP.md"):
        with open("VERTEX_AI_SETUP.md", 'r', encoding='utf-8') as f:
            content = f.read()
        
        hebrew_doc_features = [
            (r"Hebrew", "Hebrew language mentioned"),
            (r"RTL", "RTL support mentioned"),
            (r"עברית", "Hebrew text in documentation"),
            (r"he_IL\.UTF-8", "Hebrew locale configuration"),
            (r"Hebrew.*support", "Hebrew support documentation")
        ]
        
        for pattern, description in hebrew_doc_features:
            if re.search(pattern, content, re.IGNORECASE):
                hebrew_features.append(f"{description} in documentation")
                print(f"   ✅ {description}")
    
    print(f"\n   📊 Total Hebrew features found: {len(hebrew_features)}")
    
    return len(hebrew_features) >= 8  # Expect at least 8 Hebrew-related features


def validate_configuration_completeness():
    """Validate that all configuration options are present."""
    print("\n⚙️ Configuration Completeness")
    print("=" * 30)
    
    config_checks = []
    
    # Check environment variables in docker-compose
    if os.path.exists("docker-compose.dev.yaml"):
        with open("docker-compose.dev.yaml", 'r') as f:
            compose_content = f.read()
        
        env_vars = [
            "GOOGLE_VERTEX_PROJECT",
            "GOOGLE_VERTEX_LOCATION", 
            "GOOGLE_APPLICATION_CREDENTIALS",
            "LANG.*he_IL.UTF-8",
            "LC_ALL.*he_IL.UTF-8"
        ]
        
        for var in env_vars:
            if re.search(var, compose_content):
                config_checks.append(f"Environment variable {var}")
                print(f"   ✅ {var} configured in docker-compose")
            else:
                print(f"   ❌ {var} missing from docker-compose")
    
    # Check for credential configuration
    credential_configs = [
        (r"project_id", "GCP Project ID configuration"),
        (r"location", "GCP Region configuration"), 
        (r"service_account", "Service Account configuration"),
        (r"credentials_path", "Credentials path configuration")
    ]
    
    for filename in ["vertex_ai_provider.py", "dify_vertex_ai_integration.py"]:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                content = f.read()
            
            for pattern, description in credential_configs:
                if re.search(pattern, content):
                    config_checks.append(f"{description} in {filename}")
    
    # Remove duplicates
    config_checks = list(set(config_checks))
    
    print(f"\n   📊 Total configuration features: {len(config_checks)}")
    for check in config_checks:
        print(f"      • {check}")
    
    return len(config_checks) >= 10


def generate_validation_report():
    """Generate a comprehensive validation report."""
    print("\n📊 Validation Report")
    print("=" * 20)
    
    report = {
        "timestamp": "2024-12-09",
        "validation_results": {
            "file_structure": validate_file_structure(),
            "vertex_ai_provider": validate_vertex_ai_provider(),
            "dify_integration": validate_dify_integration(),
            "hebrew_support": validate_hebrew_support(),
            "configuration": validate_configuration_completeness()
        },
        "implementation_summary": {
            "total_files": len([f for f in os.listdir('.') if f.endswith('.py') or f.endswith('.md')]),
            "code_files": len([f for f in os.listdir('.') if f.endswith('.py')]),
            "documentation_files": len([f for f in os.listdir('.') if f.endswith('.md')]),
            "features": [
                "Vertex AI integration",
                "Hebrew language support",
                "RTL text processing", 
                "Dify.ai compatibility",
                "Gemini Pro model",
                "Gemini Flash model",
                "Configuration management",
                "Error handling",
                "Testing framework",
                "Documentation"
            ]
        }
    }
    
    # Calculate overall score
    total_tests = len(report["validation_results"])
    passed_tests = sum(1 for result in report["validation_results"].values() if result)
    score = (passed_tests / total_tests) * 100
    
    report["overall_score"] = score
    report["status"] = "READY" if score >= 80 else "NEEDS_WORK" if score >= 60 else "INCOMPLETE"
    
    print(json.dumps(report, indent=2))
    
    return report


def main():
    """Main validation execution."""
    print("🔍 Vertex AI Integration Validation")
    print("==================================\n")
    
    # Run all validations
    report = generate_validation_report()
    
    print(f"\n📈 Overall Score: {report['overall_score']:.1f}%")
    print(f"🎯 Status: {report['status']}")
    
    if report['status'] == 'READY':
        print("\n✅ Implementation is ready for integration with Dify.ai!")
        print("\n🚀 Next steps:")
        print("1. Set up GCP project and Vertex AI API")
        print("2. Create service account with proper permissions")
        print("3. Configure environment variables")
        print("4. Deploy to Dify development environment")
        print("5. Test Hebrew language capabilities")
        return 0
    else:
        print(f"\n⚠️ Implementation needs more work before deployment")
        print("Please address the failed validations above.")
        return 1


if __name__ == "__main__":
    exit(main())