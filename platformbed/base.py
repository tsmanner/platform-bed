import platformbed.joints

from solid import color, cube, rotate, mirror, translate, union, difference


end_color = color((135/255, 68/255, 20/255))
side_color = color((234/255, 159/255, 105/255))


# In terms of the matress width/length, and the bed platform height
def side(length):
    body = (
        translate((0, 1.5, 0))(cube((1.5, length-3, 3.5)))
      - translate((0, 0, 2.75))(cube((1.5, 3.5, 0.75)))
      - translate((0, length-3.5, 2.75))(cube((1.5, 3.5, 0.75)))
    )
    slats = union()(
        [
            translate((0, y, 3))(cube((1.5, 3.5, 0.5)))
            for y in range(0, 70, 7)
        ]
    )
    return (
        body
      + platformbed.joints.base_side_dovetail_joint()
      + platformbed.joints.base_side_bridle_joint()
      + translate((0, length-1.5, 0))(platformbed.joints.base_side_dovetail_joint())
      + translate((0, length-3.5, 0))(platformbed.joints.base_side_bridle_joint())
      - translate((0, 6.5, 0))(slats)
    )


def end(width):
    body = cube((width, 1.5, 2.75))
    tenon = cube((1.5, 1.5, 0.75))
    return (
        body
      + translate((width/3-0.75, 0, 2.75))(tenon)
      + translate((2*width/3-0.75, 0, 2.75))(tenon)
      - platformbed.joints.base_side_dovetail_joint()
      - translate((width, 0, 0))(mirror((1, 0, 0))(platformbed.joints.base_side_dovetail_joint()))
      - translate((width/2-0.75, 0, 1.375))(cube((1.5, 1.5, 1.375)))
    )


def base(width, length, height):
    left = side(length)
    right = translate((width, 0, 0))(
        mirror((1, 0, 0))(left)
    )
    center = translate((width/2-0.75, 0, 0))(
        translate((0, 1.5, 0))(cube((1.5, length-3, 1.375)))
      + translate((0, 0, 1.375))(cube((1.5, length, 1.375)))
    )
    foot = end(width)
    head = translate((0, length, 0))(
        mirror((0, 1, 0))(foot)
    )
    return union()(
        end_color(head),
        end_color(foot),
        side_color(left),
        side_color(right),
        side_color(center),
    )
