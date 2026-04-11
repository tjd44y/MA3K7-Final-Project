from fractions import Fraction


def simulate(N):
    HALF = Fraction(1, 2)
    QUARTER = Fraction(1, 4)
    threshold = Fraction(N - 3, 4 * (N - 2))

    def beth_all_moves(glasses):
        """All N possible Beth moves — every adjacent pair in the circle."""
        moves = []
        for i in range(N):
            g = list(glasses)
            g[i] = Fraction(0)
            g[(i + 1) % N] = Fraction(0)
            moves.append(tuple(g))
        return moves

    def overflow(glasses):
        return any(g > Fraction(1) for g in glasses)

    def apply(glasses, dist):
        return tuple(glasses[i] + dist[i] for i in range(N))

    def ali_strategy(glasses, phase):
        zero = Fraction(0)

        if phase == 1:
            # Equalise all glasses, spread remainder evenly
            current_max = max(glasses)
            top_ups = [max(zero, current_max - g) for g in glasses]
            remaining = HALF - sum(top_ups)
            extra = remaining / N
            return tuple(top_ups[i] + extra for i in range(N))

        elif phase == 2:
            # Leave the emptiest glass empty, equalise the rest
            min_idx = min(range(N), key=lambda i: glasses[i])
            current_max = max(glasses)
            top_ups = [max(zero, current_max - g) for g in glasses]
            top_ups[min_idx] = zero
            remaining = HALF - sum(top_ups)
            extra = remaining / (N - 1)
            return tuple(
                zero if i == min_idx else top_ups[i] + extra
                for i in range(N)
            )

        elif phase == 3:
            # Add 1/4 to the two most-full non-adjacent glasses
            best_pair, best_total = None, Fraction(-1)
            for i in range(N):
                for j in range(i + 1, N):
                    adjacent = (j == i + 1) or (i == 0 and j == N - 1)
                    if not adjacent:
                        total = glasses[i] + glasses[j]
                        if total > best_total:
                            best_total, best_pair = total, (i, j)
            dist = [zero] * N
            dist[best_pair[0]] = QUARTER
            dist[best_pair[1]] = QUARTER
            return tuple(dist)

        else:
            # Phase 4: dump everything into the most-full glass
            best = max(range(N), key=lambda i: glasses[i])
            dist = [zero] * N
            dist[best] = HALF
            return tuple(dist)

    print(f"n = {N},  threshold a_k > {threshold} = {float(threshold):.4f}")
    print("=" * 58)
    print(f"{'Round':<8} {'Phase':<8} {'Unique states':<16} {'Ali wins':<12} {'Continue'}")
    print("-" * 58)

    # Each entry: (glasses tuple, rounds spent in phase 2+)
    branches = {(tuple([Fraction(0)] * N), 0)}
    rnd = 0

    while branches:
        rnd += 1
        wins_this_round = 0
        next_branches = set()
        phase_this_round = None

        for state, p2count in branches:
            # Determine current phase
            a_k = max(state)
            if a_k <= threshold:
                phase, next_p2 = 1, 0
            elif p2count == 0:
                phase, next_p2 = 2, 1
            elif p2count == 1:
                phase, next_p2 = 3, 2
            else:
                phase, next_p2 = 4, 3
            phase_this_round = phase

            dist = ali_strategy(state, phase)
            after_ali = apply(state, dist)

            if overflow(after_ali):
                wins_this_round += 1
            else:
                for b in beth_all_moves(after_ali):
                    next_branches.add((b, next_p2))

        print(f"{rnd:<8} {phase_this_round:<8} {len(branches):<16} {wins_this_round:<12} {len(next_branches)}")
        branches = next_branches

        if rnd > 100:
            print("ERROR: exceeded round limit — strategy may be incomplete.")
            break

    print("=" * 58)
    if not branches:
        print(f"Result: ALI WINS IN ALL BRANCHES for n = {N}\n")
    else:
        print(f"WARNING: {len(branches)} unresolved branches for n = {N}\n")


if __name__ == "__main__":
    for N in [6, 7, 8]:
        simulate(N)
