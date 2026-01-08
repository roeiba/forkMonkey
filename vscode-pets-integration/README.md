# VS Code Pets Integration - Fork Monkey

This directory contains experiments and assets for integrating the Fork Monkey pet into the [VS Code Pets extension](https://github.com/tonybaloney/vscode-pets).

## 🧪 Experiments

We tested two different approaches for generating Fork Monkey animations:

### Experiment 1: Image-Based Frame Generation
- **Method:** Generate each animation frame as a separate image using Gemini AI
- **Results:** High control, good quality, but time-consuming and larger files
- **Best for:** Static poses (idle, swipe, with_ball)
- [View Details →](experiment1/README.md)

### Experiment 2: Video-Based Frame Extraction ⭐ **Winner**
- **Method:** Generate a single video, extract frames, convert to GIF
- **Results:** 8x faster, 42% smaller files, smoother motion, single API call
- **Best for:** Motion animations (walk, run)
- [View Details →](experiment2/README.md)

## 📊 Quick Comparison

| Metric | Experiment 1 | Experiment 2 | Winner |
|--------|--------------|--------------|--------|
| **API Calls** | 6 per animation | 1 per animation | ✅ Exp 2 |
| **Generation Time** | ~4 minutes | ~30 seconds | ✅ Exp 2 |
| **File Size** | 20.8 KB | 12.0 KB | ✅ Exp 2 |
| **Motion Quality** | Good | Excellent | ✅ Exp 2 |
| **Pose Control** | High | Medium | ✅ Exp 1 |
| **Cost Efficiency** | Lower | Higher | ✅ Exp 2 |

**[View Interactive Comparison →](comparison.html)**

## 🎯 Recommended Hybrid Approach

Combine both methods for optimal results:

1. **Use Video Generation (Exp 2) for:**
   - `brown_walk_8fps.gif` - Walking animation
   - `brown_run_8fps.gif` - Running animation

2. **Use Image Generation (Exp 1) for:**
   - `brown_idle_8fps.gif` - Idle/breathing animation
   - `brown_swipe_8fps.gif` - Eating/swipe animation
   - `brown_with_ball_8fps.gif` - Holding ball animation

This approach minimizes API calls and generation time while maintaining high quality across all animation types.

## 📁 Directory Structure

```
vscode-pets-integration/
├── experiment1/              # Image-based approach
│   ├── assets/fork-monkey/   # Generated GIFs (5 animations)
│   ├── scripts/              # Generation scripts
│   └── README.md
├── experiment2/              # Video-based approach
│   ├── videos/               # Generated videos
│   ├── frames/               # Extracted frames
│   ├── gifs/                 # Final GIFs
│   ├── scripts/              # Conversion scripts
│   └── README.md
├── comparison.html           # Interactive comparison page
└── README.md                 # This file
```

## 🚀 Getting Started

### Prerequisites

```bash
# Install Python packages
pip3 install google-genai pillow

# Install ffmpeg (for video processing)
sudo apt-get install ffmpeg

# Set API key
export GEMINI_API_KEY="your-api-key-here"
```

### Generate Animations

**Option 1: Image-Based (Experiment 1)**
```bash
cd experiment1/scripts/sprite-generation
python3 generate_forkmonkey.py
python3 assemble_gifs.py
```

**Option 2: Video-Based (Experiment 2)**
```bash
cd experiment2/scripts
# First generate video using Gemini API
python3 video_to_gif.py
```

## 📈 Performance Metrics

### Experiment 1 (Image-Based)
- **Total API Calls:** 27 (for all 5 animations)
- **Total Generation Time:** ~19 minutes
- **Total File Size:** 93.2 KB
- **Animations:** idle, walk, run, swipe, with_ball

### Experiment 2 (Video-Based)
- **Total API Calls:** 1 (for walk animation)
- **Total Generation Time:** ~30 seconds
- **Total File Size:** 12.0 KB
- **Animations:** walk (more can be generated)

### Hybrid Approach (Recommended)
- **Total API Calls:** ~15 (3 videos + 12 images)
- **Estimated Time:** ~5 minutes
- **Estimated Size:** ~60 KB (all 5 animations)
- **Best Quality:** ✅

## 🎨 Asset Specifications

All animations must meet VS Code Pets standards:

- **Dimensions:** 111×101 pixels
- **Format:** Animated GIF
- **Frame Rate:** 4 FPS (250ms per frame)
- **Transparency:** Binary alpha (no semi-transparent pixels)
- **Background:** Transparent
- **Style:** 8-bit pixel art

## 🔗 Integration Steps

Once you have the final assets:

1. **Copy GIFs** to VS Code Pets media directory
2. **Create Pet Class** (`src/panel/pets/fork-monkey.ts`)
3. **Update Type Definitions** (add to `src/panel/pets.ts`)
4. **Register in Pet Factory**
5. **Test Locally** in VS Code Extension Development Host
6. **Submit Pull Request** to vscode-pets repository

See [experiment1/assets/fork-monkey/README.md](experiment1/assets/fork-monkey/README.md) for detailed integration instructions.

## 📝 Lessons Learned

1. **Video generation is superior for motion-based animations**
   - Faster, cheaper, smoother results
   - Single API call vs multiple

2. **Image generation is better for static poses**
   - More control over specific frames
   - Better for non-motion animations

3. **Hybrid approach is optimal**
   - Use the right tool for each animation type
   - Balances speed, cost, and quality

4. **Transparency handling is critical**
   - Binary alpha (no semi-transparency) is essential
   - White background removal must be aggressive
   - Post-processing is necessary for clean GIFs

## 🔍 References

- [VS Code Pets Repository](https://github.com/tonybaloney/vscode-pets)
- [Fork Monkey Issue #850](https://github.com/tonybaloney/vscode-pets/issues/850)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Gemini Video Generation](https://ai.google.dev/gemini-api/docs/video-generation)

## 📜 License

The Fork Monkey assets and code are intended for integration into VS Code Pets and follow the same license as the main project.

---

**Created:** December 24, 2025  
**Author:** Levi Law (with Manus AI assistance)  
**Status:** Experiments complete, ready for hybrid implementation
