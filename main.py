import os
import platformbed
from solid import cube, difference, mirror, rotate, scad_render, translate, union


if __name__ == "__main__":
    width = 60
    length = 79.5
    with open(f"slat.scad", "w") as scadfile:
        scadfile.write(scad_render(platformbed.slat(width, 2)))
    with open(f"side.scad", "w") as scadfile:
        scadfile.write(scad_render(platformbed.side(width)))
