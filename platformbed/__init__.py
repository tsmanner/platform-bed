from solid import cube, hole, mirror, part, rotate, translate
from .joints import dovetail

X = 0
Y = 1
Z = 2


def board(length, width, thickness, axis):
    length = length
    width = width
    thickness = thickness
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
    half_cross = hole()(cube((3/2, 5.5, 0.5)))
    mortice = hole()(cube((3/2, 3/2, 3/4)))
    return part()(
        one_by_six(length)
      - translate((length - 3/2 - overhang, 0, 0))(half_cross)
      - translate((overhang, 0, 0))(half_cross)
      - translate((matress_width / 3 - 3/4, 2, 0))(mortice)
      - translate((2 * matress_width / 3 - 3/4, 2, 0))(mortice)
    )


def base_corner_joint():
    return (
        translate((3/2, 0, 1 + 1/4 + 3/4))(rotate((0, 90, 90))(dovetail(1.25, 3/2, 3/2, 1/6)))
      + translate((0, 0, 3))(cube((3/2, 3/2, 0.5)))
    )


def base_side(matress_length):#, num_slats, slat_width):
    return part()(
        translate((0, 3/2, 0))(two_by_four(matress_length - 3, (Y, Z, X)))
      + base_corner_joint()
      + translate((0, matress_length - 3/2, 0))(base_corner_joint())
    )


def base_support(matress_length, overhang):
    half_cross = hole()(cube((3/2, 3/2, 11/8)))
    return part()(
        board(matress_length + overhang * 2, 11/4, 3/2, (Y, Z, X))
      - translate((0, overhang, 11/8))(half_cross)
      - translate((0, overhang + matress_length - 3/2, 11/8))(half_cross)
    )


def base_end(matress_width):
    joint = hole()(base_corner_joint())
    tenon = cube((3/2, 3/2, 3/4))
    return part()(
        board(matress_width, 11/4, 3/2, (X, Z, Y))
      - joint
      - translate((matress_width, 0, 0))(mirror((1, 0, 0))(joint))
      + translate((matress_width / 3 - 3/4, 0, 11/4))(tenon)
      + translate((2 * matress_width / 3 - 3/4, 0, 11/4))(tenon)
    )


