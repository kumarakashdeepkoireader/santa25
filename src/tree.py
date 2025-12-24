from decimal import Decimal, getcontext
from shapely import affinity
from shapely.geometry import Polygon

getcontext().prec = 25
SCALE = Decimal('1e18')


class ChristmasTree:
    def __init__(self, x='0', y='0', angle='0'):
        self.x = Decimal(x)
        self.y = Decimal(y)
        self.angle = Decimal(angle)

        trunk_w = Decimal('0.15')
        trunk_h = Decimal('0.2')
        base_w = Decimal('0.7')
        mid_w = Decimal('0.4')
        top_w = Decimal('0.25')

        tip_y = Decimal('0.8')
        tier1_y = Decimal('0.5')
        tier2_y = Decimal('0.25')
        base_y = Decimal('0.0')
        trunk_bottom_y = -trunk_h

        self.local_polygon = Polygon([
            (0, tip_y),
            (top_w/2, tier1_y), (top_w/4, tier1_y),
            (mid_w/2, tier2_y), (mid_w/4, tier2_y),
            (base_w/2, base_y),
            (trunk_w/2, base_y), (trunk_w/2, trunk_bottom_y),
            (-trunk_w/2, trunk_bottom_y), (-trunk_w/2, base_y),
            (-base_w/2, base_y),
            (-mid_w/4, tier2_y), (-mid_w/2, tier2_y),
            (-top_w/4, tier1_y), (-top_w/2, tier1_y),
        ])

        scaled = affinity.scale(self.local_polygon, xfact=float(SCALE), yfact=float(SCALE))
        rotated = affinity.rotate(scaled, float(self.angle), origin=(0, 0))
        self.polygon = affinity.translate(
            rotated,
            xoff=float(self.x * SCALE),
            yoff=float(self.y * SCALE),
        )
