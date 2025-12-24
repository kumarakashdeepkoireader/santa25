import matplotlib.pyplot as plt
from tree import ChristmasTree
from shapely.geometry import Polygon


def plot_trees(placements, title="Packing"):
    fig, ax = plt.subplots(figsize=(6, 6))

    polys = []
    for i, (x, y, deg) in enumerate(placements):
        t = ChristmasTree(str(x), str(y), str(deg))
        poly = t.polygon
        xs, ys = poly.exterior.xy
        ax.fill(xs, ys, alpha=0.6)
        ax.text(x, y, str(i), color="red", fontsize=8)

        polys.append(poly)

    from shapely.ops import unary_union
    bounds = unary_union(polys).bounds
    side = max(bounds[2] - bounds[0], bounds[3] - bounds[1])

    ax.set_xlim(bounds[0], bounds[0] + side)
    ax.set_ylim(bounds[1], bounds[1] + side)
    ax.set_aspect("equal")
    ax.set_title(title)

    plt.show()
