import time, _thread, socket
import network
from machine import Pin, I2C
from sen5x.sen5x import SEN5x

# Just a comment

# ---------- Global Variables ----------
sensor_data = {
    'ppm1_0': 0,
    'ppm2_5': 0,
    'ppm4_0': 0,
    'ppm10_0': 0,
    'humidity': 0,
    'temperature': 0,
    'voc': 0,
    'nox': 0,
}
ip = None  # Will be set after connecting to WiFi

# ---------- WiFi Connection ----------
SSID = 'XXX'
PASSWORD = 'XXX'

def wifi_connect():
    global ip
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to WiFi...")
    while not wlan.isconnected():
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print("Connected, IP address:", ip)
    return ip

# ---------- Sensor Loop ----------
def sensor_loop():
    global sensor_data
    # I2C settings for your sensor
    i2c = I2C(0, scl=Pin(6, pull=Pin.PULL_UP), sda=Pin(5, pull=Pin.PULL_UP), freq=50000)
    with SEN5x(i2c) as sen:
        while True:
            ppm1_0, ppm2_5, ppm4_0, ppm10_0, rh, t, voc, nox = sen.measured_values
            sensor_data = {
                'ppm1_0': ppm1_0,
                'ppm2_5': ppm2_5,
                'ppm4_0': ppm4_0,
                'ppm10_0': ppm10_0,
                'humidity': rh,
                'temperature': t,
                'voc': voc,
                'nox': nox,
            }
            print("Sensor data updated:", sensor_data)
            time.sleep(5)

# ---------- HTTP Server (for Prometheus scraping) ----------
def http_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("HTTP server listening on", addr)
    while True:
        cl, addr = s.accept()
        print("Client connected from", addr)
        cl_file = cl.makefile('rwb', 0)
        # Read and ignore the HTTP request headers
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break

        # Format sensor data in Prometheus text format:
        response = ""
        response += "# HELP sen5x_ppm1_0 Particulate Matter 1.0 measurement\n"
        response += "# TYPE sen5x_ppm1_0 gauge\n"
        response += "sen5x_ppm1_0 {}\n".format(sensor_data['ppm1_0'])
        response += "# HELP sen5x_ppm2_5 Particulate Matter 2.5 measurement\n"
        response += "# TYPE sen5x_ppm2_5 gauge\n"
        response += "sen5x_ppm2_5 {}\n".format(sensor_data['ppm2_5'])
        response += "# HELP sen5x_ppm4_0 Particulate Matter 4.0 measurement\n"
        response += "# TYPE sen5x_ppm4_0 gauge\n"
        response += "sen5x_ppm4_0 {}\n".format(sensor_data['ppm4_0'])
        response += "# HELP sen5x_ppm10_0 Particulate Matter 10.0 measurement\n"
        response += "# TYPE sen5x_ppm10_0 gauge\n"
        response += "sen5x_ppm10_0 {}\n".format(sensor_data['ppm10_0'])
        response += "# HELP sen5x_humidity Humidity measurement\n"
        response += "# TYPE sen5x_humidity gauge\n"
        response += "sen5x_humidity {}\n".format(sensor_data['humidity'])
        response += "# HELP sen5x_temperature Temperature measurement\n"
        response += "# TYPE sen5x_temperature gauge\n"
        response += "sen5x_temperature {}\n".format(sensor_data['temperature'])
        response += "# HELP sen5x_voc VOC measurement\n"
        response += "# TYPE sen5x_voc gauge\n"
        response += "sen5x_voc {}\n".format(sensor_data['voc'])
        response += "# HELP sen5x_nox NOx measurement\n"
        response += "# TYPE sen5x_nox gauge\n"
        response += "sen5x_nox {}\n".format(sensor_data['nox'])

        http_response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\n" + response
        cl.send(http_response)
        cl.close()

# Then in your main() function, start your sensor loop & HTTP server


# ---------- Main Function ----------
def main():
    # Connect to WiFi (this sets the global ip variable)
    wifi_connect()
    # Start sensor loop in a background thread
    _thread.start_new_thread(sensor_loop, ())
    # Start HTTP server in a background thread
    _thread.start_new_thread(http_server, ())

if __name__ == '__main__':
    main()
