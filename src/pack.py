import math


def grid_pack(n, dx=0.8, dy=1.1):
    """
    Returns list of (x, y, deg) placements for n trees
    """
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    placements = []

    start_x = - (cols - 1) * dx / 2
    start_y = - (rows - 1) * dy / 2

    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= n:
                break

            x = start_x + c * dx
            y = start_y + r * dy
            placements.append((x, y, 0.0))
            idx += 1

    return placements



import math


def hex_pack(n, dx=0.71, dy=0.81, rotations=(0.0, 180.0)):
    """
    Hex-style staggered packing.
    rotations: tuple used to alternate rows
    """
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    placements = []

    start_x = - (cols - 1) * dx / 2
    start_y = - (rows - 1) * dy / 2

    idx = 0
    for r in range(rows):
        row_offset = (dx / 2) if (r % 2 == 1) else 0.0
        angle = rotations[r % len(rotations)]

        for c in range(cols):
            if idx >= n:
                break

            x = start_x + c * dx + row_offset
            y = start_y + r * dy

            placements.append((x, y, angle))
            idx += 1

    return placements
