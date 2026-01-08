# Fork Monkey Sprite Generation Scripts

Automated GIF generation pipeline using **Gemini 2.5 Flash Image (Nano Banana)** and Python.

## 📁 Scripts

### 1. `test_gemini.py`
Tests the Gemini API connection and generates a sample image.

```bash
python3 test_gemini.py
```

### 2. `generate_forkmonkey.py`
Generates all animation frames using Gemini AI.

```bash
python3 generate_forkmonkey.py
```

**Output:** 28 PNG frames (1024×1024) in `frames/` directory

### 3. `assemble_gifs.py`
Processes frames and assembles them into animated GIFs.

```bash
python3 assemble_gifs.py
```

**Output:** 5 animated GIFs (111×101, 8 FPS) in `gifs/` directory

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
sudo pip3 install google-genai pillow

# Set API key
export GEMINI_API_KEY="your-api-key-here"
```

### Generate All Assets

```bash
# 1. Test connection
python3 test_gemini.py

# 2. Generate frames (~8 minutes)
python3 generate_forkmonkey.py

# 3. Assemble GIFs (~30 seconds)
python3 assemble_gifs.py
```

## 📊 Output Specifications

- **Dimensions:** 111×101 pixels
- **Frame Rate:** 8 FPS
- **Format:** Animated GIF
- **Background:** Transparent
- **Style:** Pixel art

## 🎨 Animations Generated

1. **idle** - 4 frames, breathing animation
2. **walk** - 6 frames, walking cycle
3. **run** - 8 frames, running motion
4. **swipe** - 5 frames, fork eating motion
5. **with_ball** - 4 frames, holding ball

## 🔧 Customization

Edit `generate_forkmonkey.py` to:
- Add new animations
- Change character design
- Adjust frame counts
- Modify prompts

Edit `assemble_gifs.py` to:
- Change target size
- Adjust frame rate
- Modify color variants

## 📝 Notes

- Generation uses 1K resolution for quality
- Each frame takes ~15-20 seconds to generate
- Total generation time: ~8-10 minutes
- GIF assembly is fast (~30 seconds)

## 🎯 Integration

Generated GIFs are ready for VS Code Pets integration.
See `../assets/fork-monkey/README.md` for integration instructions.
