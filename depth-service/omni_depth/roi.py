import numpy as np


def front_lower_roi(depth_map, width_fraction=0.4, y_start_fraction=0.5, y_end_fraction=0.9):
    depth = np.asarray(depth_map)
    if depth.ndim != 2:
        raise ValueError("depth_map must be a 2D array")

    height, width = depth.shape
    roi_width = max(1, int(width * width_fraction))
    x0 = (width - roi_width) // 2
    x1 = x0 + roi_width
    y0 = int(height * y_start_fraction)
    y1 = int(height * y_end_fraction)
    return depth[y0:y1, x0:x1]


def percentile_distance(roi, percentile=5):
    values = np.asarray(roi, dtype=float)
    valid = values[np.isfinite(values) & (values > 0)]
    if valid.size == 0:
        return None
    return float(np.percentile(valid, percentile))
