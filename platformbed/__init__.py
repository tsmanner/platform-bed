from solid import cube, hole, mirror, part, translate


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


def two_by_four(length, axis=(X, Y, Z)):
    return board(length, 3.5, 1.5, axis)


def slat(matress_width, overhang):
    length = matress_width + overhang * 2
    half = (
        one_by_four(length / 2)
      - hole()(translate((length / 2 - 1.5 - overhang, 0, 0))(cube((1.5, 3.5, 0.25))))
    )
    return part()(translate((length / 2, 0, 0))(
        half + 
        mirror((1, 0, 0))(
            half
        )
    ))


def side(matress_length):#, num_slats, slat_width):
    length = matress_length
    half = two_by_four(length, (Y, Z, X))
    return half
