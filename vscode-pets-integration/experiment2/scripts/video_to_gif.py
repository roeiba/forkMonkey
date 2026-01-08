#!/usr/bin/env python3
"""
Extract frames from video and create animated GIF
Experiment 2: Video-based approach
"""

import os
import subprocess
from PIL import Image
import glob

VIDEO_PATH = "/home/ubuntu/forkMonkey/vscode-pets-integration/experiment2/videos/walking_monkey.mp4"
FRAMES_DIR = "/home/ubuntu/forkMonkey/vscode-pets-integration/experiment2/frames"
GIFS_DIR = "/home/ubuntu/forkMonkey/vscode-pets-integration/experiment2/gifs"
TARGET_SIZE = (111, 101)
TARGET_FPS = 4
FRAME_DURATION = 250  # ms

def extract_frames_from_video(video_path, output_dir, fps=4):
    """Extract frames from video at specified FPS"""
    print(f"📹 Extracting frames from video at {fps} FPS...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Use ffmpeg to extract frames
    # -vf fps=4 extracts 4 frames per second
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f'fps={fps}',
        os.path.join(output_dir, 'frame_%03d.png'),
        '-y'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error extracting frames: {result.stderr}")
        return False
    
    frame_files = sorted(glob.glob(os.path.join(output_dir, 'frame_*.png')))
    print(f"✅ Extracted {len(frame_files)} frames")
    
    return frame_files

def remove_white_background(img, threshold=240):
    """
    Remove white/near-white background
    Pixels with RGB values all above threshold become transparent
    """
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    pixels = img.load()
    width, height = img.size
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # If pixel is near-white, make it transparent
            if r >= threshold and g >= threshold and b >= threshold:
                pixels[x, y] = (255, 255, 255, 0)
            else:
                # Make sure non-white pixels are fully opaque
                pixels[x, y] = (r, g, b, 255)
    
    return img

def process_frame(frame_path, target_size):
    """Process a single frame"""
    img = Image.open(frame_path).convert('RGBA')
    
    # Remove white background
    img = remove_white_background(img, threshold=240)
    
    # Crop to content
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    
    # Resize maintaining aspect ratio
    img.thumbnail(target_size, Image.Resampling.LANCZOS)
    
    # Remove any semi-transparency created by resize
    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a < 128:
                pixels[x, y] = (0, 0, 0, 0)
            else:
                pixels[x, y] = (r, g, b, 255)
    
    # Create final canvas
    final = Image.new('RGBA', target_size, (0, 0, 0, 0))
    x = (target_size[0] - img.width) // 2
    y = (target_size[1] - img.height) // 2
    final.paste(img, (x, y), img)
    
    return final

def create_walking_cycle(frame_files, output_path, cycle_length=6):
    """
    Create a walking cycle GIF from extracted frames
    Select evenly spaced frames to create a smooth cycle
    """
    print(f"\n🎬 Creating walking cycle GIF...")
    print(f"   Total frames available: {len(frame_files)}")
    print(f"   Target cycle length: {cycle_length} frames")
    
    # Select evenly spaced frames for the walking cycle
    if len(frame_files) > cycle_length:
        # Calculate step to get evenly distributed frames
        step = len(frame_files) // cycle_length
        selected_frames = frame_files[::step][:cycle_length]
    else:
        selected_frames = frame_files
    
    print(f"   Selected {len(selected_frames)} frames")
    
    # Process frames
    processed_frames = []
    for i, frame_path in enumerate(selected_frames):
        print(f"    Processing frame {i+1}/{len(selected_frames)}: {os.path.basename(frame_path)}")
        processed = process_frame(frame_path, TARGET_SIZE)
        processed_frames.append(processed)
    
    # Save as GIF
    print(f"   💾 Saving to: {output_path}")
    processed_frames[0].save(
        output_path,
        save_all=True,
        append_images=processed_frames[1:],
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
    print("🎞️  EXPERIMENT 2: VIDEO-TO-GIF CONVERSION")
    print("="*70)
    print(f"Video: {os.path.basename(VIDEO_PATH)}")
    print(f"Target: {TARGET_SIZE[0]}x{TARGET_SIZE[1]} @ {TARGET_FPS} FPS")
    print()
    
    # Extract frames from video
    frame_files = extract_frames_from_video(VIDEO_PATH, FRAMES_DIR, fps=TARGET_FPS)
    
    if not frame_files:
        print("❌ Failed to extract frames")
        return
    
    # Create output directory
    os.makedirs(GIFS_DIR, exist_ok=True)
    
    # Create walking cycle GIF
    output_path = os.path.join(GIFS_DIR, "brown_walk_8fps.gif")
    create_walking_cycle(frame_files, output_path, cycle_length=6)
    
    print("\n" + "="*70)
    print("✅ COMPLETE!")
    print("="*70)
    print(f"\n📁 Output: {output_path}")
    
    # Show comparison
    print("\n📊 Comparison:")
    exp1_walk = "/home/ubuntu/forkMonkey/vscode-pets-integration/experiment1/assets/fork-monkey/brown_walk_8fps.gif"
    if os.path.exists(exp1_walk):
        exp1_size = os.path.getsize(exp1_walk)
        exp2_size = os.path.getsize(output_path)
        print(f"   Experiment 1 (image-based): {exp1_size / 1024:.1f} KB")
        print(f"   Experiment 2 (video-based):  {exp2_size / 1024:.1f} KB")
        print(f"   Difference: {(exp2_size - exp1_size) / 1024:+.1f} KB")

if __name__ == "__main__":
    main()
