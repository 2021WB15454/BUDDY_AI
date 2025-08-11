#!/usr/bin/env python3
"""
Detailed response analyzer to see what the server is actually returning
"""

import requests
import json

def analyze_server_response():
    """Get detailed response from server"""
    
    print("🔍 DETAILED SERVER RESPONSE ANALYSIS")
    print("=" * 50)
    
    url = "https://buddy-ai-0t6c.onrender.com/api/ask"
    test_message = "Tell me a joke"
    
    print(f"Testing: {test_message}")
    print(f"Endpoint: {url}")
    print()
    
    try:
        response = requests.post(
            url,
            json={"message": test_message},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("Response JSON:")
                print(json.dumps(data, indent=2))
                
                # Check what fields are in the response
                print(f"\nResponse keys: {list(data.keys())}")
                
                for key, value in data.items():
                    print(f"{key}: {type(value)} = {str(value)[:100]}...")
                    
            except json.JSONDecodeError:
                print("Response is not valid JSON:")
                print(response.text)
        else:
            print("Error response:")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    analyze_server_response()
