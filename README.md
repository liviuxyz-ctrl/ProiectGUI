# Mandelbrot Set Viewer

This program is an interactive viewer for the Mandelbrot set, developed using Python, Pygame, and OpenGL. You can navigate the Mandelbrot set using mouse and keyboard controls.

# Examples 

![image](https://github.com/liviuxyz-ctrl/ProiectGUI/assets/70070368/d4d14d51-d324-4ee8-bba8-9aaf83ab7354)
![image](https://github.com/liviuxyz-ctrl/ProiectGUI/assets/70070368/79e875c8-79d2-44a1-8c83-6621fd5f9fd2)


## Features

- Real-time rendering of the Mandelbrot set.
- Smooth zooming and panning functionality.
- Support for both automatic and manual navigation.

## Controls

The viewer supports several keyboard and mouse controls:

- **Mouse Movement**: When mouse control mode is enabled (`m` key), the position of the set on the screen follows the mouse cursor.
- **Mouse Scroll**: Zoom in and out. Scroll up to zoom in, and scroll down to zoom out.
- **Arrow Keys**: Move the set on the screen. Use the up/down/left/right arrow keys to move the set in the corresponding direction.
- **`m` Key**: Toggle mouse control mode. When enabled, the set follows the mouse cursor.
- **`p` Key**: Toggle automatic path following. When enabled, the viewer automatically follows a pre-defined path.
- **`1` Key**: Increase the zoom speed modifier.
- **`2` Key**: Decrease the zoom speed modifier.
- **`r` Key**: Reset the viewer to its initial state.

## Requirements

- Python 3.7 or later.
- Pygame.
- PyOpenGL.

## Installation

Clone the repository:

git clone https://github.com/liviuxyz-ctrl/ProiectGUI

Enter the project directory:

cd mandelbrot_viewer

Install the required packages:

pip install -r requirements.txt

## Usage

Run the viewer:

python mandelbrot_viewer.py

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

