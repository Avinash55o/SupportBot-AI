#!/usr/bin/env python3
"""
Simple test to verify token generation
"""
from datetime import datetime
import uuid

def generate_token():
    """Generate a ticket token"""
    return f"TKT-{datetime.now().strftime('%y%m%d')}-{str(uuid.uuid4())[:4].upper()}"

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
    
    # Check token format (should be 15 characters: TKT-YYMMDD-XXXX)
    for token in tokens:
        if token.startswith("TKT-") and len(token) == 15:
            print(f"✅ Token format correct: {token}")
        else:
            print(f"❌ Token format incorrect: {token} (length: {len(token)})")
    
    print(f"\n📋 Token generation test completed!")
    print(f"   Generated {len(tokens)} tokens")
    print(f"   All tokens are unique: {len(tokens) == len(unique_tokens)}")
    
    # Test token format for dashboard display
    print(f"\n🎫 Sample tokens for dashboard:")
    for i, token in enumerate(tokens[:3]):
        print(f"   Ticket {i+1}: {token}")
        print(f"   Display format: {token[:8]}...{token[-4:]}")

if __name__ == "__main__":
    test_token_generation()
