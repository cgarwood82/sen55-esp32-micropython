# icons.py
import math

def color565_BGR(r, g, b):
    # Convert full 8-bit values to BGR565 instead of RGB565.
    # That means: blue in bits 15-11, green in bits 10-5, red in bits 4-0.
    return ((b & 0xF8) << 8) | ((g & 0xFC) << 3) | (r >> 3)

# --------------------------
# Helper drawing functions
# --------------------------

def draw_steam_line(display, start_x, start_y, length, amplitude, frequency, color):
    """
    Draws a single wavy steam line.

    - display: your display object
    - start_x, start_y: starting coordinates of the line
    - length: how many pixels upward the line will go
    - amplitude: maximum horizontal offset from start_x
    - frequency: controls the wavelength of the sine wave
    - color: 16-bit color for the line
    """
    prev_x = start_x
    prev_y = start_y
    # Step by 2 pixels for efficiency and smoothness.
    for t in range(1, length + 1, 2):
        offset = int(amplitude * math.sin(frequency * t))
        cur_x = start_x + offset
        cur_y = start_y - t  # moving upward (y decreases)
        draw_line(display, prev_x, prev_y, cur_x, cur_y, color)
        prev_x = cur_x
        prev_y = cur_y

def draw_line(display, x0, y0, x1, y1, color):
    """Bresenham's line algorithm."""
    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        display.draw_pixel(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy

def draw_circle(display, cx, cy, radius, color):
    """Midpoint circle algorithm (outline)."""
    x = radius
    y = 0
    err = 0
    while x >= y:
        display.draw_pixel(cx + x, cy + y, color)
        display.draw_pixel(cx + y, cy + x, color)
        display.draw_pixel(cx - y, cy + x, color)
        display.draw_pixel(cx - x, cy + y, color)
        display.draw_pixel(cx - x, cy - y, color)
        display.draw_pixel(cx - y, cy - x, color)
        display.draw_pixel(cx + y, cy - x, color)
        display.draw_pixel(cx + x, cy - y, color)
        y += 1
        if err <= 0:
            err += 2 * y + 1
        if err > 0:
            x -= 1
            err -= 2 * x + 1

def draw_arc(display, cx, cy, radius, start_angle, end_angle, color):
    """
    Draw an arc (outline only) of a circle with center (cx, cy) and given radius.
    Angles are in degrees.
    """
    for angle in range(start_angle, end_angle + 1):
        rad = math.radians(angle)
        x = int(cx + radius * math.cos(rad))
        y = int(cy + radius * math.sin(rad))
        display.draw_pixel(x, y, color)


# --------------------------
# Icon drawing functions
# --------------------------

def draw_temp_icon(display, x, y, size, color):
    """
    Draw a thermometer icon.
      - A vertical line (the thermometer tube)
      - A circle at the bottom (the bulb)
    """
    # Determine dimensions based on size
    tube_width = max(2, size // 4)
    circle_d = max(2, size // 2)
    # x_center = x + tube_width // 2
    x_center = max(2, size // 2)
    # Draw the tube as a vertical line
    for yy in range(y, y + size - circle_d):
        display.draw_pixel(x_center, yy, color)
    # Draw the bulb as a circle at the bottom
    cx = x_center
    cy = y + size - circle_d // 2
    radius = circle_d // 2
    draw_circle(display, cx, cy, radius, color)

def draw_particles_icon(display, x, y, size, color):
    """
    Draw a particles icon as three circles arranged in a triangle,
    with each circle having a slightly different size.

    Parameters:
      display: The display object with a draw_circle() function.
      x, y: The top-left coordinate of the icon area.
      size: The square area (in pixels) allotted for this icon.
      color: 16-bit color for the circles.
    """
    # Define radii for each circle (varying sizes)
    top_radius = max(1, size // 5)  # Slightly larger for the top circle
    left_radius = max(1, size // 9)  # Smaller for the bottom left
    right_radius = max(1, size // 7)  # Intermediate size for the bottom right

    # Calculate center positions for each circle
    # Top circle: centered horizontally at the top, offset by its radius
    cx_top = x + size // 2
    cy_top = y + top_radius

    # Bottom left: roughly in the left quarter, at the bottom of the icon area
    cx_bl = x + size // 4
    cy_bl = y + size - left_radius - 1  # subtract 1 to ensure full display

    # Bottom right: roughly in the right quarter, at the bottom of the icon area
    cx_br = x + (3 * size) // 4
    cy_br = y + size - right_radius - 1  # subtract 1 to ensure full display

    # Draw the circles (assuming draw_circle() is defined in your icons library)
    draw_circle(display, cx_top, cy_top, top_radius, color)
    draw_circle(display, cx_bl, cy_bl, left_radius, color)
    draw_circle(display, cx_br, cy_br, right_radius, color)


def draw_vocs_icon(display, x, y, size, color):
    """
    Draws a VOCs icon that represents fumes/steam rising.

    Parameters:
      display: The display object.
      x, y: The top-left coordinate of the icon area.
      size: The square area (in pixels) allotted for this icon.
      color: 16-bit color for the steam lines.
    """
    # Define parameters for the steam lines.
    # We'll have the steam originate near the bottom of the icon area.
    line_length = int(0.8 * size)  # steam goes upward for about 80% of the icon's height.
    amplitude = max(1, size // 10)  # amplitude of the sine wave
    frequency = 0.2  # frequency of the sine wave (tweak as needed)

    # Starting y: near the bottom of the icon area.
    start_y = y + int(0.8 * size)

    # Define three starting x positions spaced evenly across the icon.
    start_x1 = x + size // 4
    start_x2 = x + size // 2
    start_x3 = x + (3 * size) // 4

    # Draw three steam lines.
    draw_steam_line(display, start_x1, start_y, line_length, amplitude, frequency, color)
    draw_steam_line(display, start_x2, start_y, line_length, amplitude, frequency, color)
    draw_steam_line(display, start_x3, start_y, line_length, amplitude, frequency, color)


def draw_humidity_icon(display, x, y, size, color):
    """
    Draws an outlined teardrop-shaped humidity icon.

    The icon consists of:
      - A pointed top: two lines forming the sides from the tip to a flat base.
      - A rounded bottom: an arc drawn as the bottom half of a circle.

    Parameters:
      display: The display object with a draw_pixel(x, y, color) method.
      x, y: Top-left coordinates of the bounding box for the icon.
      size: Overall height of the icon.
      color: 16-bit color used for the outline.
    """
    # Define the half circle's radius.
    r = size // 3
    # The triangle (pointed top) occupies the top part: height = size - r.
    triangle_height = size - r
    # For simplicity, we'll assume the icon's overall width is 2*r.
    # center_x = x + r  # Horizontal center of the icon.
    center_x = int(size // 2)

    # The tip of the teardrop is at (center_x, y).
    tip_x, tip_y = center_x, y
    # The flat base of the triangle (which will be the top of the arc) is at y + triangle_height.
    left_base = (center_x - r, y + triangle_height)
    right_base = (center_x + r, y + triangle_height)

    # Draw the two sides of the teardrop (the triangle outline).
    draw_line(display, tip_x, tip_y, left_base[0], left_base[1], color)
    draw_line(display, tip_x, tip_y, right_base[0], right_base[1], color)

    # Draw the arc for the rounded bottom.
    # This arc has its endpoints at left_base and right_base.
    # Using our coordinate system (with y increasing downward), drawing an arc
    # from 0° to 180° with center at (center_x, y + triangle_height) yields the bottom curve.
    draw_arc(display, center_x, y + triangle_height, r, 0, 180, color)


def draw_nox_icon(display, x, y, size, color):
    """
    Draw a NOx icon as a circle with a small cross inside.
    """
    radius = int(max(1, size // 2 - (size * 0.05)))
    cx = x + size // 2
    cy = y + size // 2
    draw_circle(display, cx, cy, radius, color)
    # Draw a horizontal line for the cross
    for i in range(cx - radius // 2, cx + radius // 2 + 1):
        display.draw_pixel(i, cy, color)
    # Draw a vertical line for the cross
    for j in range(cy - radius // 2, cy + radius // 2 + 1):
        display.draw_pixel(cx, j, color)
