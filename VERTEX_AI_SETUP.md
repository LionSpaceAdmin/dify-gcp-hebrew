# 🚀 Vertex AI Integration Setup for Dify.ai with Hebrew Support

This guide provides complete instructions for integrating Google Cloud Vertex AI with Dify.ai, including Hebrew language support and RTL text processing.

## 📋 Prerequisites

### 1. Google Cloud Platform Setup
- Active GCP project with billing enabled
- Vertex AI API enabled
- Service account with appropriate permissions

### 2. Required GCP APIs
```bash
# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage-component.googleapis.com
gcloud services enable compute.googleapis.com
```

### 3. Service Account Permissions
Create a service account with these roles:
- `roles/aiplatform.user` - For Vertex AI access
- `roles/storage.objectViewer` - For model access
- `roles/serviceusage.serviceUsageConsumer` - For API usage

## 🔧 Installation Steps

### Step 1: Install Dependencies

The required dependencies are already included in Dify's `pyproject.toml`:

```python
# Already included in Dify
"google-cloud-aiplatform==1.49.0"
"google-auth==2.29.0"
"google-cloud-storage==2.16.0"
```

If installing manually:
```bash
pip install google-cloud-aiplatform==1.49.0 vertexai
```

### Step 2: Setup Service Account

#### Option A: Service Account JSON Key
1. Create a service account in GCP Console
2. Download JSON key file
3. Set environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

#### Option B: Application Default Credentials (ADC)
For production environments, use ADC:
```bash
gcloud auth application-default login
```

### Step 3: Configure Environment Variables

Add to your `.env` file or docker-compose environment:

```env
# Vertex AI Configuration
GOOGLE_VERTEX_PROJECT=your-gcp-project-id
GOOGLE_VERTEX_LOCATION=us-east1
GOOGLE_APPLICATION_CREDENTIALS=/app/gcp-key.json

# Hebrew Language Support
LANG=he_IL.UTF-8
LC_ALL=he_IL.UTF-8
```

### Step 4: Integration with Dify

#### Method A: Plugin Integration (Recommended)

1. **Copy Integration Files**:
```bash
# Copy to Dify API directory
cp vertex_ai_provider.py dify/api/core/model_runtime/model_providers/
cp dify_vertex_ai_integration.py dify/api/core/model_runtime/model_providers/
```

2. **Update Position Configuration**:
The `vertex_ai` provider is already listed in `_position.yaml`, so no changes needed.

3. **Register Provider**:
Add to Dify's model provider factory or plugin system as needed.

#### Method B: Direct Integration

For development and testing, you can use the providers directly:

```python
from vertex_ai_provider import create_vertex_ai_provider
from dify_vertex_ai_integration import create_dify_vertex_ai_integration

# Initialize provider
provider = create_vertex_ai_provider(
    project_id="your-project-id",
    location="us-east1"
)

# Test Hebrew capabilities
hebrew_test = provider.test_hebrew_capabilities()
print(hebrew_test)
```

## 🧪 Testing the Integration

### Quick Test

Run the test script to validate everything is working:

```bash
# Set environment variables
export GOOGLE_VERTEX_PROJECT=your-project-id
export GOOGLE_VERTEX_LOCATION=us-east1

# Run tests
python test_vertex_ai.py
```

Expected output:
```
🚀 Testing Vertex AI Provider for Dify.ai with Hebrew Support
============================================================
✅ Configuration is valid
🤖 Gemini Pro (gemini-pro): Hebrew Support: ✅
🤖 Gemini Flash (gemini-flash): Hebrew Support: ✅
🎉 Vertex AI Provider Testing Complete!
```

### Advanced Testing

Test the full Dify integration:

```bash
python dify_vertex_ai_integration.py
```

## 🌐 Dify Configuration

### 1. Access Model Provider Settings

1. Open Dify admin interface
2. Go to **Model Providers**
3. Find **Google Vertex AI** provider
4. Click **Configure**

### 2. Enter Credentials

Fill in the required fields:
- **GCP Project ID**: Your Google Cloud project ID
- **Region**: `us-east1` (or your preferred region)
- **Service Account Key**: JSON key content or file path

### 3. Test Connection

Click **Test** to validate the configuration. You should see:
- ✅ Connection successful
- ✅ Hebrew support enabled
- ✅ Available models: Gemini Pro, Gemini Flash

### 4. Enable Models

After successful configuration:
1. Enable the models you want to use
2. Set default parameters if needed
3. Save configuration

## 🎯 Model Configuration

### Available Models

| Model | Description | Max Tokens | Hebrew Support | Use Case |
|-------|-------------|------------|----------------|----------|
| `gemini-pro` | Advanced multimodal model | 8,192 | ✅ | Complex reasoning, analysis |
| `gemini-flash` | Fast, efficient model | 8,192 | ✅ | Quick responses, conversations |

### Recommended Settings

#### For Hebrew Conversations
```json
{
  "temperature": 0.7,
  "max_tokens": 1024,
  "top_p": 0.95,
  "top_k": 40
}
```

#### For Hebrew Content Generation
```json
{
  "temperature": 0.8,
  "max_tokens": 2048,
  "top_p": 0.9,
  "top_k": 50
}
```

## 🔧 Docker Integration

### Update docker-compose.dev.yaml

The configuration is already set up in the existing docker-compose file:

