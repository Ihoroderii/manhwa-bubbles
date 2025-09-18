"""
Demo script showing how to use the manhwa_bubbles library.
Run this script to see examples of all bubble and narration types.
"""

from PIL import Image, ImageDraw
from manhwa_bubbles import (
    speech_bubble, 
    narrator_plain, 
    narrator_borderless,
    narrator_dashed, 
    narrator_dark, 
    narrator_wavy
)


def demo_speech_bubbles():
    """Demonstrates all speech bubble types."""
    print("Creating speech bubbles demo...")
    
    # Create canvas
    img = Image.new("RGB", (800, 600), "lightblue")
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((10, 10), "Manhwa Speech Bubbles Demo", fill="black")
    
    # Examples of different bubble types
    speech_bubble(draw, (50, 50, 200, 100), "Normal speech", "oval")
    speech_bubble(draw, (300, 50, 200, 100), "Narration", "rect")
    speech_bubble(draw, (550, 50, 200, 100), "Thinking...", "cloud")
    
    speech_bubble(draw, (50, 250, 200, 120), "HEY!!", "jagged")
    speech_bubble(draw, (300, 250, 200, 100), "I'm nervous...", "wavy")
    speech_bubble(draw, (550, 250, 200, 100), "Dark thoughts", "black")
    
    # Add labels
    draw.text((50, 160), "Normal", fill="black")
    draw.text((300, 160), "Narration", fill="black")
    draw.text((550, 160), "Thought", fill="black")
    draw.text((50, 380), "Shouting", fill="black")
    draw.text((300, 360), "Nervous", fill="black")
    draw.text((550, 360), "Dark", fill="black")
    
    img.save("examples/speech_bubbles_demo.png")
    print("Saved: examples/speech_bubbles_demo.png")
    return img


def demo_narration_boxes():
    """Demonstrates all narration box types."""
    print("Creating narration boxes demo...")
    
    # Create canvas
    img = Image.new("RGB", (800, 600), "lightgray")
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((10, 10), "Manhwa Narration Boxes Demo", fill="black")
    
    # Examples of each narrator type
    narrator_plain(draw, (50, 50, 250, 80), "Plain narration box")
    narrator_borderless(draw, (350, 70, 200, 50), "Borderless narration")
    narrator_dashed(draw, (50, 180, 250, 80), "Dashed border narration")
    narrator_dark(draw, (350, 180, 250, 80), "Dark narration box")
    narrator_wavy(draw, (200, 320, 300, 100), "Wavy narration (dreamy)")
    
    # Add labels
    draw.text((50, 140), "Plain", fill="black")
    draw.text((350, 130), "Borderless", fill="black")
    draw.text((50, 270), "Dashed", fill="black")
    draw.text((350, 270), "Dark", fill="black")
    draw.text((200, 430), "Wavy", fill="black")
    
    img.save("examples/narration_boxes_demo.png")
    print("Saved: examples/narration_boxes_demo.png")
    return img


def demo_comic_panel():
    """Creates a sample comic panel using multiple elements."""
    print("Creating comic panel demo...")
    
    # Create canvas
    img = Image.new("RGB", (1000, 700), "white")
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((10, 10), "Sample Comic Panel", fill="black")
    
    # Scene setup narration
    narrator_plain(draw, (50, 50, 300, 60), "Meanwhile, in the dark forest...")
    
    # Character dialogue
    speech_bubble(draw, (100, 150, 180, 80), "Who's there?", "oval", "down")
    speech_bubble(draw, (400, 120, 200, 90), "Show yourself!", "jagged", "left")
    
    # Thought bubble
    speech_bubble(draw, (650, 200, 180, 100), "This feels dangerous...", "cloud", "down")
    
    # Internal monologue
    narrator_dark(draw, (50, 350, 350, 80), "Little did she know, danger was approaching...")
    
    # Nervous speech
    speech_bubble(draw, (500, 400, 200, 80), "I should run...", "wavy", "up")
    
    # Sound effect area
    narrator_borderless(draw, (700, 450, 200, 50), "CRACK!")
    
    # Flashback narration
    narrator_dashed(draw, (100, 550, 300, 80), "She remembered her father's warning...")
    
    img.save("examples/comic_panel_demo.png")
    print("Saved: examples/comic_panel_demo.png")
    return img


def main():
    """Run all demos."""
    print("Running Manhwa Bubbles Library Demo")
    print("=" * 40)
    
    try:
        # Run demos
        speech_img = demo_speech_bubbles()
        narration_img = demo_narration_boxes()
        comic_img = demo_comic_panel()
        
        print("\nDemo completed successfully!")
        print("Check the 'examples/' folder for generated images.")
        
        # Optionally show the images (comment out if running headless)
        # speech_img.show()
        # narration_img.show() 
        # comic_img.show()
        
    except Exception as e:
        print(f"Error running demo: {e}")
        print("Make sure you have installed the manhwa_bubbles package:")
        print("pip install -e .")


if __name__ == "__main__":
    main()