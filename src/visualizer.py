"""
ForkMonkey Visualizer

Generates SVG representations of monkeys based on their DNA.
"""

import math
from typing import Dict, Tuple
from src.genetics import MonkeyDNA, TraitCategory, Rarity


class MonkeyVisualizer:
    """Generates SVG monkey art from DNA"""
    
    # Color mappings
    COLORS = {
        # Body colors
        "brown": "#8B4513",
        "tan": "#D2B48C",
        "beige": "#F5F5DC",
        "gray": "#808080",
        "golden": "#FFD700",
        "silver": "#C0C0C0",
        "copper": "#B87333",
        "bronze": "#CD7F32",
        "blue": "#4169E1",
        "purple": "#9370DB",
        "green": "#32CD32",
        "pink": "#FF69B4",
        "rainbow": "url(#rainbow-gradient)",
        "galaxy": "url(#galaxy-gradient)",
        "holographic": "url(#holo-gradient)",
        "crystal": "#E0FFFF",
        
        # Background colors
        "white": "#FFFFFF",
        "blue_sky": "#87CEEB",
        "green_grass": "#90EE90",
        "sunset": "#FF6347",
        "forest": "#228B22",
        "beach": "#F0E68C",
        "mountains": "#708090",
        "city": "#696969",
        "space": "#000033",
        "underwater": "#006994",
        "volcano": "#FF4500",
        "aurora": "#00FF7F",
        "multiverse": "url(#multiverse-gradient)",
        "black_hole": "#000000",
        "dimension_rift": "url(#rift-gradient)",
        "heaven": "#F0F8FF"
    }
    
    @classmethod
    def generate_svg(cls, dna: MonkeyDNA, width: int = 400, height: int = 400) -> str:
        """Generate complete SVG for a monkey"""
        
        # Get trait values
        body_color = dna.traits[TraitCategory.BODY_COLOR].value
        expression = dna.traits[TraitCategory.FACE_EXPRESSION].value
        accessory = dna.traits[TraitCategory.ACCESSORY].value
        pattern = dna.traits[TraitCategory.PATTERN].value
        background = dna.traits[TraitCategory.BACKGROUND].value
        special = dna.traits[TraitCategory.SPECIAL].value
        
        # Build SVG
        svg_parts = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            cls._generate_defs(),
            cls._generate_background(background, width, height),
            cls._generate_body(body_color, pattern, width, height),
            cls._generate_face(expression, width, height),
            cls._generate_accessory(accessory, width, height),
            cls._generate_special_effects(special, width, height),
            '</svg>'
        ]
        
        return '\n'.join(svg_parts)
    
    @classmethod
    def _generate_defs(cls) -> str:
        """Generate SVG definitions (gradients, patterns)"""
        return '''
<defs>
    <!-- Rainbow gradient -->
    <linearGradient id="rainbow-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#FF0000;stop-opacity:1" />
        <stop offset="16%" style="stop-color:#FF7F00;stop-opacity:1" />
        <stop offset="33%" style="stop-color:#FFFF00;stop-opacity:1" />
        <stop offset="50%" style="stop-color:#00FF00;stop-opacity:1" />
        <stop offset="66%" style="stop-color:#0000FF;stop-opacity:1" />
        <stop offset="83%" style="stop-color:#4B0082;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#9400D3;stop-opacity:1" />
    </linearGradient>
    
    <!-- Galaxy gradient -->
    <radialGradient id="galaxy-gradient">
        <stop offset="0%" style="stop-color:#9400D3;stop-opacity:1" />
        <stop offset="50%" style="stop-color:#4B0082;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#000033;stop-opacity:1" />
    </radialGradient>
    
    <!-- Holographic gradient -->
    <linearGradient id="holo-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#FF00FF;stop-opacity:0.8" />
        <stop offset="50%" style="stop-color:#00FFFF;stop-opacity:0.8" />
        <stop offset="100%" style="stop-color:#FFFF00;stop-opacity:0.8" />
    </linearGradient>
    
    <!-- Multiverse gradient -->
    <radialGradient id="multiverse-gradient">
        <stop offset="0%" style="stop-color:#FFD700;stop-opacity:1" />
        <stop offset="33%" style="stop-color:#FF00FF;stop-opacity:1" />
        <stop offset="66%" style="stop-color:#00FFFF;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
    </radialGradient>
    
    <!-- Dimension rift gradient -->
    <linearGradient id="rift-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#000000;stop-opacity:1" />
        <stop offset="25%" style="stop-color:#9400D3;stop-opacity:1" />
        <stop offset="50%" style="stop-color:#00FFFF;stop-opacity:1" />
        <stop offset="75%" style="stop-color:#9400D3;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
    </linearGradient>
</defs>
'''
    
    @classmethod
    def _generate_background(cls, background: str, width: int, height: int) -> str:
        """Generate background"""
        color = cls.COLORS.get(background, "#FFFFFF")
        
        if background == "space":
            # Add stars
            stars = ''.join([
                f'<circle cx="{i*50+25}" cy="{j*50+25}" r="1" fill="white" opacity="0.8"/>'
                for i in range(width//50) for j in range(height//50)
            ])
            return f'<rect width="{width}" height="{height}" fill="{color}"/>{stars}'
        
        return f'<rect width="{width}" height="{height}" fill="{color}"/>'
    
    @classmethod
    def _generate_body(cls, body_color: str, pattern: str, width: int, height: int) -> str:
        """Generate monkey body"""
        cx, cy = width // 2, height // 2
        color = cls.COLORS.get(body_color, "#8B4513")
        
        body_parts = []
        
        # Head (large circle)
        head_r = 120
        body_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{head_r}" fill="{color}" stroke="#000" stroke-width="3"/>')
        
        # Ears
        ear_r = 40
        ear_offset = 90
        body_parts.append(f'<circle cx="{cx-ear_offset}" cy="{cy-30}" r="{ear_r}" fill="{color}" stroke="#000" stroke-width="2"/>')
        body_parts.append(f'<circle cx="{cx+ear_offset}" cy="{cy-30}" r="{ear_r}" fill="{color}" stroke="#000" stroke-width="2"/>')
        
        # Inner ears
        body_parts.append(f'<circle cx="{cx-ear_offset}" cy="{cy-30}" r="{ear_r-15}" fill="#FFB6C1"/>')
        body_parts.append(f'<circle cx="{cx+ear_offset}" cy="{cy-30}" r="{ear_r-15}" fill="#FFB6C1"/>')
        
        # Face area (lighter)
        face_r = 80
        body_parts.append(f'<ellipse cx="{cx}" cy="{cy+20}" rx="{face_r}" ry="{face_r-10}" fill="#F5DEB3"/>')
        
        # Add pattern overlay
        if pattern != "solid":
            body_parts.append(cls._generate_pattern(pattern, cx, cy, head_r))
        
        return '\n'.join(body_parts)
    
    @classmethod
    def _generate_pattern(cls, pattern: str, cx: int, cy: int, radius: int) -> str:
        """Generate pattern overlay"""
        if pattern == "spots":
            spots = []
            for i in range(8):
                angle = (i / 8) * 2 * math.pi
                x = cx + math.cos(angle) * (radius * 0.6)
                y = cy + math.sin(angle) * (radius * 0.6)
                spots.append(f'<circle cx="{x}" cy="{y}" r="15" fill="#000" opacity="0.3"/>')
            return '\n'.join(spots)
        
        elif pattern == "stripes":
            stripes = []
            for i in range(5):
                y = cy - radius + (i * radius * 0.5)
                stripes.append(f'<rect x="{cx-radius}" y="{y}" width="{radius*2}" height="15" fill="#000" opacity="0.2"/>')
            return '\n'.join(stripes)
        
        elif pattern == "stars":
            stars = []
            for i in range(6):
                angle = (i / 6) * 2 * math.pi
                x = cx + math.cos(angle) * (radius * 0.7)
                y = cy + math.sin(angle) * (radius * 0.7)
                stars.append(f'<text x="{x}" y="{y}" font-size="20" fill="gold" text-anchor="middle">★</text>')
            return '\n'.join(stars)
        
        return ""
    
    @classmethod
    def _generate_face(cls, expression: str, width: int, height: int) -> str:
        """Generate facial features"""
        cx, cy = width // 2, height // 2
        
        face_parts = []
        
        # Eyes
        eye_y = cy - 10
        eye_spacing = 40
        
        if expression in ["happy", "excited", "laughing"]:
            # Happy eyes (curved)
            face_parts.append(f'<ellipse cx="{cx-eye_spacing}" cy="{eye_y}" rx="15" ry="20" fill="#000"/>')
            face_parts.append(f'<ellipse cx="{cx+eye_spacing}" cy="{eye_y}" rx="15" ry="20" fill="#000"/>')
            face_parts.append(f'<ellipse cx="{cx-eye_spacing}" cy="{eye_y-5}" rx="5" ry="8" fill="#FFF"/>')
            face_parts.append(f'<ellipse cx="{cx+eye_spacing}" cy="{eye_y-5}" rx="5" ry="8" fill="#FFF"/>')
        
        elif expression == "winking":
            # One eye open, one closed
            face_parts.append(f'<ellipse cx="{cx-eye_spacing}" cy="{eye_y}" rx="15" ry="20" fill="#000"/>')
            face_parts.append(f'<line x1="{cx+eye_spacing-15}" y1="{eye_y}" x2="{cx+eye_spacing+15}" y2="{eye_y}" stroke="#000" stroke-width="3"/>')
        
        elif expression == "laser_eyes":
            # Glowing eyes
            face_parts.append(f'<circle cx="{cx-eye_spacing}" cy="{eye_y}" r="15" fill="#FF0000" opacity="0.8"/>')
            face_parts.append(f'<circle cx="{cx+eye_spacing}" cy="{eye_y}" r="15" fill="#FF0000" opacity="0.8"/>')
            face_parts.append(f'<circle cx="{cx-eye_spacing}" cy="{eye_y}" r="8" fill="#FFFF00"/>')
            face_parts.append(f'<circle cx="{cx+eye_spacing}" cy="{eye_y}" r="8" fill="#FFFF00"/>')
        
        else:
            # Normal eyes
            face_parts.append(f'<circle cx="{cx-eye_spacing}" cy="{eye_y}" r="15" fill="#000"/>')
            face_parts.append(f'<circle cx="{cx+eye_spacing}" cy="{eye_y}" r="15" fill="#000"/>')
            face_parts.append(f'<circle cx="{cx-eye_spacing-3}" cy="{eye_y-3}" r="5" fill="#FFF"/>')
            face_parts.append(f'<circle cx="{cx+eye_spacing-3}" cy="{eye_y-3}" r="5" fill="#FFF"/>')
        
        # Nose
        nose_y = cy + 20
        face_parts.append(f'<ellipse cx="{cx}" cy="{nose_y}" rx="12" ry="8" fill="#8B4513"/>')
        
        # Mouth
        mouth_y = cy + 45
        
        if expression in ["happy", "excited", "laughing"]:
            # Smile
            face_parts.append(f'<path d="M {cx-30} {mouth_y} Q {cx} {mouth_y+20} {cx+30} {mouth_y}" stroke="#000" stroke-width="3" fill="none"/>')
        elif expression in ["surprised", "excited"]:
            # Open mouth
            face_parts.append(f'<ellipse cx="{cx}" cy="{mouth_y}" rx="15" ry="20" fill="#000"/>')
        elif expression == "zen":
            # Slight smile
            face_parts.append(f'<path d="M {cx-20} {mouth_y} Q {cx} {mouth_y+5} {cx+20} {mouth_y}" stroke="#000" stroke-width="2" fill="none"/>')
        else:
            # Neutral
            face_parts.append(f'<line x1="{cx-20}" y1="{mouth_y}" x2="{cx+20}" y2="{mouth_y}" stroke="#000" stroke-width="2"/>')
        
        return '\n'.join(face_parts)
    
    @classmethod
    def _generate_accessory(cls, accessory: str, width: int, height: int) -> str:
        """Generate accessories"""
        cx, cy = width // 2, height // 2
        
        if accessory == "none":
            return ""
        
        elif accessory == "simple_hat":
            return f'<rect x="{cx-50}" y="{cy-150}" width="100" height="20" fill="#8B0000" stroke="#000" stroke-width="2"/>'
        
        elif accessory == "crown":
            return f'''
                <polygon points="{cx-40},{cy-140} {cx-20},{cy-160} {cx},{cy-140} {cx+20},{cy-160} {cx+40},{cy-140} {cx+40},{cy-120} {cx-40},{cy-120}" 
                         fill="#FFD700" stroke="#000" stroke-width="2"/>
            '''
        
        elif accessory == "sunglasses":
            return f'''
                <rect x="{cx-60}" y="{cy-20}" width="40" height="25" rx="5" fill="#000" opacity="0.8"/>
                <rect x="{cx+20}" y="{cy-20}" width="40" height="25" rx="5" fill="#000" opacity="0.8"/>
                <line x1="{cx-20}" y1="{cy-7}" x2="{cx+20}" y2="{cy-7}" stroke="#000" stroke-width="3"/>
            '''
        
        elif accessory == "halo":
            return f'<ellipse cx="{cx}" cy="{cy-160}" rx="60" ry="15" fill="none" stroke="#FFD700" stroke-width="5" opacity="0.8"/>'
        
        elif accessory == "wizard_hat":
            return f'''
                <polygon points="{cx},{cy-180} {cx-60},{cy-120} {cx+60},{cy-120}" fill="#4B0082" stroke="#000" stroke-width="2"/>
                <ellipse cx="{cx}" cy="{cy-120}" rx="70" ry="15" fill="#4B0082" stroke="#000" stroke-width="2"/>
            '''
        
        elif accessory == "golden_crown":
            return f'''
                <polygon points="{cx-50},{cy-140} {cx-30},{cy-170} {cx-10},{cy-145} {cx+10},{cy-170} {cx+30},{cy-145} {cx+50},{cy-170} {cx+50},{cy-120} {cx-50},{cy-120}" 
                         fill="#FFD700" stroke="#DAA520" stroke-width="3"/>
                <circle cx="{cx}" cy="{cy-165}" r="8" fill="#FF0000"/>
            '''
        
        return ""
    
    @classmethod
    def _generate_special_effects(cls, special: str, width: int, height: int) -> str:
        """Generate special effects"""
        cx, cy = width // 2, height // 2
        
        if special == "none":
            return ""
        
        elif special == "sparkles":
            sparkles = []
            positions = [(cx-100, cy-100), (cx+100, cy-100), (cx-100, cy+100), (cx+100, cy+100)]
            for x, y in positions:
                sparkles.append(f'<text x="{x}" y="{y}" font-size="30" fill="gold">✨</text>')
            return '\n'.join(sparkles)
        
        elif special == "glow":
            return f'<circle cx="{cx}" cy="{cy}" r="140" fill="none" stroke="#FFD700" stroke-width="5" opacity="0.3"/>'
        
        elif special == "aura":
            return f'''
                <circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="#9400D3" stroke-width="3" opacity="0.5"/>
                <circle cx="{cx}" cy="{cy}" r="160" fill="none" stroke="#4B0082" stroke-width="2" opacity="0.3"/>
            '''
        
        elif special == "transcendent":
            return f'''
                <circle cx="{cx}" cy="{cy}" r="170" fill="none" stroke="#FFD700" stroke-width="5" opacity="0.6"/>
                <circle cx="{cx}" cy="{cy}" r="180" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.4"/>
                <text x="{cx}" y="{cy-190}" font-size="40" fill="gold" text-anchor="middle">👑</text>
            '''
        
        return ""
    
    @classmethod
    def generate_thumbnail(cls, dna: MonkeyDNA, size: int = 100) -> str:
        """Generate small thumbnail version"""
        return cls.generate_svg(dna, width=size, height=size)


def main():
    """Test visualizer"""
    from src.genetics import GeneticsEngine
    
    print("🎨 ForkMonkey Visualizer Test\n")
    
    # Generate random monkey
    dna = GeneticsEngine.generate_random_dna()
    
    print("Generating SVG...")
    svg = MonkeyVisualizer.generate_svg(dna)
    
    # Save to file
    with open("test_monkey.svg", "w") as f:
        f.write(svg)
    
    print("✅ SVG saved to test_monkey.svg")
    print(f"   Traits: {', '.join([t.value for t in dna.traits.values()])}")


if __name__ == "__main__":
    main()
