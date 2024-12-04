import curses

class RenderTerminal:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.color_mode = 0
        self.initialized = False
        self.buffer = []

    def setup_screen(self, width, height, color_mode):
        self.width = width
        self.height = height
        self.color_mode = color_mode
        self.initialized = True
        self.buffer = [[" "] * width for _ in range(height)]

    def draw_character(self, x, y, color, char):
        if self.initialized and 0 <= x < self.width and 0 <= y < self.height:
            self.buffer[y][x] = char

    def clear_screen(self):
        if self.initialized:
            self.buffer = [[" "] * self.width for _ in range(self.height)]

    def render(self, stdscr):
        if not self.initialized:
            return
        stdscr.clear()
        for y, row in enumerate(self.buffer):
            for x, char in enumerate(row):
                stdscr.addch(y, x, char)
        stdscr.refresh()

def parse_command(command, data, renderer):
    if command == 0x1:  # Screen setup
        if len(data) == 3:
            width, height, color_mode = data
            renderer.setup_screen(width, height, color_mode)
        else:
            print("Error: Invalid data length for Screen Setup.")
    elif command == 0x2:  # Draw character
        if len(data) == 4:
            x, y, color, char = data
            renderer.draw_character(x, y, color, chr(char))
        else:
            print("Error: Invalid data length for Draw Character.")
    elif command == 0x7:  # Clear screen
        if len(data) == 0:
            renderer.clear_screen()
        else:
            print("Error: Clear Screen should have no additional data.")
    elif command == 0xFF:  # End of file
        if len(data) == 0:
            return True  # Indicates end of input
        else:
            print("Error: End of File should have no additional data.")
    else:
        print(f"Warning: Unknown command 0x{command:02X}.")
    
    return False

def main(stdscr):
    curses.curs_set(0)
    renderer = RenderTerminal()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Enter command and data (e.g., 0x1 0x03 40 20 0x01) or 'q' to quit:")
        stdscr.refresh()

        # Get user input
        command_line = stdscr.getstr(1, 0, 80).decode("utf-8").strip()

        if command_line.lower() == 'q':
            break  # Quit the program

        try:
            # Convert the command input into a list of integers (hex values)
            command_parts = command_line.split()
            command = int(command_parts[0], 16)  # First part is the command byte
            data = [int(byte, 16) for byte in command_parts[1:]]  # Rest are the data bytes

            # Parse and execute the command
            if parse_command(command, data, renderer):
                break  # If command is 0xFF (end), break the loop
            
        except ValueError:
            stdscr.addstr(2, 0, "Invalid input. Please enter valid hex values.")
            stdscr.refresh()
            stdscr.getch()  # Wait for user to acknowledge the error

        renderer.render(stdscr)
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
