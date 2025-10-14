"""
Quick Setup Script for Gemini API Key
Run this to easily configure your Gemini API key
"""
import os
from pathlib import Path

def setup_gemini_key():
    print("=" * 60)
    print("🤖 GEMINI AI SETUP")
    print("=" * 60)
    print()
    
    env_path = Path(__file__).parent / '.env'
    
    # Check if .env exists
    if not env_path.exists():
        print("❌ .env file not found!")
        print("Creating .env file from .env.example...")
        
        example_path = Path(__file__).parent / '.env.example'
        if example_path.exists():
            with open(example_path, 'r') as f:
                content = f.read()
            with open(env_path, 'w') as f:
                f.write(content)
            print("✅ .env file created!")
        else:
            print("❌ .env.example not found!")
            return
    
    # Read current .env
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Check if GEMINI_API_KEY already exists
    has_gemini_key = False
    key_line_index = -1
    
    for i, line in enumerate(lines):
        if line.startswith('GEMINI_API_KEY='):
            has_gemini_key = True
            key_line_index = i
            current_key = line.split('=', 1)[1].strip()
            if current_key and current_key != '':
                print(f"✅ Gemini API key already configured: {current_key[:10]}...")
                change = input("\n🔄 Do you want to change it? (y/n): ")
                if change.lower() != 'y':
                    print("✅ Keeping existing key")
                    return
            break
    
    print()
    print("📝 Get your FREE Gemini API key:")
    print("   👉 https://aistudio.google.com/app/apikey")
    print()
    print("   1. Sign in with Google")
    print("   2. Click 'Get API Key' or 'Create API Key'")
    print("   3. Copy your key (starts with AIza...)")
    print()
    
    api_key = input("🔑 Enter your Gemini API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⏭️  Skipped - You can add it later in .env file")
        return
    
    # Validate key format
    if not api_key.startswith('AIza'):
        print("⚠️  Warning: Key doesn't start with 'AIza' - it might be invalid")
        proceed = input("   Continue anyway? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    # Update .env file
    if has_gemini_key:
        lines[key_line_index] = f"GEMINI_API_KEY={api_key}\n"
    else:
        lines.append(f"\nGEMINI_API_KEY={api_key}\n")
    
    with open(env_path, 'w') as f:
        f.writelines(lines)
    
    print()
    print("=" * 60)
    print("✅ SUCCESS! Gemini API key configured")
    print("=" * 60)
    print()
    print("🚀 Next steps:")
    print("   1. Restart the backend server (Ctrl+C then 'python main.py')")
    print("   2. You should see: '✅ Gemini AI parser initialized successfully'")
    print("   3. Try asking: 'What's a good tech stock to day trade?'")
    print()
    print("💡 Tip: The app will still work without Gemini (uses fallback parser)")
    print()

if __name__ == "__main__":
    try:
        setup_gemini_key()
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
