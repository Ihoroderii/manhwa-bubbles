import cairo
import math
import random

def create_overlapping_circles_square(ctx, cx, cy, base_size, text="OVERLAP!", circle_style="varied", num_circles_per_side=5):
    """Create a square with overlapping circles/ovals on all sides"""
    
    # Calculate base square
    half_size = base_size / 2
    
    # Generate overlapping circles for each side
    all_circles = generate_side_circles(cx, cy, half_size, circle_style, num_circles_per_side)
    
    # Draw the main square FIRST (will be under the circles)
    draw_base_square(ctx, cx, cy, base_size)
    
    # CRITICAL: Set clipping region to EXACTLY the square area
    ctx.save()
    ctx.rectangle(cx - half_size, cy - half_size, base_size, base_size)
    ctx.clip()
    
    # Draw all circles - ONLY parts inside square will be visible
    draw_overlapping_circles(ctx, all_circles, cx, cy, base_size)
    
    # Restore clipping
    ctx.restore()
    
    # Draw only the parts of square border that are NOT crossed by circles
    draw_uncrossed_square_border(ctx, all_circles, cx, cy, half_size)
    
    # Find and emphasize only the part of circle borders that are INSIDE the square
    emphasize_border_crossing_pixels(ctx, all_circles, cx, cy, half_size)
    
    # Add text
    draw_overlap_text(ctx, cx, cy, text)

def generate_side_circles(cx, cy, half_size, style, num_per_side):
    """Generate circles/ovals for each side of the square"""
    
    all_circles = []
    
    # Define the four sides
    sides = [
        ("top", cx - half_size, cy - half_size, cx + half_size, cy - half_size),
        ("right", cx + half_size, cy - half_size, cx + half_size, cy + half_size),
        ("bottom", cx + half_size, cy + half_size, cx - half_size, cy + half_size),
        ("left", cx - half_size, cy + half_size, cx - half_size, cy - half_size)
    ]
    
    circle_id = 0
    for side_name, start_x, start_y, end_x, end_y in sides:
        side_circles = generate_circles_for_side(
            start_x, start_y, end_x, end_y, side_name, style, num_per_side, half_size, circle_id
        )
        all_circles.extend(side_circles)
        circle_id += len(side_circles)
    
    return all_circles

def generate_circles_for_side(start_x, start_y, end_x, end_y, side_name, style, num_circles, base_half_size, start_id):
    """Generate overlapping circles along one side"""
    
    circles = []
    
    for i in range(num_circles):
        # Position along the side
        if num_circles == 1:
            t = 0.5
        else:
            t = i / (num_circles - 1)
        
        # Base position on the side
        side_x = start_x + t * (end_x - start_x)
        side_y = start_y + t * (end_y - start_y)
        
        # Calculate outward direction from square
        if side_name == "top":
            normal_x, normal_y = 0, -1
        elif side_name == "right":
            normal_x, normal_y = 1, 0
        elif side_name == "bottom":
            normal_x, normal_y = 0, 1
        else:  # left
            normal_x, normal_y = -1, 0
        
        # Circle properties based on style
        if style == "varied":
            # Varied sizes and positions
            radius_x = random.uniform(15, 35)
            radius_y = random.uniform(15, 35)
            overlap_distance = random.uniform(10, 25)
            
        elif style == "uniform":
            # More uniform circles
            radius_x = random.uniform(20, 30)
            radius_y = radius_x  # Perfect circles
            overlap_distance = 15
            
        elif style == "ovals":
            # Elongated ovals
            if side_name in ["top", "bottom"]:
                radius_x = random.uniform(25, 40)  # Wide ovals
                radius_y = random.uniform(12, 20)
            else:  # left, right sides
                radius_x = random.uniform(12, 20)
                radius_y = random.uniform(25, 40)  # Tall ovals
            overlap_distance = random.uniform(8, 18)
            
        elif style == "bubbles":
            # Bubble-like varied circles
            base_radius = random.uniform(18, 32)
            radius_x = base_radius * random.uniform(0.8, 1.2)
            radius_y = base_radius * random.uniform(0.8, 1.2)
            overlap_distance = random.uniform(12, 22)
            
        elif style == "organic":
            # Organic, natural variation
            base_radius = random.uniform(16, 30)
            radius_x = base_radius * random.uniform(0.7, 1.3)
            radius_y = base_radius * random.uniform(0.7, 1.3)
            overlap_distance = random.uniform(8, 20)
            
        else:  # "small"
            # Small overlapping circles
            radius_x = random.uniform(8, 18)
            radius_y = random.uniform(8, 18)
            overlap_distance = random.uniform(5, 12)
        
        # Calculate circle center (overlapping with square)
        circle_x = side_x + normal_x * overlap_distance
        circle_y = side_y + normal_y * overlap_distance
        
        # Add some random variation to position
        variation_x = random.uniform(-8, 8)
        variation_y = random.uniform(-8, 8)
        circle_x += variation_x
        circle_y += variation_y
        
        circles.append({
            'x': circle_x,
            'y': circle_y,
            'rx': radius_x,
            'ry': radius_y,
            'side': side_name,
            'id': start_id + i
        })
    
    return circles

