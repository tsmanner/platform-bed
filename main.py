import os
import platformbed
from solid import cube, difference, mirror, rotate, scad_render_to_file, translate, union


if __name__ == "__main__":
    width = 60
    length = 79.5
    overhang = 2

    scad_render_to_file(platformbed.middle_slat(width, overhang), filepath="middle_slat.scad")
    scad_render_to_file(platformbed.end_slat(width, overhang), filepath="end_slat.scad")
    scad_render_to_file(platformbed.base_side(length), filepath="base_side.scad")
    scad_render_to_file(platformbed.base_support(length, overhang), filepath="base_support.scad")
    scad_render_to_file(platformbed.base_end(width), filepath="base_end.scad")
    scad_render_to_file(platformbed.base(width, length, overhang), filepath="base.scad")
    scad_render_to_file(platformbed.slats(width, length, overhang), filepath="slats.scad")
    scad_render_to_file(platformbed.bed(width, length, overhang), filepath="bed.scad")
