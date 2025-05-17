"""
Azure OpenAI Deployment List Script

This script will list all available models and deployments in your Azure OpenAI service.
Run this script after updating your config.yml with the correct endpoint and API key.
"""

import os
import yaml
import openai
import sys

def print_section(title):
    print("\n" + "=" * 50)
    print(f" {title} ")
    print("=" * 50)

def main():
    print_section("Azure OpenAI Deployment Checker")
    
    try:
        # Load configuration
        config = yaml.safe_load(open("config.yml"))
        api_key = config.get('AZURE_OPENAI_API_KEY', '')
        api_version = config.get('AZURE_OPENAI_API_VERSION', '2023-05-15')
        endpoint = config.get('AZURE_OPENAI_ENDPOINT', '')
        
        # Print current configuration
        print(f"API Key: {api_key[:5]}..." if api_key else "API Key: Not set")
        print(f"API Version: {api_version}")
        print(f"Endpoint: {endpoint}")
        
        # Try both newer and older API versions
        api_versions_to_try = [
            api_version,  # Try the configured version first
            "2023-05-15",
            "2023-07-01-preview",
            "2023-12-01-preview"
        ]
        
        connection_successful = False
        
        for version in api_versions_to_try:
            print_section(f"Trying with API Version: {version}")
            
            try:
                client = openai.AzureOpenAI(
                    api_key=api_key,
                    api_version=version,
                    azure_endpoint=endpoint
                )
                
                # Test connection by listing models
                print("Listing available models...")
                models = client.models.list()
                
                print("✅ Connection successful!")
                print("\nAvailable Models:")
                for model in models:
                    print(f"- {model.id}")
                
                connection_successful = True
                print(f"\n✅ Working API Version: {version}")
                
                # No need to try other versions if this one works
                break
                
            except Exception as e:
                print(f"❌ Error with API Version {version}:")
                print(f"   {str(e)}")
                print("Trying next API version...\n")
        
        if not connection_successful:
            print_section("Connection Failed")
            print("Could not connect to Azure OpenAI with any API version.")
            print("Please check your endpoint URL and API key.")
            return 1
            
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
