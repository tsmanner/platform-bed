import collections
import os
import platformbed
from solid import cube, difference, mirror, rotate, scad_render_to_file, translate, union, OpenSCADObject


SCADFILE_DIR = "/mnt/c/Users/zephr/Documents/platformbed/"


def iter_children(scad_object: OpenSCADObject):
    yield scad_object
    for child in scad_object.children:
        for child_child in iter_children(child):
            yield child_child


if __name__ == "__main__":
    width = 60
    length = 79.5
    overhang = 2
    rise = 12

    if not os.path.isdir(SCADFILE_DIR):
        if os.path.isfile(SCADFILE_DIR):
            os.remove(SCADFILE_DIR)
        os.mkdir(SCADFILE_DIR)

    scad_render_to_file(platformbed.slat_middle(width, overhang), filepath=f"{SCADFILE_DIR}/slat_middle.scad")
    scad_render_to_file(platformbed.slat_end(width, overhang), filepath=f"{SCADFILE_DIR}/slat_end.scad")
    scad_render_to_file(platformbed.base_side(length, overhang), filepath=f"{SCADFILE_DIR}/base_side.scad")
    scad_render_to_file(platformbed.base_support(length, overhang), filepath=f"{SCADFILE_DIR}/base_support.scad")
    scad_render_to_file(platformbed.base_end(width, overhang), filepath=f"{SCADFILE_DIR}/base_end.scad")
    scad_render_to_file(platformbed.base(width, length, overhang), filepath=f"{SCADFILE_DIR}/base.scad")
    scad_render_to_file(platformbed.slats(width, length, overhang), filepath=f"{SCADFILE_DIR}/slats.scad")
    scad_render_to_file(platformbed.bed(width, length, overhang), filepath=f"{SCADFILE_DIR}/bed.scad")
    scad_render_to_file(platformbed.bed(width, length, overhang, 8.5), filepath=f"{SCADFILE_DIR}/bed_with_feet.scad")

    scad_render_to_file(platformbed.foot(rise), filepath=f"{SCADFILE_DIR}/foot_end.scad")

    scad_render_to_file(platformbed.TwoByFour(72), filepath=f"{SCADFILE_DIR}/TwoByFour.scad")

    boards_by_type = collections.defaultdict(lambda: collections.defaultdict(list))
    for element in iter_children(platformbed.bed(width, length, overhang, 8.5)):
        if isinstance(element, platformbed.Board):
            boards_by_type[type(element)][element.length].append(element)

    row = "| {count:>5} | {board}"
    print(row.format(count="Count", board="Board"))
    for boards_by_length in boards_by_type.values():
        for length, boards in boards_by_length.items():
            print(row.format(count=len(boards), board=boards[0]))