def draw_overlapping_circles(ctx, circles, cx, cy, base_size):
    """Draw all circles with overlapping effect"""
    
    # Sort circles by distance from center (draw farthest first)
    circles_with_distance = []
    for circle in circles:
        distance = math.sqrt((circle['x'] - cx)**2 + (circle['y'] - cy)**2)
        circles_with_distance.append((distance, circle))
    
    circles_with_distance.sort(key=lambda x: x[0], reverse=True)
    
    # Draw circles from farthest to nearest for proper overlapping
    for distance, circle in circles_with_distance:
        draw_single_circle(ctx, circle, cx, cy, base_size)

def draw_single_circle(ctx, circle, cx, cy, base_size):
    """Draw a single circle/oval with gradient"""
    
    # Save current state
    ctx.save()
    
    # Move to circle center and create ellipse
    ctx.translate(circle['x'], circle['y'])
    ctx.scale(circle['rx'], circle['ry'])
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    
    # Restore for gradient calculation
    ctx.restore()
    
    # Create gradient for this circle
    gradient = cairo.RadialGradient(
        circle['x'], circle['y'], 0,
        circle['x'], circle['y'], max(circle['rx'], circle['ry'])
    )
    
    # Different colors based on position/side
    if circle['side'] == 'top':
        gradient.add_color_stop_rgb(0, 1.0, 0.95, 0.9)   # Light cream
        gradient.add_color_stop_rgb(1, 0.9, 0.85, 0.75)  # Cream edge
    elif circle['side'] == 'right':
        gradient.add_color_stop_rgb(0, 0.95, 1.0, 0.9)   # Light green
        gradient.add_color_stop_rgb(1, 0.85, 0.9, 0.75)  # Green edge
    elif circle['side'] == 'bottom':
        gradient.add_color_stop_rgb(0, 0.9, 0.95, 1.0)   # Light blue
        gradient.add_color_stop_rgb(1, 0.75, 0.85, 0.9)  # Blue edge
    else:  # left
        gradient.add_color_stop_rgb(0, 1.0, 0.9, 0.95)   # Light pink
        gradient.add_color_stop_rgb(1, 0.9, 0.75, 0.85)  # Pink edge
    
    # Fill circle
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Enhanced circle outline - thicker and darker for contact emphasis
    ctx.set_source_rgba(0, 0, 0, 0.6)
    ctx.set_line_width(2.0)
    ctx.stroke()

def draw_base_square(ctx, cx, cy, size):
    """Draw the base square (will be partially covered by circles)"""
    
    half_size = size / 2
    
    # Square path
    ctx.rectangle(cx - half_size, cy - half_size, size, size)
    
    # Square gradient
    gradient = cairo.RadialGradient(cx, cy, 0, cx, cy, size * 0.7)
    gradient.add_color_stop_rgb(0, 1.0, 1.0, 1.0)      # White center
    gradient.add_color_stop_rgb(0.7, 0.95, 0.95, 0.98) # Light gray
    gradient.add_color_stop_rgb(1, 0.85, 0.85, 0.9)    # Gray edge
    
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Enhanced square outline - thicker and darker to emphasize contact with circles
    ctx.set_source_rgba(0, 0, 0, 0.7)
    ctx.set_line_width(2.5)
    ctx.stroke()

