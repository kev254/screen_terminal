# Terminal Renderer

This Python program renders a text-based screen using the `curses` library. It interprets binary commands passed interactively, allowing users to control screen setup, draw characters, and clear the screen.

## Features
- **Screen Setup**: Define the screen width, height, and color mode.
- **Draw Character**: Place characters at specific coordinates on the screen.
- **Clear Screen**: Clear the entire screen.
- **End of File (EOF)**: Terminate input with the EOF command (`0xFF`).
- **Interactive Command Input**: Enter each command one at a time through the terminal.
- **Screenshot Option**: Take a screenshot of the rendered screen.

## Requirements
- Python 3.x
- `curses` library (usually pre-installed with Python)

## Installation
1. Clone or download the repository.
2. Make sure you have Python 3.x installed on your system.
3. Install the required libraries (if necessary):
   ```bash
   pip install curses
