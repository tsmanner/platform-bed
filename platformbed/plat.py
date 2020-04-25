import platformbed.joints

from solid import color, cube, rotate, mirror, translate, union, difference


platform_color = color((165/255, 96/255, 45/255))


def end(width):
    body = translate((-2, -2, 2.75))(cube((width+4, 5.5, 0.75)))
    bridle = platformbed.joints.base_side_bridle_joint()
    tenon = cube((1.5, 1.5, 0.75))
    return (
        body
      - bridle
      - translate((width-1.5, 0, 0))(platformbed.joints.base_side_bridle_joint())
      - translate((width/3-0.75, 0, 2.75))(tenon)
      - translate((2*width/3-0.75, 0, 2.75))(tenon)
    )


def slat(width):
    body = translate((-2, 0, 0))(cube((width+4, 3.5, 0.75)))
    cross_halving = cube((1.5, 3.5, 0.25))
    return translate((0, 0, 2.75))(
        body
      - cross_halving
      - translate((width-1.5, 0, 0))(cross_halving)
    )


def platform(width, length, height):
    foot = end(width)
    head = translate((0, length, 0))(
        mirror((0, 1, 0))(foot)
    )
    slats = union()(
        [
            translate((0, y, 0))(slat(width))
            for y in range(0, 70, 7)
        ]
    )
    return (
        platform_color(head)
      + platform_color(foot)
      + platform_color(translate((0, 6.5, 0))(slats))
    )