```yaml
api:
  environment:
    # Vertex AI Configuration
    GOOGLE_APPLICATION_CREDENTIALS: /app/gcp-key.json
    GOOGLE_VERTEX_PROJECT: lionspace
    GOOGLE_VERTEX_LOCATION: us-east1
    
    # Hebrew Support
    LANG: he_IL.UTF-8
    LC_ALL: he_IL.UTF-8
  volumes:
    - ~/.config/gcloud:/app/.config/gcloud:ro
```

### Mount Service Account Key

If using JSON key file:

```yaml
volumes:
  - /path/to/your-service-account-key.json:/app/gcp-key.json:ro
```

## 🌍 Hebrew Language Features

### Automatic Hebrew Detection

The integration automatically detects Hebrew text and:
- Optimizes prompt formatting for RTL text
- Ensures proper Hebrew grammar instructions
- Maintains Hebrew character encoding (UTF-8)

### Hebrew-Specific Prompts

The system adds Hebrew instructions automatically:

```python
# Input prompt
"מה זה Dify.ai?"

# Enhanced prompt sent to Vertex AI
"""אנא השב בעברית בצורה ברורה ומדויקת. 
שים לב לכיווניות הטקסט (RTL) ולתקינות הדקדוק העברי.

מה זה Dify.ai?"""
```

### RTL Text Support

- Proper text direction handling
- Hebrew punctuation preservation
- Mixed Hebrew-English text support

## 🚨 Troubleshooting

### Common Issues

#### 1. Authentication Errors
```
Error: google.auth.exceptions.DefaultCredentialsError
```

**Solutions**:
- Verify `GOOGLE_APPLICATION_CREDENTIALS` path
- Check service account permissions
- Try ADC: `gcloud auth application-default login`

#### 2. Project/Region Issues
```
Error: Project 'xxx' not found or region not supported
```

**Solutions**:
- Verify project ID is correct
- Ensure Vertex AI is enabled in the project
- Check region availability for Vertex AI

#### 3. Hebrew Encoding Issues
```
Error: UnicodeDecodeError or mojibake in Hebrew text
```

**Solutions**:
- Ensure `LANG=he_IL.UTF-8` is set
- Verify terminal/browser supports Hebrew
- Check database collation for Hebrew support

#### 4. Model Not Available
```
Error: Model 'gemini-pro' not available
```

**Solutions**:
- Check model availability in your region
- Verify quotas and limits in GCP Console
- Try alternative model names

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Test with debug info
provider = create_vertex_ai_provider(project_id="your-project")
```

### Health Check

Quick health check command:

```bash
# Check configuration
python -c "
from dify_vertex_ai_integration import create_dify_vertex_ai_integration
integration = create_dify_vertex_ai_integration()
print(integration.get_provider_schema())
"
```

## 📊 Performance Optimization

### Model Selection Guidelines

- **Quick responses**: Use `gemini-flash`
- **Complex analysis**: Use `gemini-pro`
- **Hebrew-heavy content**: Both models optimized for Hebrew

### Token Management

```python
# Optimize token usage
parameters = {
    "max_tokens": 512,  # Reduce for shorter responses
    "temperature": 0.3,  # Lower for more focused responses
}
```

### Caching Strategies

For production deployment:
- Cache frequent Hebrew prompts
- Use Redis for model responses
- Implement prompt templates

## 🔒 Security Best Practices

### 1. Credential Management
- Never commit JSON keys to git
- Use Secret Manager in production
- Rotate service account keys regularly

### 2. Access Control
- Limit service account permissions
- Use IAM conditions for additional security
- Monitor API usage with Cloud Audit Logs

### 3. Data Privacy
- Be aware of data processing in Google Cloud
- Review Google's AI/ML data usage policies
- Consider data residency requirements

## 📈 Monitoring and Observability

### GCP Monitoring

Monitor in Google Cloud Console:
- **Vertex AI Metrics**: API calls, latency, errors
- **Cloud Logging**: Request/response logs
- **Billing**: API usage and costs

### Dify Integration Monitoring

Add to your monitoring:
- Model response times
- Hebrew text processing accuracy
- Token usage patterns
- Error rates by model

## ✅ Validation Checklist

Before going to production:

- [ ] GCP project and billing configured
- [ ] Vertex AI API enabled
- [ ] Service account created with proper roles
- [ ] Environment variables configured
- [ ] Hebrew language support tested
- [ ] Both Gemini models working
- [ ] Authentication working in Docker
- [ ] Integration tests passing
- [ ] Hebrew RTL text displaying correctly
- [ ] Monitoring and logging configured

## 🚀 Next Steps

After successful setup:

1. **Test Hebrew Conversations**: Create test apps in Dify with Hebrew prompts
2. **Performance Tuning**: Optimize model parameters for your use case
3. **Production Deployment**: Move to GCP production environment
4. **User Training**: Train users on Hebrew-specific features
5. **Monitoring Setup**: Implement comprehensive monitoring

## 🆘 Support

For additional support:

1. **Dify Documentation**: [docs.dify.ai](https://docs.dify.ai)
2. **Vertex AI Documentation**: [cloud.google.com/vertex-ai/docs](https://cloud.google.com/vertex-ai/docs)
3. **Hebrew Language Issues**: Check UTF-8 encoding and browser support
4. **GCP Issues**: Use Google Cloud Support or Community forums

---

**עם תמיכה מלאה בעברית ו-RTL! 🇮🇱**
*Full Hebrew and RTL support included! 🇮🇱*