def emphasize_border_crossing_pixels(ctx, all_circles, cx, cy, half_size):
    """Emphasize only the part of circle borders that are INSIDE the square"""
    
    # Square boundaries
    square_left = cx - half_size
    square_right = cx + half_size
    square_top = cy - half_size
    square_bottom = cy + half_size
    
    # For each circle, find and emphasize only the border segments that are inside
    for circle in all_circles:
        inside_segments = find_crossing_border_segments(circle, square_left, square_right, square_top, square_bottom, all_circles)
        
        # Draw emphasis only on the inside border segments that don't overlap other circles
        draw_crossing_border_emphasis(ctx, inside_segments)

def find_crossing_border_segments(circle, square_left, square_right, square_top, square_bottom, all_circles):
    """Find segments of circle border that are INSIDE the square boundary and NOT covered by other circles"""
    
    crossing_segments = []
    
    # Get circle parameters
    cx, cy = circle['x'], circle['y']
    rx, ry = circle['rx'], circle['ry']
    
    # Sample points around the circle perimeter with high resolution
    num_samples = int(max(rx, ry) * 10)  # High resolution for smooth segments
    border_points = []
    
    for i in range(num_samples):
        angle = (2 * math.pi * i) / num_samples
        
        # Calculate point on circle perimeter
        px = cx + rx * math.cos(angle)
        py = cy + ry * math.sin(angle)
        
        # Check if this point is INSIDE the square
        is_inside = (px >= square_left and px <= square_right and 
                    py >= square_top and py <= square_bottom)
        
        # Check if this point is covered by any OTHER circle
        is_covered_by_other = False
        if is_inside:  # Only check coverage if point is inside square
            for other_circle in all_circles:
                if other_circle != circle:  # Don't check against itself
                    if point_inside_circle(px, py, other_circle):
                        is_covered_by_other = True
                        break
        
        # Point should be emphasized only if it's inside square AND not covered by other circles
        should_emphasize = is_inside and not is_covered_by_other
        
        border_points.append({
            'x': px,
            'y': py,
            'angle': angle,
            'should_emphasize': should_emphasize
        })
    
    # Find continuous segments of border points that should be emphasized
    current_segment = []
    
    for point in border_points:
        if point['should_emphasize']:
            current_segment.append(point)
        else:
            # End of emphasizable segment
            if len(current_segment) > 2:  # Only keep segments with multiple points
                crossing_segments.append(current_segment)
            current_segment = []
    
    # Handle wrap-around case (segment continues from end to beginning)
    if current_segment and crossing_segments and crossing_segments[0]:
        # Check if first segment and last segment should be connected
        first_segment = crossing_segments[0]
        if (abs(current_segment[-1]['angle'] - (first_segment[0]['angle'] + 2*math.pi)) < 0.2 or
            abs(current_segment[-1]['angle'] - first_segment[0]['angle']) < 0.2):
            # Connect the segments
            crossing_segments[0] = current_segment + first_segment
        else:
            if len(current_segment) > 2:
                crossing_segments.append(current_segment)
    elif len(current_segment) > 2:
        crossing_segments.append(current_segment)
    
    return crossing_segments

def draw_crossing_border_emphasis(ctx, inside_segments):
    """Draw emphasis on border segments that are INSIDE the square"""
    
    if not inside_segments:
        return
    
    ctx.set_source_rgba(0, 0, 0, 0.9)  # Strong black emphasis
    ctx.set_line_width(4.0)  # Thick line for visibility
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    
    for segment in inside_segments:
        if len(segment) < 2:
            continue
        
        # Draw the segment as a smooth curve
        ctx.move_to(segment[0]['x'], segment[0]['y'])
        
        for point in segment[1:]:
            ctx.line_to(point['x'], point['y'])
        
        ctx.stroke()

