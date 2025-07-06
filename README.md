# Pidog Autonomous Patrol with Obstacle Avoidance

This project enables a Pidog robot to autonomously patrol an area, intelligently detecting and avoiding obstacles using its ultrasonic sensor. The Pidog will scan its environment only when an obstacle is detected, choose the safest escape route, and then reorient itself to continue patrolling.

## Features

* **Intelligent Obstacle Detection:** Uses the Pidog's built-in ultrasonic sensor to detect objects.
* **Dynamic Environment Scanning:** Scans multiple directions only when an obstacle is too close, optimizing movement.
* **Smart Escape Routing:** Calculates the best and safest direction to move in when blocked, prioritizing clear paths.
* **Autonomous Movement:** Continues patrolling forward when clear, reacting only when necessary.
* **Visual & Auditory Feedback:** Uses RGB LED strip and barking sounds to indicate danger.
* **Playful Interactions:** Incorporates head shakes and tail wags during clear forward movement.

## Requirements

### Hardware

* **Pidog Robot:** This code is specifically designed for the Pidog robot.
* **Raspberry Pi:** The Pidog robot is controlled by a Raspberry Pi.

### Software

* **Python 3**
* **Pidog Library:** The core library for controlling the Pidog robot.
* **`preset_actions`:** This module is assumed to be part of the Pidog environment or available locally for actions like `bark`.

## Installation

1.  **Ensure your Pidog is assembled and connected** according to its official documentation.
2.  **Install the Pidog library:**
    If you haven't already, install the `pidog` library. You might need to follow the official Pidog setup guide for this, which usually involves:
    ```bash
    pip3 install pidog
    ```
    Or, if you prefer to use the provided `requirements.txt`:
    ```bash
    pip3 install -r requirements.txt
    ```
3.  **Place the code:** Save the provided Python code as `main.py` (or any other `.py` file) in a suitable directory on your Raspberry Pi. Ensure the `preset_actions.py` module is accessible in the same directory or within your Python path if it's a separate file.

## Usage

1.  **Run the script:**
    Navigate to the directory where you saved the `main.py` file using your terminal on the Raspberry Pi.
    ```bash
    cd /path/to/your/project
    python3 main.py
    ```
2.  **Observe the Pidog:**
    The Pidog will start in a standing position. It will then begin patrolling forward. When it detects an obstacle within `DANGER_DISTANCE` (15 cm), it will stop, bark, move backward, scan its surroundings, turn towards the safest direction, and then resume its forward patrol.
3.  **Stop the program:**
    You can stop the program at any time by pressing `Ctrl+C` in the terminal. The Pidog will gracefully shut down its motors.

## Configuration

* **`DANGER_DISTANCE`**: Adjust this constant in `main.py` (default: 15 cm) to change how close the Pidog gets to an obstacle before reacting.
* **`SCAN_ANGLES`**: Modify this list to change the angles (in degrees relative to the Pidog's forward direction) at which the Pidog scans for obstacles.

## Troubleshooting

* If the Pidog doesn't move or respond, ensure all power connections are secure and the `pidog` library is correctly installed.
* Check the terminal output for any error messages.
* Ensure the ultrasonic sensor is clean and unobstructed.

## Contribution

Feel free to fork this repository and improve upon the navigation logic or add new behaviors!
