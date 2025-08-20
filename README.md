# Micro Python esp32-c3 Environment Sensor

## Using icon library
Example usage:
```
# Example usage: Draw each icon at different positions
# Temperature icon in red
icons.draw_temp_icon(display, 10, 10, 40, icons.color565_BGR(255, 0, 0))
# Particles icon in green
icons.draw_particles_icon(display, 70, 10, 40, icons.color565_BGR(255, 255, 255))
# VOCs icon in blue
icons.draw_vocs_icon(display, 130, 10, 40, icons.color565_BGR(0, 255, 0))
# Humidity icon in blue
icons.draw_humidity_icon(display, 190, 10, 40, icons.color565_BGR(0, 0, 255))
# NOx icon in magenta
icons.draw_nox_icon(display, 250, 10, 40, icons.color565_BGR(255, 0, 255))
```