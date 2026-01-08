# Experiment 1: Image-Based Frame Generation

## Approach

Generate individual animation frames as separate images using Gemini AI, then assemble them into animated GIFs.

## Method

1. **Frame Generation:** Use Gemini 2.5 Flash Image (Nano Banana) to generate each animation frame as a separate 1024×1024 PNG image
2. **Processing:** Resize frames to 111×101 pixels and remove semi-transparency
3. **Assembly:** Combine frames into animated GIFs using Pillow

## Results

✅ **Pros:**
- High control over each frame
- Can generate specific poses/actions
- Character consistency across frames
- Clean pixel art style

❌ **Cons:**
- Requires 27 separate API calls (one per frame)
- Time-consuming generation (~19 minutes)
- Manual frame sequencing needed
- Some transparency artifacts remain

## Technical Details

- **AI Model:** Gemini 2.5 Flash Image (gemini-2.5-flash-img-001)
- **Frame Count:** 28 frames (1 base + 27 animation frames)
- **Generation Time:** ~19 minutes
- **Processing Time:** ~1 minute
- **Total Size:** 93.2 KB (5 GIFs)
- **Transparency:** Binary alpha channel

## File Structure

```
experiment1/
├── assets/fork-monkey/     # Final GIF animations
├── scripts/                # Generation and assembly scripts
└── README.md              # This file
```

## Conclusion

This approach works well for creating custom animations with specific poses, but is time-consuming and requires careful transparency handling. The results are good but could potentially be improved with a video-based approach.
