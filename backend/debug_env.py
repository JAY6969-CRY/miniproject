"""
Debug environment variable loading
"""
import os
from pathlib import Path
from dotenv import load_dotenv

print("=" * 70)
print("🔍 DEBUGGING ENVIRONMENT VARIABLES")
print("=" * 70)
print()

# Check .env file
env_path = Path(__file__).parent / '.env'
print(f"1. .env file path: {env_path}")
print(f"   Exists: {env_path.exists()}")
print()

# Read .env file directly
if env_path.exists():
    print("2. .env file contents:")
    with open(env_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:10], 1):
            line = line.strip()
            if line and not line.startswith('#'):
                print(f"   Line {i}: {line}")
    print()

# Load with dotenv
print("3. Loading with dotenv...")
result = load_dotenv(env_path)
print(f"   load_dotenv() returned: {result}")
print()

# Check environment variables
print("4. Environment variables:")
keys_to_check = ['ALPHA_VANTAGE_API_KEY', 'NEWS_API_KEY', 'GEMINI_API_KEY']
for key in keys_to_check:
    value = os.getenv(key)
    if value:
        print(f"   ✅ {key}: {value[:10]}...{value[-4:]} (length: {len(value)})")
    else:
        print(f"   ❌ {key}: Not found")
print()

# Check raw environment
print("5. Raw os.environ check:")
for key in keys_to_check:
    if key in os.environ:
        value = os.environ[key]
        print(f"   ✅ {key}: {value[:10]}...{value[-4:]} (length: {len(value)})")
    else:
        print(f"   ❌ {key}: Not in os.environ")
