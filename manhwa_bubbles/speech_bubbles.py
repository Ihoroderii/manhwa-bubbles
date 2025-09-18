"""
Speech bubble functions for manhwa-style comics.
"""

from PIL import ImageDraw, ImageFont
import math


def bubble_heart(draw, xy, text):
    """
    Heart-shaped bubble (romantic).
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for bubble position and size
        text: Text to display in the bubble
    """
    x, y, w, h = xy
    points = []
    for t in range(0, 360, 5):
        rad = math.radians(t)
        px = x + w//2 + int(16*math.sin(rad)**3 * (w/20))
        py = y + h//2 - int((13*math.cos(rad) - 5*math.cos(2*rad) - 2*math.cos(3*rad) - math.cos(4*rad)) * (h/20))
        points.append((px, py))
    draw.polygon(points, fill="white", outline="red", width=3)
    font = ImageFont.load_default()
    draw.text((x+w//3, y+h//3), text, font=font, fill="red")


def bubble_spiky(draw, xy, text):
    """
    Spiky flame-like bubble (rage).
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for bubble position and size
        text: Text to display in the bubble
    """
    x, y, w, h = xy
    points = []
    num_points = 40
    for i in range(num_points):
        angle = 2*math.pi*i/num_points
        r = (w//2) + (20 if i % 2 == 0 else 5)
        px = x+w//2 + int(r*math.cos(angle))
        py = y+h//2 + int(r*math.sin(angle))
        points.append((px, py))
    draw.polygon(points, fill="white", outline="black")
    font = ImageFont.load_default()
    draw.text((x+w//3, y+h//3), text, font=font, fill="black")


def bubble_glow(draw, xy, text):
    """
    Bubble with glowing aura (magic/divine).
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for bubble position and size
        text: Text to display in the bubble
    """
    x, y, w, h = xy
    for r in range(0, 20, 4):
        draw.ellipse((x-r, y-r, x+w+r, y+h+r), outline="yellow", width=2)
    draw.ellipse((x, y, x+w, y+h), fill="white", outline="gold", width=3)
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="black")


def bubble_scratchy(draw, xy, text):
    """
    Scratchy/rough border bubble (madness/creepy).
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for bubble position and size
        text: Text to display in the bubble
    """
    x, y, w, h = xy
    for i in range(100):
        px1 = x + int(math.cos(i)*w/2) + w//2
        py1 = y + int(math.sin(i)*h/2) + h//2
        px2 = px1 + (math.sin(i*3)*10)
        py2 = py1 + (math.cos(i*5)*10)
        draw.line((px1, py1, px2, py2), fill="black", width=1)
    draw.rectangle((x, y, x+w, y+h), fill="white")
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="black")


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
        bubble_type: Type of bubble ("oval", "rect", "cloud", "jagged", "wavy", "black", "heart", "spiky", "glow", "scratchy")
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
        
    elif bubble_type == "heart":  # romantic
        bubble_heart(draw, xy, text)
        return  # heart bubble handles its own text
        
    elif bubble_type == "spiky":  # rage/flame
        bubble_spiky(draw, xy, text)
        return  # spiky bubble handles its own text
        
    elif bubble_type == "glow":  # magic/divine
        bubble_glow(draw, xy, text)
        return  # glow bubble handles its own text
        
    elif bubble_type == "scratchy":  # madness/creepy
        bubble_scratchy(draw, xy, text)
        return  # scratchy bubble handles its own text

    # Tail (skip for special bubbles that handle their own rendering)
    if bubble_type not in ["rect", "wavy", "heart", "spiky", "glow", "scratchy"]:
        draw_tail(draw, x+w//2, y+h, direction=tail_dir)

    # Add text (skip for special bubbles that handle their own text)
    if bubble_type not in ["heart", "spiky", "glow", "scratchy"]:
        font = ImageFont.load_default()
        draw.text((x+10, y+10), text, font=font, fill=text_color)