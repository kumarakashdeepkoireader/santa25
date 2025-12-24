from shapely.strtree import STRtree


def check_no_overlap(polygons):
    """
    Raises ValueError if any two polygons overlap
    (touching edges is allowed).
    """
    rtree = STRtree(polygons)

    for i, poly in enumerate(polygons):
        candidates = rtree.query(poly)
        for j in candidates:
            if i == j:
                continue
            other = polygons[j]
            if poly.intersects(other) and not poly.touches(other):
                raise ValueError("Overlap detected")

    return True