def find_border_crossing_pixels(circle, square_left, square_right, square_top, square_bottom):
    """Find all pixels of a circle that cross the square border"""
    
    crossing_pixels = []
    
    # Get circle parameters
    cx, cy = circle['x'], circle['y']
    rx, ry = circle['rx'], circle['ry']
    
    # Sample points around the circle perimeter with high resolution
    num_samples = int(max(rx, ry) * 6)  # High resolution sampling
    
    for i in range(num_samples):
        angle = (2 * math.pi * i) / num_samples
        
        # Calculate point on circle perimeter
        px = cx + rx * math.cos(angle)
        py = cy + ry * math.sin(angle)
        
        # Check if this pixel is ON or very close to a square border
        is_crossing = False
        border_type = None
        
        # Check left border crossing
        if (abs(px - square_left) < 1.5 and 
            square_top <= py <= square_bottom):
            is_crossing = True
            border_type = "left"
        
        # Check right border crossing  
        elif (abs(px - square_right) < 1.5 and 
              square_top <= py <= square_bottom):
            is_crossing = True
            border_type = "right"
        
        # Check top border crossing
        elif (abs(py - square_top) < 1.5 and 
              square_left <= px <= square_right):
            is_crossing = True
            border_type = "top"
        
        # Check bottom border crossing
        elif (abs(py - square_bottom) < 1.5 and 
              square_left <= px <= square_right):
            is_crossing = True
            border_type = "bottom"
        
        if is_crossing:
            crossing_pixels.append({
                'x': px,
                'y': py,
                'border': border_type,
                'circle_id': circle.get('id', 0)
            })
    
    return crossing_pixels

def draw_crossing_pixel_emphasis(ctx, crossing_pixels):
    """Draw emphasis on specific crossing pixels"""
    
    if not crossing_pixels:
        return
    
    # Group consecutive crossing pixels for smooth lines
    pixel_groups = group_consecutive_pixels(crossing_pixels)
    
    for group in pixel_groups:
        if len(group) < 2:
            # Single pixel - draw as small circle
            pixel = group[0]
            ctx.arc(pixel['x'], pixel['y'], 1.5, 0, 2 * math.pi)
            ctx.set_source_rgba(0, 0, 0, 0.9)
            ctx.fill()
        else:
            # Multiple consecutive pixels - draw as thick line
            ctx.set_source_rgba(0, 0, 0, 0.9)
            ctx.set_line_width(3.0)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            
            # Start path at first pixel
            ctx.move_to(group[0]['x'], group[0]['y'])
            
            # Draw through all pixels in group
            for pixel in group[1:]:
                ctx.line_to(pixel['x'], pixel['y'])
            
            ctx.stroke()

def group_consecutive_pixels(crossing_pixels):
    """Group consecutive crossing pixels that are close together"""
    
    if not crossing_pixels:
        return []
    
    # Sort pixels by border and position
    crossing_pixels.sort(key=lambda p: (p['border'], p['x'] + p['y']))
    
    groups = []
    current_group = [crossing_pixels[0]]
    
    for i in range(1, len(crossing_pixels)):
        prev_pixel = crossing_pixels[i-1]
        curr_pixel = crossing_pixels[i]
        
        # Check if pixels are consecutive (same border and close distance)
        distance = math.sqrt((curr_pixel['x'] - prev_pixel['x'])**2 + 
                           (curr_pixel['y'] - prev_pixel['y'])**2)
        
        if (curr_pixel['border'] == prev_pixel['border'] and 
            distance < 3.0):  # Pixels are close and on same border
            current_group.append(curr_pixel)
        else:
            # Start new group
            groups.append(current_group)
            current_group = [curr_pixel]
    
    # Add the last group
    groups.append(current_group)
    
    return groups

def draw_unified_contour(ctx, all_circles, cx, cy, half_size):
    """Draw the unified contour outline of the combined square+circles shape"""
    
    # Create a path that traces the outer contour of the combined shape
    ctx.set_source_rgba(0, 0, 0, 0.9)  # Strong black outline
    ctx.set_line_width(3.0)  # Thick contour line
    
    # Square boundaries
    square_left = cx - half_size
    square_right = cx + half_size
    square_top = cy - half_size
    square_bottom = cy + half_size
    
    # Trace the contour by following the outermost boundary
    # Start from top-left corner of square
    ctx.move_to(square_left, square_top)
    
    # Trace top edge, deviating around circles that extend beyond
    trace_edge_with_circles(ctx, "top", square_left, square_top, square_right, square_top, all_circles)
    
    # Trace right edge
    trace_edge_with_circles(ctx, "right", square_right, square_top, square_right, square_bottom, all_circles)
    
    # Trace bottom edge
    trace_edge_with_circles(ctx, "bottom", square_right, square_bottom, square_left, square_bottom, all_circles)
    
    # Trace left edge
    trace_edge_with_circles(ctx, "left", square_left, square_bottom, square_left, square_top, all_circles)
    
    # Close the path and stroke
    ctx.close_path()
    ctx.stroke()

