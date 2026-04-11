import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def draw_glasses(ax, glasses, title, highlight=None):
    n = len(glasses)
    angles = [2 * np.pi * i / n - np.pi / 2 for i in range(n)]
    r = 1.0
    for i, (a, g) in enumerate(zip(angles, glasses)):
        x, y = r * np.cos(a), r * np.sin(a)
        color = '#5DCAA5' if g > 0 else '#D3D1C7'
        if highlight and i in highlight:
            color = '#F09595'
        circle = plt.Circle((x, y), 0.18, color=color, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y + 0.01, f'{g:.2f}', ha='center', va='center',
               fontsize=7.5, fontweight='bold', zorder=4)
        ax.text(x * 1.35, y * 1.35, str(i+1), ha='center', va='center', fontsize=8)
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(title, fontsize=9, pad=4)

states = []
glasses = np.zeros(8)

glasses[[0,2,4,6]] += 1/8
states.append((glasses.copy(), 'After Ali round 1', None))
glasses[[0,1]] = 0  # Beth empties 1,2
states.append((glasses.copy(), 'After Beth round 1', {0,1}))

glasses[[2,4,6]] += 1/6
states.append((glasses.copy(), 'After Ali round 2', None))
glasses[[2,3]] = 0  # Beth empties 3,4
states.append((glasses.copy(), 'After Beth round 2', {2,3}))

glasses[[4,6]] += 1/4
states.append((glasses.copy(), 'After Ali round 3', None))
glasses[[4,5]] = 0  # Beth empties 5,6
states.append((glasses.copy(), 'After Beth round 3', {4,5}))

glasses[6] += 0.5
states.append((glasses.copy(), 'Ali wins! Glass 7 overflows', {6}))

fig, axes = plt.subplots(3, 3, figsize=(9, 9))
for ax, (g, title, hl) in zip(axes.flat, states):
    draw_glasses(ax, g, title, hl)

axes.flat[7].set_visible(False)
axes.flat[8].set_visible(False)

green = mpatches.Patch(color='#5DCAA5', label='Water present')
red   = mpatches.Patch(color='#F09595', label='Emptied / overflow')
gray  = mpatches.Patch(color='#D3D1C7', label='Empty')
fig.legend(handles=[green, red, gray], loc='lower center', ncol=3, fontsize=9)
plt.suptitle("Ali's alternating strategy — n=8", fontsize=13)
plt.tight_layout()
plt.savefig("n8_strategy.png", dpi=300, bbox_inches='tight')
plt.show()
