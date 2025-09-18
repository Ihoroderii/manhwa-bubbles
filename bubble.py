from PIL import Image, ImageDraw, ImageFont
import math, random


def narrator_plain(draw, xy, text):
    """Plain rectangular narration box."""
    x, y, w, h = xy
    draw.rectangle((x, y, x+w, y+h), fill="white", outline="black", width=2)
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="black")

def narrator_borderless(draw, xy, text):
    """Borderless floating narration (just text)."""
    x, y, w, h = xy
    font = ImageFont.load_default()
    draw.text((x, y), text, font=font, fill="black")

def narrator_dashed(draw, xy, text):
    """Dashed border narration box."""
    x, y, w, h = xy
    # Dashed rectangle (drawn manually)
    step = 10
    for i in range(x, x+w, step):
        draw.line((i, y, min(i+5, x+w), y), fill="black", width=2)  # top
        draw.line((i, y+h, min(i+5, x+w), y+h), fill="black", width=2)  # bottom
    for j in range(y, y+h, step):
        draw.line((x, j, x, min(j+5, y+h)), fill="black", width=2)  # left
        draw.line((x+w, j, x+w, min(j+5, y+h)), fill="black", width=2)  # right
    draw.rectangle((x, y, x+w, y+h), fill="white")
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="black")

def narrator_dark(draw, xy, text):
    """Dark/ominous narration box."""
    x, y, w, h = xy
    draw.rectangle((x, y, x+w, y+h), fill="black", outline="white", width=2)
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="white")

def narrator_wavy(draw, xy, text):
    """Wavy border narration box (dreamy/unstable)."""
    x, y, w, h = xy
    step = 10
    offset = 0
    path_top, path_bottom = [], []
    for i in range(x, x+w+1, step):
        offset = 5 if (i//step) % 2 == 0 else -5
        path_top.append((i, y+offset))
        path_bottom.append((i, y+h+offset))
    draw.line(path_top, fill="black", width=2)
    draw.line(path_bottom, fill="black", width=2)
    # left and right wavy lines
    path_left, path_right = [], []
    for j in range(y, y+h+1, step):
        offset = 5 if (j//step) % 2 == 0 else -5
        path_left.append((x+offset, j))
        path_right.append((x+w+offset, j))
    draw.line(path_left, fill="black", width=2)
    draw.line(path_right, fill="black", width=2)
    # fill background
    draw.rectangle((x, y, x+w, y+h), fill="white")
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="black")

def draw_tail(draw, x, y, direction="down"):
    """Draws a simple triangular tail pointing in a direction."""
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
    """Draws different manhwa bubble types."""
    x, y, w, h = xy

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
    else:
        text_color = "black"

    # Tail
    if bubble_type not in ["rect", "wavy"]:  # narration usually no tail
        draw_tail(draw, x+w//2, y+h, direction=tail_dir)

    # Add text
    font = ImageFont.load_default()
    text_color = "black" if bubble_type != "black" else "white"
    draw.text((x+10, y+10), text, font=font, fill=text_color)


# Create canvas
img = Image.new("RGB", (800, 600), "lightblue")
draw = ImageDraw.Draw(img)

# Examples
speech_bubble(draw, (50, 50, 200, 100), "Normal speech", "oval")
speech_bubble(draw, (300, 50, 200, 100), "Narration", "rect")
speech_bubble(draw, (550, 50, 200, 100), "Thinking...", "cloud")
speech_bubble(draw, (50, 250, 200, 120), "HEY!!", "jagged")
speech_bubble(draw, (300, 250, 200, 100), "I'm nervous...", "wavy")
speech_bubble(draw, (550, 250, 200, 100), "Dark thoughts", "black")

img.show()

# Create canvas
img2 = Image.new("RGB", (800, 600), "lightgray")
draw2 = ImageDraw.Draw(img2)

# Examples of each narrator type
narrator_plain(draw2, (50, 50, 250, 80), "Plain narration")
narrator_borderless(draw2, (350, 70, 200, 50), "Borderless narration")
narrator_dashed(draw2, (50, 180, 250, 80), "Dashed border narration")
narrator_dark(draw2, (350, 180, 250, 80), "Dark narration")
narrator_wavy(draw2, (200, 320, 300, 100), "Wavy narration (dreamy)")

img2.show()