def trace_edge_with_circles(ctx, edge_name, start_x, start_y, end_x, end_y, circles):
    """Trace an edge of the square, following circle contours where they extend beyond"""
    
    # Collect circles that affect this edge
    affecting_circles = []
    
    for circle in circles:
        if edge_affects_circle(edge_name, start_x, start_y, end_x, end_y, circle):
            affecting_circles.append(circle)
    
    if not affecting_circles:
        # No circles affect this edge, draw straight line
        ctx.line_to(end_x, end_y)
        return
    
    # Sort circles by position along the edge
    affecting_circles.sort(key=lambda c: get_circle_position_on_edge(edge_name, c))
    
    current_x, current_y = start_x, start_y
    
    for circle in affecting_circles:
        # Draw to the start of the circle's influence
        circle_start_x, circle_start_y = get_circle_influence_start(edge_name, circle, start_x, start_y, end_x, end_y)
        
        if distance(current_x, current_y, circle_start_x, circle_start_y) > 2:
            ctx.line_to(circle_start_x, circle_start_y)
        
        # Draw the circle's contour that extends beyond the square
        draw_circle_contour_extension(ctx, edge_name, circle)
        
        # Update current position
        current_x, current_y = get_circle_influence_end(edge_name, circle, start_x, start_y, end_x, end_y)
    
    # Draw the remaining straight line to the end
    if distance(current_x, current_y, end_x, end_y) > 2:
        ctx.line_to(end_x, end_y)

def edge_affects_circle(edge_name, start_x, start_y, end_x, end_y, circle):
    """Check if a circle extends beyond this edge of the square"""
    
    if edge_name == "top":
        return (circle['y'] - circle['ry'] < start_y and 
                circle['x'] - circle['rx'] < end_x and 
                circle['x'] + circle['rx'] > start_x)
    elif edge_name == "right":
        return (circle['x'] + circle['rx'] > start_x and 
                circle['y'] - circle['ry'] < end_y and 
                circle['y'] + circle['ry'] > start_y)
    elif edge_name == "bottom":
        return (circle['y'] + circle['ry'] > start_y and 
                circle['x'] - circle['rx'] < start_x and 
                circle['x'] + circle['rx'] > end_x)
    elif edge_name == "left":
        return (circle['x'] - circle['rx'] < start_x and 
                circle['y'] - circle['ry'] < start_y and 
                circle['y'] + circle['ry'] > end_y)
    return False

def get_circle_position_on_edge(edge_name, circle):
    """Get the position of a circle along an edge for sorting"""
    if edge_name in ["top", "bottom"]:
        return circle['x']
    else:  # left or right
        return circle['y']

def get_circle_influence_start(edge_name, circle, start_x, start_y, end_x, end_y):
    """Get where the circle's influence starts on an edge"""
    if edge_name == "top":
        return (max(start_x, circle['x'] - circle['rx']), start_y)
    elif edge_name == "right":
        return (start_x, max(start_y, circle['y'] - circle['ry']))
    elif edge_name == "bottom":
        return (min(start_x, circle['x'] + circle['rx']), start_y)
    elif edge_name == "left":
        return (start_x, min(start_y, circle['y'] + circle['ry']))

def get_circle_influence_end(edge_name, circle, start_x, start_y, end_x, end_y):
    """Get where the circle's influence ends on an edge"""
    if edge_name == "top":
        return (min(end_x, circle['x'] + circle['rx']), start_y)
    elif edge_name == "right":
        return (start_x, min(end_y, circle['y'] + circle['ry']))
    elif edge_name == "bottom":
        return (max(end_x, circle['x'] - circle['rx']), start_y)
    elif edge_name == "left":
        return (start_x, max(end_y, circle['y'] - circle['ry']))

def draw_circle_contour_extension(ctx, edge_name, circle):
    """Draw the part of the circle that extends beyond the square edge"""
    
    # Calculate the arc of the circle that extends beyond the square
    cx, cy = circle['x'], circle['y']
    rx, ry = circle['rx'], circle['ry']
    
    # Create several points along the circle's contour that extends beyond
    num_points = 10
    if edge_name == "top":
        # Arc from left intersection to right intersection, going above the square
        start_angle = math.pi * 0.75  # Upper left
        end_angle = math.pi * 0.25    # Upper right
    elif edge_name == "right":
        # Arc going to the right of the square
        start_angle = math.pi * 1.75  # Lower right
        end_angle = math.pi * 0.25    # Upper right
    elif edge_name == "bottom":
        # Arc going below the square
        start_angle = math.pi * 1.25  # Lower left
        end_angle = math.pi * 1.75    # Lower right
    elif edge_name == "left":
        # Arc going to the left of the square
        start_angle = math.pi * 0.75  # Upper left
        end_angle = math.pi * 1.25    # Lower left
    
    # Draw smooth arc
    for i in range(num_points + 1):
        t = i / num_points
        angle = start_angle + (end_angle - start_angle) * t
        
        # Calculate point on ellipse
        px = cx + rx * math.cos(angle)
        py = cy + ry * math.sin(angle)
        
        ctx.line_to(px, py)

