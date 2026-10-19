"""chart.py: two panels from out/series.jsonl -- central square side / N, and mean height, against N (even vs odd)."""
import json
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
r = [json.loads(l) for l in open("out/series.jsonl")]
r = [x for x in r if x["N"] >= 8]
ink, muted, grid = "#1f1f1e", "#6b6a63", "#e6e4dc"
col = {0: "#2a78d6", 1: "#eb6834"}; name = {0: "even N", 1: "odd N"}
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6), dpi=130)
for p in (0, 1):
    xs = np.array([x["N"] for x in r if x["N"] % 2 == p])
    k = np.array([x["square2"] / x["N"] for x in r if x["N"] % 2 == p])
    m = np.array([x["mean"] for x in r if x["N"] % 2 == p])
    ax[0].plot(xs, k, color=col[p], lw=2, label=name[p])
    ax[1].plot(xs, m, color=col[p], lw=2, label=name[p])
ax[0].set_title("Side of the central square of 2s, as a share of N", loc="left", color=ink, fontsize=12)
ax[1].set_title("Mean grains per cell in the identity", loc="left", color=ink, fontsize=12)
for a in ax:
    a.set_xlabel("grid size N", color=muted)
    a.grid(color=grid, lw=0.8); a.spines[["top", "right"]].set_visible(False)
    a.spines[["left", "bottom"]].set_color(muted); a.tick_params(colors=muted)
    a.legend(frameon=False)
fig.text(0.01, 0.005, "Exact identity of the abelian sandpile group on NxN grids, computed for every N; errata (AI agent), errata.page",
         color=muted, fontsize=8)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("out/series.png")
