#!/usr/bin/env python3
"""
Fork Monkey GIF Assembly - FINAL VERSION
Removes ALL semi-transparency to achieve clean GIF backgrounds
"""

import os
from PIL import Image
import glob

FRAMES_DIR = "/home/ubuntu/forkmonkey-assets/frames"
GIFS_DIR = "/home/ubuntu/forkmonkey-assets/gifs"
TARGET_SIZE = (111, 101)
FPS = 4
FRAME_DURATION = 250  # milliseconds
COLOR = "brown"

ANIMATIONS = {
    'idle': 4,
    'walk': 6,
    'run': 8,
    'swipe': 5,
    'with_ball': 4
}

def remove_all_semitransparency(img, threshold=200):
    """
    Remove ALL semi-transparent pixels
    Pixels with alpha > threshold become fully opaque
    Pixels with alpha <= threshold become fully transparent
    This eliminates the dotted pattern issue
    """
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    pixels = img.load()
    width, height = img.size
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # Binary alpha: either fully transparent or fully opaque
            if a > threshold:
                pixels[x, y] = (r, g, b, 255)  # Fully opaque
            else:
                pixels[x, y] = (0, 0, 0, 0)  # Fully transparent
    
    return img

def process_frame(frame_path, target_size):
    """Process frame with binary transparency"""
    print(f"    Processing: {os.path.basename(frame_path)}")
    
    img = Image.open(frame_path).convert('RGBA')
    
    # Remove semi-transparency FIRST
    img = remove_all_semitransparency(img, threshold=200)
    
    # Crop to content
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    
    # Resize maintaining aspect ratio
    img.thumbnail(target_size, Image.Resampling.LANCZOS)
    
    # After resize, remove semi-transparency AGAIN (resize can create it)
    img = remove_all_semitransparency(img, threshold=128)
    
    # Create final canvas
    final = Image.new('RGBA', target_size, (0, 0, 0, 0))
    x = (target_size[0] - img.width) // 2
    y = (target_size[1] - img.height) // 2
    final.paste(img, (x, y), img)
    
    # Final pass to ensure binary transparency
    final = remove_all_semitransparency(final, threshold=128)
    
    return final

def create_gif(anim_name, frame_count, output_path):
    """Create GIF with clean transparency"""
    print(f"\n🎬 Creating {anim_name} animation...")
    print(f"   Frames: {frame_count}")
    
    frame_files = []
    for i in range(1, frame_count + 1):
        frame_path = os.path.join(FRAMES_DIR, f"{anim_name}_frame_{i:02d}.png")
        if os.path.exists(frame_path):
            frame_files.append(frame_path)
    
    if not frame_files:
        print(f"   ❌ No frames found")
        return False
    
    print(f"   Found {len(frame_files)} frames")
    
    # Process frames
    frames = [process_frame(f, TARGET_SIZE) for f in frame_files]
    
    # Save as GIF
    print(f"   💾 Saving to: {output_path}")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION,
        loop=0,
        disposal=2,
        optimize=True
    )
    
    size = os.path.getsize(output_path)
    print(f"   ✅ Created! Size: {size / 1024:.1f} KB")
    
    return True

def main():
    print("="*70)
    print("🎞️  FORK MONKEY GIF ASSEMBLY - FINAL VERSION")
    print("="*70)
    print(f"Target: {TARGET_SIZE[0]}x{TARGET_SIZE[1]} @ {FPS} FPS")
    print(f"Frame duration: {FRAME_DURATION}ms")
    print(f"Strategy: Binary transparency (no semi-transparent pixels)")
    print()
    
    os.makedirs(GIFS_DIR, exist_ok=True)
    
    success = 0
    for anim_name, frame_count in ANIMATIONS.items():
        output_file = f"{COLOR}_{anim_name}_8fps.gif"
        output_path = os.path.join(GIFS_DIR, output_file)
        
        if create_gif(anim_name, frame_count, output_path):
            success += 1
    
    print("\n" + "="*70)
    print(f"✅ COMPLETE! {success}/{len(ANIMATIONS)} animations created")
    print("="*70)
    
    print("\n📋 Created GIFs:")
    total = 0
    for gif in sorted(glob.glob(os.path.join(GIFS_DIR, "*.gif"))):
        size = os.path.getsize(gif)
        total += size
        print(f"   • {os.path.basename(gif)}: {size / 1024:.1f} KB")
    
    print(f"\n   Total: {total / 1024:.1f} KB")
    print("\n✨ All semi-transparency removed - backgrounds should be clean!")

if __name__ == "__main__":
    main()
