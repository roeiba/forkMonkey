# ForkMonkey Web Interface

Beautiful, modern web interface for viewing your ForkMonkey with a cutting-edge 2025 blocky/Minecraft-inspired design.

## Features

✨ **Modern Blocky Design**
- Minecraft/pixel-art inspired aesthetic
- Retro gaming vibes with NES.css
- Smooth animations and transitions
- Fully responsive layout

🎨 **Visual Elements**
- Animated particle background
- Real-time monkey SVG display
- Trait cards with rarity colors
- Evolution history timeline
- Glowing legendary traits

⚡ **Interactive**
- Auto-refresh every 60 seconds
- Keyboard shortcuts (R to refresh, D to download)
- Download monkey as SVG
- Hover effects and animations

## Quick Start

### 1. Make sure you have a monkey initialized

```bash
cd ..
python src/cli.py init
```

### 2. Start the web server

```bash
cd web
python serve.py
```

The website will automatically open in your browser at `http://localhost:8000`

### 3. View your monkey!

The interface will display:
- Your monkey's SVG visualization
- All traits with rarity indicators
- Evolution history
- Statistics and DNA hash

## Design Features

### Color Palette
- **Primary**: `#00ff88` (Neon green)
- **Secondary**: `#ff6b9d` (Pink)
- **Accent**: `#ffd93d` (Yellow)
- **Legendary**: `#ffd700` (Gold)

### Typography
- **Headers**: Press Start 2P (retro pixel font)
- **Body**: Space Grotesk (modern geometric)

### Layout
- Blocky panels with thick borders
- Box shadows for depth
- Squared corners (no border-radius)
- Grid-based responsive layout

### Animations
- Floating monkey
- Particle background
- Glowing legendary traits
- Smooth hover transitions
- Shimmer effects on header

## Libraries Used

- **NES.css** - Retro gaming UI framework
- **Particles.js** - Animated particle background
- **Chart.js** - Future stats visualization
- **Google Fonts** - Press Start 2P & Space Grotesk

## Keyboard Shortcuts

- `R` - Refresh monkey data
- `D` - Download monkey SVG

## File Structure

```
web/
├── index.html      # Main HTML structure
├── style.css       # Custom styles (blocky design)
├── script.js       # JavaScript functionality
├── serve.py        # Simple Python web server
└── README.md       # This file
```

## Customization

### Change Colors

Edit `style.css` and modify the CSS variables:

```css
:root {
    --primary: #00ff88;
    --secondary: #ff6b9d;
    --accent: #ffd93d;
    /* ... */
}
```

### Adjust Auto-Refresh

Edit `script.js` and change the interval:

```javascript
setInterval(() => {
    loadMonkeyData();
}, 60000); // Change this value (in milliseconds)
```

### Modify Particle Effects

Edit `script.js` and adjust the `particlesJS` configuration.

## Browser Compatibility

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

## Troubleshooting

### "Failed to load monkey data"
- Make sure you've initialized a monkey: `python src/cli.py init`
- Check that `monkey_data/` directory exists with JSON files

### Particles not showing
- Check browser console for errors
- Ensure internet connection (particles.js loads from CDN)

### SVG not displaying
- Verify `monkey_data/monkey.svg` exists
- Check browser console for CORS errors

## Performance

- Lightweight (~50KB total assets)
- Fast loading (~1s on average)
- Smooth 60fps animations
- Auto-pauses when tab is hidden

## Future Enhancements

Potential additions:
- [ ] Dark/light theme toggle
- [ ] Stats charts and graphs
- [ ] Monkey comparison tool
- [ ] Share on social media
- [ ] Print-friendly version
- [ ] Mobile app wrapper
- [ ] WebGL 3D monkey viewer

## Credits

- Design inspired by Minecraft and retro gaming
- Built with modern web technologies
- Powered by AI evolution (Claude)

---

**Enjoy your ForkMonkey! 🐵✨**
