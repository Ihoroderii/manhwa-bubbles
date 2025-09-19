import cairo, math

WIDTH, HEIGHT = 500, 400
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(1, 1, 1)
ctx.paint()

# Ellipse parameters
cx, cy = 250, 200   # center
rx, ry = 150, 100   # radii

# Variable stroke thickness function
def stroke_width(theta):
    # Thin at top, thick at bottom
    return 3 + 6 * (0.5 + 0.5 * math.sin(theta))

# Tail placement
tail_angle = math.pi/2   # bottom (90°)
tail_width = 0.5         # radians: size of gap

# Compute ellipse outline with gap for tail
outer, inner = [], []
steps = 300
for i in range(steps+1):
    theta = 2*math.pi*i/steps
    # skip arc where tail attaches
    if tail_angle-tail_width/2 < theta < tail_angle+tail_width/2:
        continue

    x = cx + rx*math.cos(theta)
    y = cy + ry*math.sin(theta)

    # Normal vector
    nx = math.cos(theta) / rx
    ny = math.sin(theta) / ry
    norm = math.sqrt(nx*nx + ny*ny)
    nx, ny = nx/norm, ny/norm

    w = stroke_width(theta)
    outer.append((x + nx*w/2, y + ny*w/2))
    inner.append((x - nx*w/2, y - ny*w/2))

# Draw ellipse (as filled polygon with variable width)
ctx.set_source_rgb(0, 0, 0)
ctx.move_to(*outer[0])
for p in outer:
    ctx.line_to(*p)
for p in reversed(inner):
    ctx.line_to(*p)
ctx.close_path()
ctx.fill()

# --- Draw smoother, natural tail ---
tail_tip = (cx, cy + ry + 70)      # tip of tail
left_attach = (cx - 25, cy + ry)   # left base of gap
right_attach = (cx + 25, cy + ry)  # right base of gap

ctx.move_to(*left_attach)
ctx.curve_to(cx - 15, cy + ry + 20, cx - 10, cy + ry + 40, *tail_tip)
ctx.curve_to(cx + 10, cy + ry + 40, cx + 15, cy + ry + 20, *right_attach)
ctx.close_path()

# Fill white
ctx.set_source_rgb(1, 1, 1)
ctx.fill_preserve()

# Outline black
ctx.set_source_rgb(0, 0, 0)
ctx.set_line_width(2)
ctx.stroke()

# Save
surface.write_to_png("ellipse_natural_tail.png")
print("✅ Saved bubble with natural white tail -> ellipse_natural_tail.png")


import gi
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo
import cairo

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 300)
ctx = cairo.Context(surface)

layout = PangoCairo.create_layout(ctx)
fontdesc = Pango.FontDescription("Sans 20")
layout.set_font_description(fontdesc)
layout.set_width(200 * Pango.SCALE)  # wrap at 200px
layout.set_text("This is a long piece of text that wraps automatically inside the bubble.")

ctx.set_source_rgb(0, 0, 0)
ctx.move_to(100, 100)
PangoCairo.show_layout(ctx, layout)

surface.write_to_png("text_wrapped.png")

import cairo

WIDTH, HEIGHT = 500, 300
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

# White background
ctx.set_source_rgb(1, 1, 1)
ctx.paint()

# 👉 Use Bubble Sans (installed .otf)
ctx.select_font_face("Bubble Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(36)

# Draw text
ctx.set_source_rgb(0, 0, 0)  # black text
ctx.move_to(50, 150)
ctx.show_text("I WON'T FORGIVE YOU!")

surface.write_to_png("bubble_sans_test.png")
print("✅ Saved text with Bubble Sans -> bubble_sans_test.png")

