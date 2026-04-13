import numpy as np
import matplotlib.pyplot as plt

def beth_move(glasses):
    n = len(glasses)
    best_pair, best_total = 0, -1
    for i in range(n):
        pair_total = glasses[i] + glasses[(i + 1) % n]
        if pair_total > best_total:
            best_total, best_pair = pair_total, i
    glasses = glasses.copy()
    glasses[best_pair] = 0
    glasses[(best_pair + 1) % n] = 0
    return glasses

def ali_move(glasses):
    return glasses + 0.5 / len(glasses)

def simulate_tk(n, rounds=30):
    glasses = np.zeros(n)
    tk_vals = []
    for _ in range(rounds):
        glasses = ali_move(glasses)
        glasses = beth_move(glasses)
        tk_vals.append(sum(glasses))
    return tk_vals

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, n in zip(axes, [3, 4]):
    tk = simulate_tk(n)
    ax.plot(tk, color='steelblue', marker='o', ms=4)
    ax.axhline(0.5, color='red', linestyle='--', label='t_k = 0.5 bound')
    ax.set_title(f'n = {n} glasses')
    ax.set_xlabel('Round k'); ax.set_ylabel('Total water t_k')
    ax.legend(); ax.set_ylim(0, 0.6)
plt.tight_layout()
plt.savefig('tk_invariant.png', dpi=150)
plt.show()
