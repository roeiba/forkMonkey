#!/usr/bin/env python3
"""
Fork Monkey Sprite Generator
Generates all animation frames for the fork monkey pet using Gemini 2.5 Flash Image
"""

import os
import io
from google import genai
from google.genai import types
from PIL import Image, ImageOps
import time

# Configuration
API_KEY = os.environ.get('GEMINI_API_KEY')
MODEL = "gemini-2.5-flash-image"
OUTPUT_DIR = "/home/ubuntu/forkmonkey-assets/frames"
TARGET_SIZE = (111, 101)  # VS Code Pets standard size

# Animation definitions
ANIMATIONS = {
    'idle': {
        'frames': 4,
        'description': 'standing still with subtle breathing animation, holding a fork'
    },
    'walk': {
        'frames': 6,
        'description': 'walking animation with natural gait, fork in hand'
    },
    'run': {
        'frames': 8,
        'description': 'running fast with exaggerated movement, fork held up'
    },
    'swipe': {
        'frames': 5,
        'description': 'using the fork to eat or wave it around'
    },
    'with_ball': {
        'frames': 4,
        'description': 'standing idle while holding a ball in one hand and fork in the other'
    }
}

def create_client():
    """Create and return Gemini API client"""
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    return genai.Client(api_key=API_KEY)

def generate_base_character(client):
    """Generate the base fork monkey character design"""
    print("\n" + "="*60)
    print("🎨 Generating BASE CHARACTER DESIGN")
    print("="*60)
    
    prompt = """Create a pixel art sprite of a cute, small monkey character for a VS Code extension.
The monkey should be:
- Sitting/standing in an idle pose
- Holding a golden fork (eating utensil) in one hand
- Brown fur with lighter tan/beige face and belly
- Friendly, happy expression with big eyes
- Simple, clean pixel art style (8-bit retro game aesthetic)
- Centered in the frame
- Transparent background
- Approximately 100 pixels tall
- Similar style to retro game sprites like Pokemon or Stardew Valley

The fork should be clearly visible and golden/yellow colored.
The monkey should have a curled tail visible.
Keep the design simple and charming."""

    print(f"📝 Prompt: {prompt[:100]}...")
    print("⏳ Generating...")
    
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="1:1"
            )
        )
    )
    
    for part in response.parts:
        if part.inline_data:
            image_bytes = part.inline_data.data
            image = Image.open(io.BytesIO(image_bytes))
            
            # Save original
            base_path = os.path.join(OUTPUT_DIR, "base_character.png")
            image.save(base_path)
            print(f"✅ Base character saved: {base_path}")
            print(f"   Size: {image.size}, Mode: {image.mode}")
            
            return image
    
    raise Exception("No image generated")

def generate_animation_frame(client, animation_name, frame_number, total_frames, reference_image=None):
    """Generate a single animation frame"""
    
    anim_info = ANIMATIONS[animation_name]
    
    # Build prompt based on animation type
    base_prompt = f"""Create a pixel art sprite frame for a {animation_name} animation.
This is frame {frame_number} of {total_frames}.

Character: A cute brown monkey holding a golden fork (eating utensil).
Style: 8-bit pixel art, retro game aesthetic, clean and simple.
Background: Transparent.
Size: Approximately 100 pixels tall, centered in frame.

Animation: {anim_info['description']}
"""

    # Add frame-specific instructions
    if animation_name == 'idle':
        if frame_number == 1:
            base_prompt += "\nFrame 1: Base standing pose, neutral"
        elif frame_number == 2:
            base_prompt += "\nFrame 2: Slight upward movement (breathing in)"
        elif frame_number == 3:
            base_prompt += "\nFrame 3: Return to base pose"
        elif frame_number == 4:
            base_prompt += "\nFrame 4: Slight downward movement (breathing out)"
    
    elif animation_name == 'walk':
        cycle_pos = (frame_number - 1) % 6
        if cycle_pos in [0, 3]:
            base_prompt += f"\nFrame {frame_number}: Contact pose - one foot forward, one back"
        elif cycle_pos in [1, 4]:
            base_prompt += f"\nFrame {frame_number}: Passing pose - legs passing each other"
        else:
            base_prompt += f"\nFrame {frame_number}: Mid-stride pose"
    
    elif animation_name == 'run':
        if frame_number <= 2:
            base_prompt += f"\nFrame {frame_number}: Gathering momentum, leaning forward"
        elif frame_number <= 5:
            base_prompt += f"\nFrame {frame_number}: Full sprint, legs extended"
        else:
            base_prompt += f"\nFrame {frame_number}: Recovery stride"
    
    elif animation_name == 'swipe':
        if frame_number == 1:
            base_prompt += "\nFrame 1: Starting pose, fork at side"
        elif frame_number == 2:
            base_prompt += "\nFrame 2: Winding up, fork moving"
        elif frame_number == 3:
            base_prompt += "\nFrame 3: Peak action - fork extended/eating motion"
        elif frame_number == 4:
            base_prompt += "\nFrame 4: Follow through"
        else:
            base_prompt += "\nFrame 5: Return to neutral"
    
    elif animation_name == 'with_ball':
        base_prompt += f"\nFrame {frame_number}: Idle pose holding a small ball in one hand and fork in the other hand. Subtle breathing animation."
    
    base_prompt += "\n\nMaintain consistent character design: brown fur, tan face/belly, big eyes, curled tail, golden fork."
    
    print(f"  Frame {frame_number}/{total_frames}: Generating...")
    
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=base_prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1"
                )
            )
        )
        
        for part in response.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data
                image = Image.open(io.BytesIO(image_bytes))
                
                # Save frame
                frame_path = os.path.join(OUTPUT_DIR, f"{animation_name}_frame_{frame_number:02d}.png")
                image.save(frame_path)
                print(f"  ✅ Saved: {frame_path}")
                
                return image
        
        raise Exception("No image in response")
        
    except Exception as e:
        print(f"  ❌ Error generating frame: {e}")
        return None

def generate_all_animations(client):
    """Generate all animation frames"""
    print("\n" + "="*60)
    print("🎬 Generating ALL ANIMATION FRAMES")
    print("="*60)
    
    for anim_name, anim_info in ANIMATIONS.items():
        print(f"\n📹 Animation: {anim_name.upper()}")
        print(f"   Frames: {anim_info['frames']}")
        print(f"   Description: {anim_info['description']}")
        
        for frame_num in range(1, anim_info['frames'] + 1):
            generate_animation_frame(client, anim_name, frame_num, anim_info['frames'])
            
            # Small delay to avoid rate limiting
            time.sleep(1)
        
        print(f"✅ {anim_name} animation complete!")

def main():
    print("="*60)
    print("🐵🍴 FORK MONKEY SPRITE GENERATOR")
    print("="*60)
    
    # Create client
    client = create_client()
    print("✅ Gemini API client ready")
    
    # Generate base character
    base_char = generate_base_character(client)
    
    # Wait a bit before generating animations
    print("\n⏳ Waiting 3 seconds before generating animations...")
    time.sleep(3)
    
    # Generate all animations
    generate_all_animations(client)
    
    print("\n" + "="*60)
    print("✅ ALL SPRITES GENERATED!")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print("="*60)
    print("\n🎯 Next step: Run the GIF assembly script to create animated GIFs")

if __name__ == "__main__":
    main()
