import os
from typing import List, Dict

import numpy as np
import matplotlib.pyplot as plt

def create_mouse_heatmap(
        events: List[Dict],
        output_path: str = "datos/processed/mouse_heatmap.png",
        only_click: bool = True,
        bins: int = 100,
):
    if only_click:
        filtered = [e for e in events if e.get("type") == "click"]
    else:
        filtered = [e for e in events if "x" in e and "y" in e]

    if not filtered:
        print("⚠ Not enough events for create the heatmap.")
        return

    xs = [e["x"] for e in filtered if "x" in e]
    ys = [e["y"] for e in filtered if "y" in e]

    if not xs or not ys:
        print("No cords found in the events list.")
        return
    min_y = min(ys)
    min_x = min(xs)
    max_x = max(xs)
    max_y = max(ys)

    print(f"[HEATMAP] Rango X: {min_x} .. {max_x}")
    print(f"[HEATMAP] Rango Y: {min_y} .. {max_y}")

    if min_x == max_x or min_y == max_y:
        print("El rango de coordenadas es demasiado pequeño para un heatmap.")
        return

    xs_norm = [x - min_x for x in xs]
    ys_norm = [y - min_y for y in ys]

    width = max_x - min_x
    height = max_y - min_y

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    heatmap, xedges, yedges = np.histogram2d(
        xs_norm,
        ys_norm,
        bins=bins,
        range=[[0, width], [0, height]],
    )

    plt.figure(figsize=[6, 6])
    plt.imshow(
        heatmap.T,
        origin="lower",
        interpolation="nearest",
        cmap="hot"
    )
    plt.title("Mouse Heatmap")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.colorbar(label="Use frequency")

    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Heatmap saved to {output_path}")


