from decimal import Decimal, getcontext
from shapely.ops import unary_union
from tree import ChristmasTree
from collision import check_no_overlap

getcontext().prec = 25
SCALE = Decimal('1e18')


def score_submission(df):
    """
    df columns: id, x, y, deg (WITHOUT 's' prefix)
    """
    total_score = Decimal('0')

    df = df.copy()
    df['group'] = df['id'].str.split('_').str[0]

    for group, g in df.groupby('group'):
        trees = [
            ChristmasTree(row.x, row.y, row.deg)
            for row in g.itertuples()
        ]

        polygons = [t.polygon for t in trees]

        # collision check
        check_no_overlap(polygons)

        # bounding square
        bounds = unary_union(polygons).bounds
        side = max(bounds[2] - bounds[0], bounds[3] - bounds[1])

        n = Decimal(len(polygons))
        group_score = (Decimal(side) ** 2) / (SCALE ** 2) / n
        total_score += group_score

    return float(total_score)
