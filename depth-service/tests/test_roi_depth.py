import unittest

import numpy as np

from omni_depth.roi import front_lower_roi, percentile_distance


class RoiDepthTest(unittest.TestCase):
    def test_front_lower_roi_selects_center_bottom_band(self):
        depth = np.arange(100).reshape((10, 10))

        roi = front_lower_roi(depth)

        self.assertEqual(roi.shape, (4, 4))
        self.assertEqual(roi[0, 0], depth[5, 3])
        self.assertEqual(roi[-1, -1], depth[8, 6])

    def test_percentile_distance_ignores_invalid_values(self):
        roi = np.array([[0.0, -1.0, np.nan], [1.0, 2.0, 3.0]])

        self.assertEqual(percentile_distance(roi, percentile=50), 2.0)


if __name__ == "__main__":
    unittest.main()
