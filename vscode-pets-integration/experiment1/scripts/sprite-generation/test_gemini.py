#!/usr/bin/env python3
"""
Test script to verify Gemini API connection and image generation capability
"""

import os
from google import genai
from google.genai import types
from PIL import Image as PILImage
import io

def test_gemini_connection():
    """Test basic Gemini API connection"""
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY environment variable not set")
        return False, None
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    try:
        client = genai.Client(api_key=api_key)
        print("✅ Gemini API client created successfully")
        return True, client
    except Exception as e:
        print(f"❌ ERROR creating Gemini API client: {e}")
        return False, None

def test_image_generation(client):
    """Test image generation with a simple prompt"""
    print("\n🎨 Testing image generation...")
    
    try:
        prompt = "A simple pixel art sprite of a cute brown monkey, 8-bit style, transparent background, 111x101 pixels"
        
        print(f"📝 Prompt: {prompt}")
        print("⏳ Generating image with gemini-2.5-flash-image...")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1"
                )
            )
        )
        
        # Check if we got an image
        if response.parts:
            for part in response.parts:
                if part.inline_data:
                    print("✅ Image generated successfully!")
                    
                    # Get the image data and convert to PIL Image
                    image_bytes = part.inline_data.data
                    pil_image = PILImage.open(io.BytesIO(image_bytes))
                    
                    output_path = "/home/ubuntu/forkmonkey-assets/test_image.png"
                    pil_image.save(output_path)
                    print(f"💾 Test image saved to: {output_path}")
                    print(f"📏 Image size: {pil_image.size}")
                    print(f"🎨 Image mode: {pil_image.mode}")
                    
                    return True
                elif part.text:
                    print(f"📄 Text response: {part.text}")
        
        print("⚠️  No image in response")
        return False
        
    except Exception as e:
        print(f"❌ ERROR during image generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🧪 Gemini API Connection Test")
    print("=" * 60)
    
    success, client = test_gemini_connection()
    if not success:
        print("\n❌ Connection test failed. Exiting.")
        return
    
    if test_image_generation(client):
        print("\n" + "=" * 60)
        print("✅ All tests passed! Ready to generate fork monkey sprites!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Image generation test failed")
        print("=" * 60)

if __name__ == "__main__":
    main()
