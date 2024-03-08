import requests
from vision import compute

# URL of the ESP32 serving the images
ESP32_URL = "http://esp32_ip_address/capture"


# Function to process the image and determine motor directions
def process_image(image):
    # Your image processing logic here
    # This is just a placeholder
    # Example: detecting lines\
    result = compute(image)
    if result[0] == 0:
        if result[1] == 0:
            return 1, 1
        else:
            return 1, -1
    elif result[1] == 1:
        if result[0] == 0:
            return -1, 1
        else:
            return -1, -1
    else:
        return 0, 0


# this gets output from vision.compute for directions


# Function to send motor directions to ESP32
def send_motor_directions(direction1, direction2):
    # URL of the ESP32 to control motors
    control_url = "http://esp32_ip_address/control"
    # Send POST request with motor directions
    data = {"motor1_speed": direction1, "motor2_speed": direction2}
    response = requests.post(control_url, data=data)
    if response.status_code == 200:
        print("Motor directions sent successfully")
    else:
        print("Failed to send motor directions")


# Main loop
while True:
    try:
        # Request image from ESP32
        response = requests.get(ESP32_URL)
        if response.status_code == 200:
            image = response.content
            # Process image
            direction1, direction2 = process_image(image)
            # Send motor directions to ESP32
            send_motor_directions(direction1, direction2)
        else:
            print("Failed to receive image from ESP32")
    except Exception as e:
        print("Error:", e)
