"""
Speech bubble functions for manhwa-style comics.
"""

from PIL import ImageDraw, ImageFont
import math


def draw_tail(draw, x, y, direction="down"):
    """
    Draws a simple triangular tail pointing in a direction.
    
    Args:
        draw: PIL ImageDraw object
        x, y: Position coordinates for the tail
        direction: Direction for the tail ("down", "up", "left", "right")
    """
    if direction == "down":
        points = [(x, y), (x+20, y+30), (x-20, y+30)]
    elif direction == "up":
        points = [(x, y), (x+20, y-30), (x-20, y-30)]
    elif direction == "left":
        points = [(x, y), (x-30, y-20), (x-30, y+20)]
    else:  # right
        points = [(x, y), (x+30, y-20), (x+30, y+20)]
    draw.polygon(points, fill="white", outline="black")


def speech_bubble(draw, xy, text, bubble_type="oval", tail_dir="down"):
    """
    Draws different manhwa bubble types.
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for bubble position and size
        text: Text to display in the bubble
        bubble_type: Type of bubble ("oval", "rect", "cloud", "jagged", "wavy", "black")
        tail_dir: Direction for the speech tail ("down", "up", "left", "right")
    """
    x, y, w, h = xy
    text_color = "black"  # default

    if bubble_type == "oval":  # normal speech
        draw.ellipse((x, y, x+w, y+h), fill="white", outline="black", width=3)

    elif bubble_type == "rect":  # narration
        draw.rectangle((x, y, x+w, y+h), fill="white", outline="black", width=3)

    elif bubble_type == "cloud":  # thought
        for i in range(12):
            angle = 2*math.pi*i/12
            cx = x+w//2 + int((w//2)*math.cos(angle))
            cy = y+h//2 + int((h//2)*math.sin(angle))
            draw.ellipse((cx-15, cy-15, cx+15, cy+15), fill="white", outline="black")
        draw.ellipse((x, y, x+w, y+h), fill="white", outline="black")

    elif bubble_type == "jagged":  # shouting
        points = []
        num_points = 20
        for i in range(num_points):
            angle = 2*math.pi*i/num_points
            r = (w//2) + (15 if i % 2 == 0 else 5)
            px = x+w//2 + int(r*math.cos(angle))
            py = y+h//2 + int(r*math.sin(angle))
            points.append((px, py))
        draw.polygon(points, fill="white", outline="black")

    elif bubble_type == "wavy":  # nervous/shaky
        steps = 20
        path = []
        for i in range(steps+1):
            px = x + (w*i)//steps
            py = y + (h//2) + int(10*math.sin(i*0.8))
            path.append((px, py))
        draw.line(path, fill="black", width=3)
        draw.rectangle((x, y, x+w, y+h), fill="white")  # simple white box inside

    elif bubble_type == "black":  # evil/dark intent
        draw.ellipse((x, y, x+w, y+h), fill="black", outline="white", width=3)
        text_color = "white"

    # Tail
    if bubble_type not in ["rect", "wavy"]:  # narration usually no tail
        draw_tail(draw, x+w//2, y+h, direction=tail_dir)

    # Add text
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill=text_color)