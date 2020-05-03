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
    half_cross = hole()(cube((3/2, 3.5, 0.25)))
    return part()(
        one_by_four(length)
      - translate((length - 3/2 - overhang, 0, 0))(half_cross)
      - translate((overhang, 0, 0))(half_cross)
    )


def slat_end(matress_width, overhang):
    length = matress_width + overhang * 2
    half_cross = hole()(cube((3/2, 3.5, 0.5)))
    mortice = hole()(cube((3/2, 3/2, 3/4)))
    return part()(
        one_by_six(length)
      - translate((length - 3/2 - overhang, 2, 1/4))(half_cross)
      - translate((overhang, 2, 1/4))(half_cross)
      - translate((overhang + matress_width / 3 - 3/4, 2, 0))(mortice)
      - translate((overhang + 2 * matress_width / 3 - 3/4, 2, 0))(mortice)
    )


def base_corner_joint():
    return (
        translate((3/2, 0, 1 + 1/4 + 3/4))(rotate((0, 90, 90))(dovetail(1.25, 3/2, 3/2, 1/6)))
      + translate((0, 0, 3))(cube((3/2, 3/2, 1/2)))
      - hole()(translate((0, 3/2, 11/4))(cube((3/2, 3/2, 1/4))))
    )


def base_side(matress_length):
    half_cross = hole()(cube((3/2, 7/2, 1/2)))
    return color("tan")(part()(
        translate((0, 3/2, 0))(two_by_four(matress_length - 3, (Y, Z, X)))
      + base_corner_joint()
      + translate((0, matress_length - 3/2, 0))(base_corner_joint())
      - union()(*[translate((0, y, 3))(half_cross) for y in slat_displacements(matress_length)])
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
      - translate((0, overhang, 11/8))(half_cross)
      - translate((0, overhang + matress_length - 3/2, 11/8))(half_cross)
    ))


def base_end(matress_width):
    joint = hole()(base_corner_joint())
    tenon = cube((3/2, 3/2, 3/4))
    half_cross = hole()(cube((3/2, 3/2, 11/8)))
    return color("saddlebrown")(part()(
        board(matress_width, 11/4, 3/2, (X, Z, Y))
      - joint
      - translate((matress_width, 0, 0))(mirror((1, 0, 0))(joint))
      + translate((matress_width / 3 - 3/4, 0, 11/4))(tenon)
      + translate((2 * matress_width / 3 - 3/4, 0, 11/4))(tenon)
      - translate((matress_width / 3 - 3/4, 0, 0))(half_cross)
      - translate((2 * matress_width / 3 - 3/4, 0, 0))(half_cross)
    ))


def slats(matress_width, matress_length, overhang):
    return color("peru")(
        translate((0, 0, 11/4))(slat_end(matress_width, overhang))
      + translate((0, matress_length + 2 * overhang, 11/4))(mirror((0, 1, 0))(slat_end(matress_width, overhang)))
      + union()(*[translate((0, overhang + y, 11/4))(slat_middle(matress_width, overhang)) for y in slat_displacements(matress_length)])
    )


def base(matress_width, matress_length, overhang):
    end_to_end = zip(
        (base_side(matress_length), base_support(matress_length, overhang), base_support(matress_length, overhang), base_side(matress_length)),
        base_longitudinal_displacements(matress_width),
        (overhang, 0, 0, overhang)
    )
    end_to_end = union()(
        translate((0, overhang, 0))(base_end(matress_width)),
        translate((0, overhang + matress_length, 0))(mirror((0, 1, 0))(base_end(matress_width))),
        translate((0, overhang, 0))(base_side(matress_length)),
        translate((matress_width, overhang, 0))(mirror((1, 0, 0))(base_side(matress_length))),
        *[translate((x, y, 0))(part) for part, x, y in end_to_end]
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


def bed(matress_width, matress_length, overhang, rise=None):
    if rise:
        return translate((0, 0, rise))(bed(matress_width, matress_length, overhang)) + translate((overhang - 1, overhang - 1, 0))(feet(matress_width, matress_length, rise))
    return translate((overhang, 0, 0))(base(matress_width, matress_length, overhang)) + slats(matress_width, matress_length, overhang)
