import cairo
import math
import random

def create_manually_clipped_circles_square(ctx, cx, cy, base_size, text="MANUAL CLIP!", circle_style="varied", num_circles_per_side=5):
    """Create a square with circles manually clipped (not using ctx.clip())"""
    
    # Calculate base square
    half_size = base_size / 2
    
    # Generate overlapping circles for each side
    all_circles = generate_side_circles_manual(cx, cy, half_size, circle_style, num_circles_per_side)
    
    # Draw the main square FIRST
    draw_base_square(ctx, cx, cy, base_size)
    
    # Manually draw only the parts of circles that are inside the square
    for circle in all_circles:
        draw_circle_manually_clipped(ctx, circle, cx, cy, half_size)
    
    # Draw square outline for clean edges
    ctx.rectangle(cx - half_size, cy - half_size, base_size, base_size)
    ctx.set_source_rgba(0, 0, 0, 0.7)
    ctx.set_line_width(2.5)
    ctx.stroke()
    
    # Add text
    draw_overlap_text(ctx, cx, cy, text)

def generate_side_circles_manual(cx, cy, half_size, style, num_per_side):
    """Generate circles that definitely extend outside the square"""
    
    all_circles = []
    
    for i in range(num_per_side):
        # Top side circles - positioned to extend upward
        circle_x = cx + (i - num_per_side/2) * (half_size * 0.6)
        circle_y = cy - half_size + 15  # Close to top edge
        radius = half_size * 0.5  # Large enough to extend outside
        
        all_circles.append({
            'x': circle_x,
            'y': circle_y,
            'rx': radius,
            'ry': radius,
            'side': 'top',
            'color': (1.0, 0.8, 0.8)  # Light red
        })
        
        # Right side circles - positioned to extend rightward  
        circle_x = cx + half_size - 15  # Close to right edge
        circle_y = cy + (i - num_per_side/2) * (half_size * 0.6)
        
        all_circles.append({
            'x': circle_x,
            'y': circle_y,
            'rx': radius,
            'ry': radius,
            'side': 'right',
            'color': (0.8, 1.0, 0.8)  # Light green
        })
        
        # Bottom side circles - positioned to extend downward
        circle_x = cx + (i - num_per_side/2) * (half_size * 0.6)
        circle_y = cy + half_size - 15  # Close to bottom edge
        
        all_circles.append({
            'x': circle_x,
            'y': circle_y,
            'rx': radius,
            'ry': radius,
            'side': 'bottom',
            'color': (0.8, 0.8, 1.0)  # Light blue
        })
        
        # Left side circles - positioned to extend leftward
        circle_x = cx - half_size + 15  # Close to left edge
        circle_y = cy + (i - num_per_side/2) * (half_size * 0.6)
        
        all_circles.append({
            'x': circle_x,
            'y': circle_y,
            'rx': radius,
            'ry': radius,
            'side': 'left',
            'color': (1.0, 1.0, 0.8)  # Light yellow
        })
    
    return all_circles

def draw_circle_manually_clipped(ctx, circle, square_cx, square_cy, square_half_size):
    """Draw only the part of a circle that's inside the square"""
    
    # Square boundaries
    square_left = square_cx - square_half_size
    square_right = square_cx + square_half_size
    square_top = square_cy - square_half_size
    square_bottom = square_cy + square_half_size
    
    # Sample points around the circle and only draw those inside the square
    cx, cy = circle['x'], circle['y']
    rx, ry = circle['rx'], circle['ry']
    
    # Create a path with only the inside parts
    inside_points = []
    num_samples = 100
    
    for i in range(num_samples):
        angle = (2 * math.pi * i) / num_samples
        px = cx + rx * math.cos(angle)
        py = cy + ry * math.sin(angle)
        
        # Check if point is inside square
        if (square_left <= px <= square_right and 
            square_top <= py <= square_bottom):
            inside_points.append((px, py))
    
    if len(inside_points) < 3:
        return  # Not enough points to draw
    
    # Draw the inside part as a filled shape
    ctx.move_to(inside_points[0][0], inside_points[0][1])
    for px, py in inside_points[1:]:
        ctx.line_to(px, py)
    ctx.close_path()
    
    # Fill with circle color
    ctx.set_source_rgb(*circle['color'])
    ctx.fill_preserve()
    
    # Outline
    ctx.set_source_rgba(0, 0, 0, 0.5)
    ctx.set_line_width(1.5)
    ctx.stroke()

def draw_base_square(ctx, cx, cy, size):
    """Draw the base square"""
    
    half_size = size / 2
    
    # Square path
    ctx.rectangle(cx - half_size, cy - half_size, size, size)
    
    # Light square fill
    ctx.set_source_rgba(1.0, 1.0, 1.0, 0.9)
    ctx.fill()

def draw_overlap_text(ctx, cx, cy, text):
    """Draw text in center"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(12)
    
    text_extents = ctx.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height
    
    text_x = cx - text_width / 2
    text_y = cy + text_height / 2
    
    # Text shadow
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.move_to(text_x + 1, text_y + 1)
    ctx.show_text(text)
    
    # Main text
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)

def create_manual_clipping_demo():
    """Create demo with manual clipping (no ctx.clip())"""
    
    random.seed(777)
    
    WIDTH, HEIGHT = 800, 600
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(0.95, 0.95, 0.95)
    ctx.paint()
    
    # Test manual clipping
    create_manually_clipped_circles_square(ctx, 150, 150, 120, "MANUAL 1!", "varied", 3)
    create_manually_clipped_circles_square(ctx, 350, 150, 120, "MANUAL 2!", "varied", 4)
    create_manually_clipped_circles_square(ctx, 550, 150, 120, "MANUAL 3!", "varied", 5)
    
    create_manually_clipped_circles_square(ctx, 200, 350, 140, "BIG MANUAL!", "varied", 4)
    create_manually_clipped_circles_square(ctx, 450, 350, 140, "HUGE MANUAL!", "varied", 6)
    
    create_manually_clipped_circles_square(ctx, 300, 500, 160, "MEGA MANUAL!", "varied", 7)
    
    # Title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(20)
    ctx.set_source_rgb(0.2, 0.2, 0.4)
    ctx.move_to(200, 50)
    ctx.show_text("MANUAL CLIPPING - NO PARTS OUTSIDE SQUARE")
    
    surface.write_to_png("manual_clipping.png")
    print("✅ Manual clipping saved as 'manual_clipping.png'")

if __name__ == "__main__":
    create_manual_clipping_demo()
    print("✂️ Created manual clipping! Circles should be completely contained in squares! 🔵⬜✨")