"""
Secret Key Generator for JWT Authentication

This script generates cryptographically secure secret keys for your FastAPI application.
Use this to generate a SECRET_KEY for your .env file.
"""

import secrets
import string
import hashlib
import os


def generate_secret_key_simple(length: int = 64) -> str:
    """
    Generate a simple random secret key using URL-safe characters
    
    Args:
        length: Length of the secret key (default: 64)
    
    Returns:
        URL-safe secret key string
    """
    return secrets.token_urlsafe(length)


def generate_secret_key_hex(length: int = 32) -> str:
    """
    Generate a hexadecimal secret key
    
    Args:
        length: Number of bytes (default: 32 bytes = 64 hex characters)
    
    Returns:
        Hexadecimal secret key string
    """
    return secrets.token_hex(length)


def generate_secret_key_advanced() -> str:
    """
    Generate an advanced secret key using multiple entropy sources
    
    Returns:
        Highly secure secret key
    """
    # Combine multiple entropy sources
    random_bytes = secrets.token_bytes(32)
    timestamp = str(os.urandom(16))
    
    # Create hash from combined sources
    combined = random_bytes + timestamp.encode()
    secret_key = hashlib.sha256(combined).hexdigest()
    
    return secret_key


def generate_custom_secret_key(length: int = 64) -> str:
    """
    Generate a custom secret key with alphanumeric and special characters
    
    Args:
        length: Length of the secret key (default: 64)
    
    Returns:
        Custom secret key with mixed characters
    """
    # Define character set
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    
    # Generate secure random key
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    return secret_key


if __name__ == "__main__":
    print("=" * 80)
    print("SECRET KEY GENERATOR FOR JWT AUTHENTICATION")
    print("=" * 80)
    print()
    
    print("📌 What is a SECRET_KEY?")
    print("-" * 80)
    print("The SECRET_KEY is used to:")
    print("  • Sign JWT tokens to ensure they haven't been tampered with")
    print("  • Verify JWT tokens when users make authenticated requests")
    print("  • Encrypt sensitive data in your application")
    print()
    print("⚠️  IMPORTANT: Never commit your secret key to version control!")
    print("    Keep it secure and change it if compromised.")
    print()
    
    print("=" * 80)
    print("GENERATED SECRET KEYS (Choose one)")
    print("=" * 80)
    print()
    
    print("1️⃣  URL-Safe Key (Recommended for FastAPI/JWT):")
    print("-" * 80)
    key1 = generate_secret_key_simple()
    print(f"SECRET_KEY={key1}")
    print(f"Length: {len(key1)} characters")
    print()
    
    print("2️⃣  Hexadecimal Key:")
    print("-" * 80)
    key2 = generate_secret_key_hex()
    print(f"SECRET_KEY={key2}")
    print(f"Length: {len(key2)} characters")
    print()
    
    print("3️⃣  Advanced Secure Key:")
    print("-" * 80)
    key3 = generate_secret_key_advanced()
    print(f"SECRET_KEY={key3}")
    print(f"Length: {len(key3)} characters")
    print()
    
    print("4️⃣  Custom Mixed Character Key:")
    print("-" * 80)
    key4 = generate_custom_secret_key()
    print(f"SECRET_KEY={key4}")
    print(f"Length: {len(key4)} characters")
    print()
    
    print("=" * 80)
    print("HOW TO USE:")
    print("=" * 80)
    print("1. Copy one of the SECRET_KEY values above")
    print("2. Paste it into your .env file")
    print("3. Example:")
    print(f"   SECRET_KEY={key1}")
    print("   ALGORITHM=HS256")
    print("   ACCESS_TOKEN_EXPIRE_MINUTES=30")
    print()
    print("=" * 80)
    print("SECURITY BEST PRACTICES:")
    print("=" * 80)
    print("✅ DO:")
    print("  • Use at least 32 characters (64+ recommended)")
    print("  • Store in .env file (never in code)")
    print("  • Add .env to .gitignore")
    print("  • Use different keys for dev/staging/production")
    print("  • Rotate keys periodically")
    print()
    print("❌ DON'T:")
    print("  • Commit secret keys to Git")
    print("  • Share keys in chat/email")
    print("  • Use simple/predictable keys like 'mysecret123'")
    print("  • Reuse keys across different projects")
    print()
    print("=" * 80)