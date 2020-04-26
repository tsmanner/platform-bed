import os
import platformbed
from solid import cube, difference, mirror, rotate, scad_render, translate, union


if __name__ == "__main__":
    width = 60
    length = 79.5
    overhang = 2
    with open(f"middle_slat.scad", "w") as scadfile:
        scadfile.write(scad_render(platformbed.middle_slat(width, overhang)))
    with open(f"end_slat.scad", "w") as scadfile:
        scadfile.write(scad_render(platformbed.end_slat(width, overhang)))
    with open(f"side.scad", "w") as scadfile:
        scadfile.write(scad_render(platformbed.base_side(length)))
    with open(f"support.scad", "w") as scadfile:
        scadfile.write(scad_render(platformbed.base_support(length, overhang)))
    with open(f"end.scad", "w") as scadfile:
        scadfile.write(scad_render(platformbed.base_end(width)))
