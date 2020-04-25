from solid import cube, linear_extrude, polygon, rotate, translate, union
from solid.objects import render


def dovetail(width, length, depth, ratio):
    return linear_extrude(depth)(
        polygon((
            (0, 0),
            (width, 0),
            (width - length * ratio, length),
            (length * ratio, length),
        ))
    )


def base_side_dovetail_joint():
    body = rotate((90, -90, 0))(dovetail(0.75, 1.5, 1.5, 1/6))
    return union()(
        translate((1.5, 1.5, 0.25))(body),
        translate((1.5, 1.5, 1.75))(body),
    )


def base_side_bridle_joint():
    cheek = cube((1.5, 3.5, 0.25))
    return union()(
        translate((0, 0, 2.75))(cheek),
        translate((0, 0, 3.25))(cheek),
    )
