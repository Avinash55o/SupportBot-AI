#!/usr/bin/env python3
"""
Simple token generation test without Flask
"""
from datetime import datetime
import uuid

def generate_token():
    """Generate a ticket token"""
    return f"TKT-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

def test_token_generation():
    """Test token generation"""
    print("🧪 Testing token generation...")
    
    # Generate multiple tokens
    tokens = []
    for i in range(5):
        token = generate_token()
        tokens.append(token)
        print(f"   Token {i+1}: {token}")
    
    # Check if tokens are unique
    unique_tokens = set(tokens)
    if len(tokens) == len(unique_tokens):
        print("✅ All tokens are unique!")
    else:
        print("❌ Duplicate tokens found!")
    
    # Check token format
    for token in tokens:
        if token.startswith("TKT-") and len(token) == 20:
            print(f"✅ Token format correct: {token}")
        else:
            print(f"❌ Token format incorrect: {token}")
    
    print(f"\n📋 Token generation test completed!")
    print(f"   Generated {len(tokens)} tokens")
    print(f"   All tokens are unique: {len(tokens) == len(unique_tokens)}")

if __name__ == "__main__":
    test_token_generation()