def distance(x1, y1, x2, y2):
    """Calculate distance between two points"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def draw_contact_emphasis(ctx, all_circles, cx, cy, half_size):
    """Draw emphasis lines where circles make contact with square edges"""
    
    # Square boundaries
    square_left = cx - half_size
    square_right = cx + half_size
    square_top = cy - half_size
    square_bottom = cy + half_size
    
    for circle in all_circles:
        # Check if circle intersects with square edges
        circle_left = circle['x'] - circle['rx']
        circle_right = circle['x'] + circle['rx']
        circle_top = circle['y'] - circle['ry']
        circle_bottom = circle['y'] + circle['ry']
        
        # Draw contact emphasis for each edge that intersects
        ctx.set_source_rgba(0, 0, 0, 0.8)  # Dark emphasis line
        ctx.set_line_width(3.0)
        
        # Left edge contact
        if (circle_left <= square_left <= circle_right and 
            circle_top <= cy <= circle_bottom):
            contact_start_y = max(circle_top, square_top)
            contact_end_y = min(circle_bottom, square_bottom)
            if contact_end_y > contact_start_y:
                ctx.move_to(square_left, contact_start_y)
                ctx.line_to(square_left, contact_end_y)
                ctx.stroke()
        
        # Right edge contact
        if (circle_left <= square_right <= circle_right and 
            circle_top <= cy <= circle_bottom):
            contact_start_y = max(circle_top, square_top)
            contact_end_y = min(circle_bottom, square_bottom)
            if contact_end_y > contact_start_y:
                ctx.move_to(square_right, contact_start_y)
                ctx.line_to(square_right, contact_end_y)
                ctx.stroke()
        
        # Top edge contact
        if (circle_top <= square_top <= circle_bottom and 
            circle_left <= cx <= circle_right):
            contact_start_x = max(circle_left, square_left)
            contact_end_x = min(circle_right, square_right)
            if contact_end_x > contact_start_x:
                ctx.move_to(contact_start_x, square_top)
                ctx.line_to(contact_end_x, square_top)
                ctx.stroke()
        
        # Bottom edge contact
        if (circle_top <= square_bottom <= circle_bottom and 
            circle_left <= cx <= circle_right):
            contact_start_x = max(circle_left, square_left)
            contact_end_x = min(circle_right, square_right)
            if contact_end_x > contact_start_x:
                ctx.move_to(contact_start_x, square_bottom)
                ctx.line_to(contact_end_x, square_bottom)
                ctx.stroke()

def draw_uncrossed_square_border(ctx, all_circles, cx, cy, half_size):
    """Draw only the parts of square border that are NOT covered by any circles"""
    
    # Square boundaries
    square_left = cx - half_size
    square_right = cx + half_size
    square_top = cy - half_size
    square_bottom = cy + half_size
    
    # Set up border drawing properties
    ctx.set_source_rgba(0, 0, 0, 0.7)
    ctx.set_line_width(2.5)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    
    # For each edge of the square, find segments that are NOT covered by circles
    edges = [
        ("top", square_left, square_top, square_right, square_top),
        ("right", square_right, square_top, square_right, square_bottom),
        ("bottom", square_right, square_bottom, square_left, square_bottom),
        ("left", square_left, square_bottom, square_left, square_top)
    ]
    
    for edge_name, start_x, start_y, end_x, end_y in edges:
        uncovered_segments = find_uncrossed_edge_segments(
            edge_name, start_x, start_y, end_x, end_y, all_circles, half_size
        )
        
        # Draw each uncovered segment
        for segment_start, segment_end in uncovered_segments:
            ctx.move_to(segment_start[0], segment_start[1])
            ctx.line_to(segment_end[0], segment_end[1])
            ctx.stroke()

def find_uncrossed_edge_segments(edge_name, start_x, start_y, end_x, end_y, all_circles, half_size):
    """Find segments of square edge that are NOT covered by any circles"""
    
    # Sample points along the edge
    num_samples = 100
    edge_points = []
    
    for i in range(num_samples + 1):
        t = i / num_samples
        px = start_x + t * (end_x - start_x)
        py = start_y + t * (end_y - start_y)
        
        # Check if this point is covered (inside) any circle
        is_covered = False
        for circle in all_circles:
            if point_inside_circle(px, py, circle):
                is_covered = True
                break
        
        edge_points.append({
            'x': px,
            'y': py,
            'position': t,
            'is_covered': is_covered
        })
    
    # Find continuous segments that are NOT covered
    uncovered_segments = []
    current_segment_start = None
    
    for i, point in enumerate(edge_points):
        if not point['is_covered']:  # Point is NOT covered by any circle
            if current_segment_start is None:
                current_segment_start = point
        else:  # Point IS covered by a circle
            if current_segment_start is not None:
                # End the current uncovered segment
                prev_point = edge_points[i-1] if i > 0 else current_segment_start
                if current_segment_start != prev_point:
                    uncovered_segments.append([
                        (current_segment_start['x'], current_segment_start['y']),
                        (prev_point['x'], prev_point['y'])
                    ])
                current_segment_start = None
    
    # Handle final segment if it ends uncovered
    if current_segment_start is not None:
        final_point = edge_points[-1]
        if current_segment_start != final_point:
            uncovered_segments.append([
                (current_segment_start['x'], current_segment_start['y']),
                (final_point['x'], final_point['y'])
            ])
    
    return uncovered_segments

def point_inside_circle(px, py, circle):
    """Check if a point is inside a circle/ellipse"""
    
    cx, cy = circle['x'], circle['y']
    rx, ry = circle['rx'], circle['ry']
    
    # Calculate distance to circle center in ellipse coordinates
    dx = (px - cx) / rx
    dy = (py - cy) / ry
    distance_squared = dx*dx + dy*dy
    
    # Point is inside if distance <= 1 (for ellipse equation)
    return distance_squared <= 1.0

def create_cloud_overlap_square(ctx, cx, cy, size, text="CLOUD!", density="medium"):
    """Create square with cloud-like overlapping circles"""
    
    # Density settings
    densities = {
        "low": 3,
        "medium": 5,
        "high": 7,
        "very_high": 9
    }
    num_circles = densities.get(density, 5)
    
    # Generate cloud-like circles
    all_circles = []
    half_size = size / 2
    
    # Add circles around the perimeter
    for angle in range(0, 360, 30):  # Every 30 degrees
        rad = math.radians(angle)
        
        # Base position on square perimeter
        base_distance = half_size + random.uniform(5, 20)
        base_x = cx + base_distance * math.cos(rad)
        base_y = cy + base_distance * math.sin(rad)
        
        # Add some circles at this angle
        for i in range(random.randint(1, 3)):
            circle_x = base_x + random.uniform(-15, 15)
            circle_y = base_y + random.uniform(-15, 15)
            
            radius = random.uniform(12, 25)
            
            all_circles.append({
                'x': circle_x,
                'y': circle_y,
                'rx': radius * random.uniform(0.8, 1.2),
                'ry': radius * random.uniform(0.8, 1.2),
                'side': 'cloud'
            })
    
    # Draw cloud circles
    for circle in all_circles:
        draw_cloud_circle(ctx, circle)
    
    # Draw base square
    draw_base_square(ctx, cx, cy, size)
    
    # Add text
    draw_overlap_text(ctx, cx, cy, text)

def draw_cloud_circle(ctx, circle):
    """Draw a cloud-style circle"""
    
    ctx.save()
    ctx.translate(circle['x'], circle['y'])
    ctx.scale(circle['rx'], circle['ry'])
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()
    
    # Cloud-like gradient
    gradient = cairo.RadialGradient(
        circle['x'], circle['y'], 0,
        circle['x'], circle['y'], max(circle['rx'], circle['ry'])
    )
    gradient.add_color_stop_rgb(0, 1.0, 1.0, 1.0)       # Pure white
    gradient.add_color_stop_rgb(0.6, 0.98, 0.98, 1.0)   # Very light blue
    gradient.add_color_stop_rgb(1, 0.9, 0.9, 0.95)      # Light edge
    
    ctx.set_source(gradient)
    ctx.fill_preserve()
    
    # Soft outline
    ctx.set_source_rgba(0, 0, 0, 0.2)
    ctx.set_line_width(0.8)
    ctx.stroke()

def draw_overlap_text(ctx, cx, cy, text):
    """Draw text in the overlapping bubble"""
    
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(14)
    
    text_extents = ctx.text_extents(text)
    text_width = text_extents.width
    text_height = text_extents.height
    
    text_x = cx - text_width / 2
    text_y = cy + text_height / 2
    
    # Text shadow
    ctx.set_source_rgba(0, 0, 0, 0.3)
    ctx.move_to(text_x + 1, text_y + 1)
    ctx.show_text(text)
    
    # Main text
    ctx.set_source_rgb(0, 0, 0)
    ctx.move_to(text_x, text_y)
    ctx.show_text(text)

def create_overlapping_demo():
    """Create demo with various overlapping circle styles"""
    
    random.seed(777)
    
    WIDTH, HEIGHT = 1300, 1000
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    
    # Background
    ctx.set_source_rgb(0.97, 0.97, 0.99)
    ctx.paint()
    
    # Row 1: Different circle styles
    create_overlapping_circles_square(ctx, 150, 140, 100, "VARIED!", "varied", 4)
    create_overlapping_circles_square(ctx, 350, 140, 100, "UNIFORM!", "uniform", 5)
    create_overlapping_circles_square(ctx, 550, 140, 100, "OVALS!", "ovals", 4)
    create_overlapping_circles_square(ctx, 750, 140, 100, "BUBBLES!", "bubbles", 6)
    create_overlapping_circles_square(ctx, 950, 140, 100, "ORGANIC!", "organic", 5)
    
    # Row 2: Different circle counts
    create_overlapping_circles_square(ctx, 150, 320, 110, "FEW!", "varied", 3)
    create_overlapping_circles_square(ctx, 350, 320, 110, "SOME!", "bubbles", 5)
    create_overlapping_circles_square(ctx, 550, 320, 110, "MANY!", "organic", 7)
    create_overlapping_circles_square(ctx, 750, 320, 110, "LOTS!", "varied", 9)
    create_overlapping_circles_square(ctx, 950, 320, 110, "SMALL!", "small", 8)
    
    # Row 3: Cloud-like overlaps
    create_cloud_overlap_square(ctx, 200, 520, 120, "CLOUD LOW!", "low")
    create_cloud_overlap_square(ctx, 450, 520, 120, "CLOUD MED!", "medium")
    create_cloud_overlap_square(ctx, 700, 520, 120, "CLOUD HIGH!", "high")
    create_cloud_overlap_square(ctx, 950, 520, 120, "CLOUD MAX!", "very_high")
    
    # Row 4: Large examples
    create_overlapping_circles_square(ctx, 200, 720, 140, "BIG OVERLAP!", "bubbles", 8)
    create_cloud_overlap_square(ctx, 500, 720, 150, "BIG CLOUD!", "high")
    create_overlapping_circles_square(ctx, 800, 720, 135, "BIG ORGANIC!", "organic", 7)
    
    # Row 5: Extra variations
    create_overlapping_circles_square(ctx, 150, 880, 120, "MEGA!", "varied", 10)
    create_overlapping_circles_square(ctx, 400, 880, 115, "SUPER!", "ovals", 6)
    create_cloud_overlap_square(ctx, 650, 880, 125, "ULTRA!", "very_high")
    create_overlapping_circles_square(ctx, 900, 880, 110, "EXTREME!", "small", 12)
    
    # Title
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(32)
    ctx.set_source_rgb(0.2, 0.2, 0.4)
    ctx.move_to(350, 50)
    ctx.show_text("OVERLAPPING CIRCLES SQUARES")
    
    # Subtitle
    ctx.set_font_size(16)
    ctx.move_to(480, 80)
    ctx.show_text("Circles & Ovals on All Sides")
    
    surface.write_to_png("overlapping_circles_squares.png")
    print("✅ Overlapping circles squares saved as 'overlapping_circles_squares.png'")

if __name__ == "__main__":
    create_overlapping_demo()
    print("🔴 Created squares with overlapping circles! Organic bubble effects! ⭕✨")