# Fourier Transform (Epicycles)
Transform an image or a polygon into a series of rotating circles.  
This project is written from scratch and it looks like a spin off from the videos because that was the aim, not because the code was copied (trust me if I could have, it would have saved me a ton of effort).  
Inspired by [this video](https://www.youtube.com/watch?v=-qgreAUpPwM) and a challenge from a friend.
## Maths
See details of the maths explained in [this video](https://www.youtube.com/watch?v=r6sGWTCMz2k&t=853s).

## Examples
### Images
#### Handshake
![Handshake](examples/output/handshake.gif "Handshake")
#### Skyline
![Skyline](examples/output/skyline.gif "Skyline")
#### Runner
![Runner](examples/output/runner.gif "Runner")
#### Bird
![Bird](examples/output/bird.gif "Bird")
### SVG Files
#### Pi Creature
![Pi Creature](examples/output/pi.gif "Pi Creature")
#### GitHub Logo
![GitHub Logo](examples/output/github.gif "GitHub Logo")
#### Heart
![Heart](examples/output/heart.gif "Heart")
#### Star
![Pi Creature](examples/output/star.gif "Star")
### Polygons
#### Traingle
![Triangle](examples/output/triangle.gif "Triangle")
#### Hexagon
![Hexagon](examples/output/hexagon.gif "Hexagon")
### Text
#### Letter G
![Letter G](examples/output/G.gif "Letter G")
### Points
#### Treble Clef
![Treble Clef](examples/output/treble-clef.gif "Treble Clef")

## Installation
Requires `python >= 3.10`  
The rendering uses [Manim Community](https://github.com/manimCommunity/manim) (the community version of the software in the [3Blue1Brown videos](https://www.youtube.com/c/3blue1brown) but you **don't** need to install $\LaTeX$.

```
pip install -r requirements.txt
```

## Usage
Transform an image (.svg) or a polygon into a series of rotating circles

```
usage: main.py [-h] [-o OUTPUT] [-p] [-n NUMBER] [-r ROTATIONS] [-d DURATION] [-f FADE] {vector,image,polygon} ...

Transform an image or a polygon into a series of rotating circles

options:
  -h, --help            show this help message and exit

Input Options:
  Select different input formats

  {vector,image,polygon}
    vector              transform an SVG file
    image               transform an image file
    polygon             transform a polygon
    text                transform text
    array               transform a numpy array of points (1D array of complex numbers x + iy)

Output Options:
  -o OUTPUT, --output OUTPUT, --output_file OUTPUT
                        output file (default: output.mp4)
  -p, --preview         preview when complete

Animation Options:
  -n NUMBER, --number NUMBER
                        number of circles (default: 50)
  -r ROTATIONS, --rotations ROTATIONS
                        number of complete rotations (default: 3)
  -d DURATION, --duration DURATION
                        number of seconds for each rotation (default: 10)
  -f FADE, --fade FADE  rate of exponential decay of path - higher means faster decay (default: 0.005)
```
### Images
```
usage: main.py image [-h] IMAGE

image

positional arguments:
  IMAGE       image file

options:
  -h, --help  show this help message and exit
```
### Vector Graphics
```
usage: main.py vector [-h] VECTOR

vector

positional arguments:
  VECTOR      SVG file

options:
  -h, --help  show this help message and exit
```
### Polygon
```
usage: main.py polygon [-h] SIDES

polygon

positional arguments:
  SIDES       number of sides

options:
  -h, --help  show this help message and exit
```

### Text
```
usage: main.py text [-h] [--font FONT] TEXT

text

positional arguments:
  TEXT         text

options:
  -h, --help   show this help message and exit
  --font FONT  specify text font (default: examples/fonts/georgia.ttf)
```
### Array
```
usage: main.py array [-h] ARRAY

array

positional arguments:
  ARRAY       NPY file

options:
  -h, --help  show this help message and exit
```