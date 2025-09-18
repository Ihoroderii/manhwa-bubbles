from PIL import Image, ImageDraw, ImageFont
import math

def bubble_heart(draw, xy, text):
    """Heart-shaped bubble (romantic)."""
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
    """Spiky flame-like bubble (rage)."""
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
    """Bubble with glowing aura (magic/divine)."""
    x, y, w, h = xy
    for r in range(0, 20, 4):
        draw.ellipse((x-r, y-r, x+w+r, y+h+r), outline="yellow", width=2)
    draw.ellipse((x, y, x+w, y+h), fill="white", outline="gold", width=3)
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="black")

def bubble_scratchy(draw, xy, text):
    """Scratchy/rough border bubble (madness/creepy)."""
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


img = Image.new("RGB", (900, 600), "lightgray")
draw = ImageDraw.Draw(img)

bubble_heart(draw, (50, 50, 200, 150), "Love~")
bubble_spiky(draw, (300, 50, 200, 150), "ANGRY!!")
bubble_glow(draw, (550, 50, 200, 150), "Divine voice")
bubble_scratchy(draw, (200, 300, 250, 150), "Insane thoughts...")

img.show()