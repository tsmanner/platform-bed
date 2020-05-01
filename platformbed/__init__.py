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
        super().__init__(length, , axis)


def slat_displacements(matress_length):
    step = 7
    offset = 7/4 + ((matress_length - 7) % step) / 2
    displacement = 3.5
    while displacement < (matress_length - step):
        yield offset + displacement
        displacement += step


def middle_slat(matress_width, overhang):
    length = matress_width + overhang * 2
    half_cross = hole()(cube((3/2, 3.5, 0.25)))
    return part()(
        one_by_four(length)
      - translate((length - 3/2 - overhang, 0, 0))(half_cross)
      - translate((overhang, 0, 0))(half_cross)
    )


def end_slat(matress_width, overhang):
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
        translate((0, 0, 11/4))(end_slat(matress_width, overhang))
      + translate((0, matress_length + 2 * overhang, 11/4))(mirror((0, 1, 0))(end_slat(matress_width, overhang)))
      + union()(*[translate((0, overhang + y, 11/4))(middle_slat(matress_width, overhang)) for y in slat_displacements(matress_length)])
    )


def base(matress_width, matress_length, overhang):
    return (
        translate((0, overhang, 0))(base_end(matress_width))
      + translate((0, overhang + matress_length, 0))(mirror((0, 1, 0))(base_end(matress_width)))
      + translate((0, overhang, 0))(base_side(matress_length))
      + translate((matress_width, overhang, 0))(mirror((1, 0, 0))(base_side(matress_length)))
      + translate((matress_width / 3 - 3/4, 0, 0))(base_support(matress_length, overhang))
      + translate((2 * matress_width / 3 - 3/4, 0, 0))(base_support(matress_length, overhang))
    )


def bed(matress_width, matress_length, overhang):
    return translate((overhang, 0, 0))(base(matress_width, matress_length, overhang)) + slats(matress_width, matress_length, overhang)
