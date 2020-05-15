from itertools import repeat
from solid import color, cube, hole, mirror, part, rotate, translate, union, OpenSCADObject
from solid import OpenSCADObject, scad_render
from .joints import dovetail

X = 0
Y = 1
Z = 2


class Board(OpenSCADObject):
    def __init__(self, length, width, thickness, axis=(X, Y, Z)):
        super().__init__("cube", {})
        self.length = length
        self.width = width
        self.thickness = thickness
        self.axis = axis

    def _render(self, *args, **kwargs):
        return cube(tuple(s[0] for s in sorted(
            zip(
                (self.length, self.width, self.thickness),
                self.axis,
            ),
            key=lambda z: z[1]
        )))()._render(*args, **kwargs)

    def __repr__(self):
        return f'{self.thickness} x {self.width} x {self.length}"'


class OneByFour(Board):
    WIDTH = 3.5
    THICKNESS = 0.75
    def __init__(self, length, axis=(X, Y, Z)):
        super().__init__(length, self.WIDTH, self.THICKNESS, axis)

    def __repr__(self):
        return f'1 x 4 x {self.length}" ({super().__repr__()})'


class OneBySix(Board):
    WIDTH = 5.5
    THICKNESS = 0.75
    def __init__(self, length, axis=(X, Y, Z)):
        super().__init__(length, self.WIDTH, self.THICKNESS, axis)

    def __repr__(self):
        return f'1 x 6 x {self.length}" ({super().__repr__()})'


class TwoByFour(Board):
    WIDTH = 3.5
    THICKNESS = 1.5
    def __init__(self, length, axis=(X, Y, Z)):
        super().__init__(length, self.WIDTH, self.THICKNESS, axis)

    def __repr__(self):
        return f'2 x 4 x {self.length}" ({super().__repr__()})'


class FourByFour(Board):
    WIDTH = 3.5
    THICKNESS = 3.5
    def __init__(self, length, axis=(X, Y, Z)):
        super().__init__(length, self.WIDTH, self.THICKNESS, axis)

    def __repr__(self):
        return f'4 x 4 x {self.length}" ({super().__repr__()})'


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
        OneByFour(length)
      - translate((length - 3/2 - overhang, 0, 0))(half_cross)
      - translate((overhang, 0, 0))(half_cross)
    )


def slat_end(matress_width, overhang):
    length = matress_width + overhang * 2
    half_cross = hole()(cube((3/2, 11/2, 1/4)) + translate((0, 2, 0))(cube((3/2, 3/2, 3/4))))
    return part()(
        OneBySix(length)
      - translate((length - 3/2 - overhang, 0, 0))(half_cross)
      - translate((overhang, 0, 0))(half_cross)
    )


def base_side(matress_length, overhang):
    end_slat_half_cross = hole()(cube((3/2, 2, 1/2)) + translate((0, 7/2, 0))(cube((3/2, 2, 1/2))))
    slat_half_cross = hole()(cube((3/2, 7/2, 1/2)))
    base_half_cross = hole()(cube((3/2, 3/2, 11/8)))
    return color("tan")(part()(
        TwoByFour(matress_length + 2 * overhang, (Y, Z, X))
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
        Board(matress_length + overhang * 2, 11/4, 3/2, (Y, Z, X))
      - translate((0, overhang, 0))(half_cross)
      - translate((0, overhang + matress_length - 3/2, 0))(half_cross)
    ))


def base_end(matress_width, overhang):
    half_cross = hole()(cube((3/2, 3/2, 11/8)))
    return color("saddlebrown")(part()(
        Board(matress_width + 2 * overhang, 11/4, 3/2, (X, Z, Y))
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
        FourByFour(notch_depth + rise, (Z, X, Y))
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
