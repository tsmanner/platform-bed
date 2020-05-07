import os
import platformbed
from solid import cube, difference, mirror, rotate, scad_render_to_file, translate, union


if __name__ == "__main__":
    width = 60
    length = 79.5
    overhang = 2
    rise = 12

    if not os.path.isdir("scadfiles"):
        if os.path.isfile("scadfiles"):
            os.remove("scadfiles")
        os.mkdir("scadfiles")

    scad_render_to_file(platformbed.slat_middle(width, overhang), filepath="scadfiles/slat_middle.scad")
    scad_render_to_file(platformbed.slat_end(width, overhang), filepath="scadfiles/slat_end.scad")
    scad_render_to_file(platformbed.base_side(length, overhang), filepath="scadfiles/base_side.scad")
    scad_render_to_file(platformbed.base_support(length, overhang), filepath="scadfiles/base_support.scad")
    scad_render_to_file(platformbed.base_end(width, overhang), filepath="scadfiles/base_end.scad")
    scad_render_to_file(platformbed.base(width, length, overhang), filepath="scadfiles/base.scad")
    scad_render_to_file(platformbed.slats(width, length, overhang), filepath="scadfiles/slats.scad")
    scad_render_to_file(platformbed.bed(width, length, overhang, 8.5), filepath="scadfiles/bed.scad")

    scad_render_to_file(platformbed.foot(rise), filepath="scadfiles/foot_end.scad")
