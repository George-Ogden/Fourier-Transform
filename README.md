# Fourier Transform (Epicycles)
Transform an image (.svg) or a polygon into a series of rotating circles.  
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

## Installation
Requires `python >= 3.7`  
The rendering uses [Manim Community](https://github.com/manimCommunity/manim) (the community version of the software in the [3Blue1Brown videos](https://www.youtube.com/c/3blue1brown) but you **don't** need to install $\LaTeX$.

```
pip install -r requirements.txt
```

## Usage
Transform an image (.svg) or a polygon into a series of rotating circles

```
usage: main.py [-h] (-v VECTOR | -i IMAGE | -s SIDES) [-o OUTPUT] [-p] [-n NUMBER] [-r ROTATIONS]
               [-d DURATION] [-f FADE]

Transform an image (.svg) or a polygon into a series of rotating circles

options:
  -h, --help            show this help message and exit

Input Options:
  -v VECTOR, --vector VECTOR
                        transform an SVG file
  -i IMAGE, --image IMAGE
                        transform an image file
  -s SIDES, --sides SIDES
                        create a polygon with s sides

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
  -f FADE, --fade FADE  rate of exponential decay of path - higher means faster decay (default:       
                        0.005)
```
