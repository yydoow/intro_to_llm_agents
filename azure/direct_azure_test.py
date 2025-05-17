import os
import openai
import yaml
import json

# Load config
config = yaml.safe_load(open("config.yml"))

# Print configuration
print("=== Azure OpenAI Configuration ===")
print(f"API Key: {config.get('AZURE_OPENAI_API_KEY', '')[:5]}...")
print(f"API Version: {config.get('AZURE_OPENAI_API_VERSION', '')}")
print(f"Endpoint: {config.get('AZURE_OPENAI_ENDPOINT', '')}")
print(f"Deployment Name: {config.get('AZURE_OPENAI_DEPLOYMENT_NAME', '')}")

# Create Azure OpenAI client with a more stable API version
api_version = "2023-05-15"  # Using a more widely supported version
api_version = "2025-01-01-preview"  # Using a more widely supported version
print(f"Using API Version: {api_version} (overriding config value)")

client = openai.AzureOpenAI(
    api_key=config.get('AZURE_OPENAI_API_KEY', ''),
    api_version=api_version,
    azure_endpoint=config.get('AZURE_OPENAI_ENDPOINT', '')
)

try:
    # Try to list models
    print("\nTesting connection by listing models...")
    models = client.models.list()
    print(f"Connection successful! Available models:")
    for model in models:
        print(f"- {model.id}")
        
    # Try a simple completion
    print("\nTesting a simple completion with your deployment...")
    response = client.chat.completions.create(
        model=config.get('AZURE_OPENAI_DEPLOYMENT_NAME', ''),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, can you confirm you're working with Azure OpenAI?"}
        ],
        max_tokens=100
    )
    print(f"\nResponse: {response.choices[0].message.content}")
    print(f"\nModel: {response.model}")
    print(f"Usage: {response.usage.total_tokens} tokens")
    
except Exception as e:
    print(f"\nError connecting to Azure OpenAI:")
    print(f"{str(e)}")
    print("\nTroubleshooting suggestions:")
    print("1. Check if your API key is correct")
    print("2. Verify your Azure endpoint exists (it should be in the format https://{resource-name}.openai.azure.com/)")
    print("3. Make sure your deployment name matches exactly what's in the Azure portal")
    print("4. Confirm the API version is supported (2024-11-20 is very new, try 2023-05-15 if it fails)")
