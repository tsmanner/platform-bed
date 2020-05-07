from itertools import repeat
from solid import color, cube, hole, mirror, part, rotate, translate, union, OpenSCADObject
from .joints import dovetail

X = 0
Y = 1
Z = 2


def board(length, width, thickness, axis):
    return cube(tuple(s[0] for s in sorted(
        zip(
            (length, width, thickness),
            axis,
        ),
        key=lambda z: z[1]
    )))()


def one_by_four(length, axis=(X, Y, Z)):
    return board(length, 3.5, 0.75, axis)


def one_by_six(length, axis=(X, Y, Z)):
    return board(length, 5.5, 0.75, axis)


def two_by_four(length, axis=(X, Y, Z)):
    return board(length, 3.5, 3/2, axis)


def four_by_four(length, axis=(X, Y, Z)):
    return board(length, 7/2, 7/2, axis)


class Board:
    def __init__(self, length, width, thickness, axis=(X, Y, Z)):
        super().__init__("Board", {})
        self.length = length
        self.width = width
        self.thickness = thickness
        self.axis = axis

    def scad(self):
        return board(self.length, self.width, self.thickness, self.axis)


class TwoByFour(Board):
    WIDTH = 3.5
    THICKNESS = 1.5
    def __init__(self, length, axis=(X, Y, Z)):
        super().__init__(length, axis)


def slat_displacements(matress_length):
    step = 7
    offset = 7/4 + ((matress_length - 7) % step) / 2
    displacement = 3.5
    while displacement < (matress_length - step):
        yield offset + displacement
        displacement += step


def slat_middle(matress_width, overhang):
    length = matress_width + overhang * 2
    half_cross = hole()(cube((3/2, 7/2, 1/4)))
    return part()(
        one_by_four(length)
      - translate((length - 3/2 - overhang, 0, 0))(half_cross)
      - translate((overhang, 0, 0))(half_cross)
    )


def slat_end(matress_width, overhang):
    length = matress_width + overhang * 2
    half_cross = hole()(cube((3/2, 11/2, 1/4)) + translate((0, 2, 0))(cube((3/2, 3/2, 3/4))))
    return part()(
        one_by_six(length)
      - translate((length - 3/2 - overhang, 0, 0))(half_cross)
      - translate((overhang, 0, 0))(half_cross)
    )


def base_side(matress_length, overhang):
    end_slat_half_cross = hole()(cube((3/2, 2, 1/2)) + translate((0, 7/2, 0))(cube((3/2, 2, 1/2))))
    slat_half_cross = hole()(cube((3/2, 7/2, 1/2)))
    base_half_cross = hole()(cube((3/2, 3/2, 11/8)))
    return color("tan")(part()(
        two_by_four(matress_length + 2 * overhang, (Y, Z, X))
      + translate((0, overhang, 0))(base_half_cross)
      + translate((0, overhang + matress_length - 3/2, 0))(base_half_cross)
      + translate((0, 0, 3))(end_slat_half_cross)
      + translate((0, 2 * overhang + matress_length - 11/2, 3))(end_slat_half_cross)
      - union()(*[translate((0, overhang + y, 3))(slat_half_cross) for y in slat_displacements(matress_length)])
    ))


def base_longitudinal_displacements(matress_width):
    segments = 3
    dx = (matress_width - 1.5) / segments
    x = 0
    while x <= matress_width:
        yield x
        x += dx


def base_lateral_displacements(matress_length):
    segments = 2
    dy = (matress_length - 1.5) / segments
    y = 0
    while y <= matress_length:
        yield y
        y += dy


def base_support(matress_length, overhang):
    half_cross = hole()(cube((3/2, 3/2, 11/8)))
    return color("tan")(part()(
        board(matress_length + overhang * 2, 11/4, 3/2, (Y, Z, X))
      - translate((0, overhang, 0))(half_cross)
      - translate((0, overhang + matress_length - 3/2, 0))(half_cross)
    ))


def base_end(matress_width, overhang):
    half_cross = hole()(cube((3/2, 3/2, 11/8)))
    return color("saddlebrown")(part()(
        board(matress_width + 2 * overhang, 11/4, 3/2, (X, Z, Y))
      - union()(*[translate((overhang + x, 0, 11/8))(half_cross) for x in base_longitudinal_displacements(matress_width)])
    ))


def slats(matress_width, matress_length, overhang):
    return color("peru")(
        translate((0, 0, 11/4))(slat_end(matress_width, overhang))
      + translate((0, matress_length + 2 * overhang, 11/4))(mirror((0, 1, 0))(slat_end(matress_width, overhang)))
      + union()(*[translate((0, overhang + y, 11/4))(slat_middle(matress_width, overhang)) for y in slat_displacements(matress_length)])
    )


def base(matress_width, matress_length, overhang):
    end_to_end = zip(
        (base_side(matress_length, overhang), base_support(matress_length, overhang), base_support(matress_length, overhang), base_side(matress_length, overhang)),
        base_longitudinal_displacements(matress_width),
    )
    end_to_end = union()(
        translate((0, overhang, 0))(base_end(matress_width, overhang)),
        translate((0, overhang + matress_length, 0))(mirror((0, 1, 0))(base_end(matress_width, overhang))),
        *[translate((overhang + x, 0, 0))(part) for part, x in end_to_end]
    )
    return end_to_end


def foot(rise):
    notch_depth = 2
    return part()(
        four_by_four(notch_depth + rise, (Z, X, Y))
      - hole()(translate((0, 1, rise))(cube((3.5, 1.5, notch_depth))))
      - hole()(translate((1, 0, rise))(cube((1.5, 3.5, notch_depth))))
    )


def feet_generator(matress_width, matress_length, rise):
    for x in base_longitudinal_displacements(matress_width):
        for y in base_lateral_displacements(matress_length):
            yield translate((x, y, 0))(foot(rise))


def feet(matress_width, matress_length, rise):
    return sum(feet_generator(matress_width, matress_length, rise))


def bed_without_feet(matress_width, matress_length, overhang):
    return base(matress_width, matress_length, overhang) + slats(matress_width, matress_length, overhang)


def bed_with_feet(matress_width, matress_length, overhang, rise):
    return translate((0, 0, rise))(bed_without_feet(matress_width, matress_length, overhang)) + translate((overhang - 1, overhang - 1, 0))(feet(matress_width, matress_length, rise))


def bed(matress_width, matress_length, overhang, rise=None):
    if rise: return bed_with_feet(matress_width, matress_length, overhang, rise)
    return bed_without_feet(matress_width, matress_length, overhang)
