print('-- Medicine for Rudolph --')

from typing import Dict, List

def _parse_mappings_dict(block: str) -> Dict[str, List[str]]:
    """Parse mapping block (lines like 'H => HO') into a dict lhs -> [rhs,...].

    Empty or malformed lines are ignored. Order of RHS values follows file order.
    """
    out: Dict[str, List[str]] = {}
    for raw in block.splitlines():
        line = raw.strip()
        if not line or '=>' not in line:
            continue
        left, right = [p.strip() for p in line.split('=>', 1)]
        out.setdefault(left, []).append(right)
    return out

with open('data.txt', 'r') as file:
    raw_mappings, d_molecule = file.read().split('\n\n')
    d_mappings = _parse_mappings_dict(raw_mappings)

with open('test.txt', 'r') as test_file:
    raw_mappings_t, t_molecule = test_file.read().split('\n\n')
    t_mappings = _parse_mappings_dict(raw_mappings_t)

def find_distinct_molecules(molecule: str, mappings: Dict[str, List[str]]) -> int:
    """Find number of distinct molecules after one replacement."""
    distinct_molecules = set()
    for i in range(len(molecule)):
        for lhs, rhss in mappings.items():
            if molecule.startswith(lhs, i):
                for rhs in rhss:
                    new_molecule = molecule[:i] + rhs + molecule[i + len(lhs):]
                    distinct_molecules.add(new_molecule)
    return len(distinct_molecules)

print('-- Part 1 --')
print(f'Test: {find_distinct_molecules(t_molecule.strip(), t_mappings)}')
print(f'Data: {find_distinct_molecules(d_molecule.strip(), d_mappings)}')


import heapq
import re

_token_re = re.compile(r'[A-Z][a-z]?')


def tokenize_count(mol: str) -> int:
    return len(_token_re.findall(mol))


def find_min_steps_a_star(target: str, mappings: Dict[str, List[str]]) -> int | None:
    """Backward A* search: start from target and reduce (rhs -> lhs) toward 'e'.

    Uses token-count heuristic (fewer tokens -> closer to 'e'). Returns number
    of steps if found, otherwise None.
    """
    # Build reversed map: rhs -> [lhs, ...]
    reversed_map: Dict[str, List[str]] = {}
    for lhs, rhss in mappings.items():
        for rhs in rhss:
            reversed_map.setdefault(rhs, []).append(lhs)

    def heuristic(mol: str) -> int:
        # refined heuristic used by many AoC Day 19 solutions:
        # tokens - count(Rn) - count(Ar) - 2*count(Y) - 1
        tokens = _token_re.findall(mol)
        cnt = {tok: 0 for tok in ('Rn', 'Ar', 'Y')}
        for t in tokens:
            if t in cnt:
                cnt[t] += 1
        return max(0, len(tokens) - cnt['Rn'] - cnt['Ar'] - 2 * cnt['Y'] - 1)

    # priority queue entries: (f = g + h, g, molecule)
    pq: list = []
    start = target
    heapq.heappush(pq, (heuristic(start), 0, start))
    best_g: Dict[str, int] = {start: 0}

    while pq:
        f, g, mol = heapq.heappop(pq)
        if mol == 'e':
            return g
        # Skip if we have already a better g for this molecule
        if g != best_g.get(mol, None):
            continue

        # enumerate all single-step reductions (replace any rhs with its lhs)
        for rhs, lhss in reversed_map.items():
            start_idx = mol.find(rhs)
            while start_idx != -1:
                for lhs in lhss:
                    new = mol[:start_idx] + lhs + mol[start_idx + len(rhs):]
                    new_g = g + 1
                    if new_g < best_g.get(new, 10**9):
                        best_g[new] = new_g
                        heapq.heappush(pq, (new_g + heuristic(new), new_g, new))
                start_idx = mol.find(rhs, start_idx + 1)

    return None


import random


def greedy_random_reverse(target: str, mappings: Dict[str, List[str]], tries: int = 10000) -> int | None:
    """Randomized greedy backward search: try many random reduction paths.

    For each trial, repeatedly apply random rhs->lhs reductions (preferring longer
    rhs first) until reaching 'e' or getting stuck. Return minimum steps found.
    """
    # Build reversed map: rhs -> [lhs, ...]
    reversed_map: Dict[str, List[str]] = {}
    for lhs, rhss in mappings.items():
        for rhs in rhss:
            reversed_map.setdefault(rhs, []).append(lhs)

    rhs_list = sorted(reversed_map.keys(), key=len, reverse=True)
    best = None

    for trial in range(tries):
        mol = target
        steps = 0
        max_steps_per_trial = 500

        while mol != 'e' and steps < max_steps_per_trial:
            # pick a random rhs, biased toward longer ones (better reductions)
            if random.random() < 0.8 and len(rhs_list) > 0:
                # pick from top 25% (longest rhs)
                idx = random.randint(0, min(len(rhs_list) // 4, len(rhs_list) - 1))
                rhs = rhs_list[idx]
            else:
                rhs = random.choice(rhs_list)

            pos = mol.find(rhs)
            if pos == -1:
                # try a few random candidates before giving up
                found = False
                for _ in range(10):
                    rhs_try = random.choice(rhs_list)
                    pos_try = mol.find(rhs_try)
                    if pos_try != -1:
                        rhs = rhs_try
                        pos = pos_try
                        found = True
                        break
                if not found:
                    break

            # apply reduction
            lhs_candidates = reversed_map[rhs]
            lhs = random.choice(lhs_candidates)
            mol = mol[:pos] + lhs + mol[pos + len(rhs):]
            steps += 1

        if mol == 'e':
            if best is None or steps < best:
                best = steps
                print(f'  Trial {trial}: found solution with {steps} steps')

    return best


print('-- Part 2 --')
print(f'Test: {greedy_random_reverse(t_molecule.strip(), t_mappings, tries=5000)}')
print(f'Data: {greedy_random_reverse(d_molecule.strip(), d_mappings, tries=1000000)}')


def greedy_random_reverse_improved(target: str, reversed_map, tries=10000, max_steps=1000, seed=None):
    """
    Randomized greedy reverse that:
    - prefers longer rhs first but adds randomness
    - picks a random occurrence position for chosen rhs
    - stops a trial if it goes over max_steps
    Returns best steps found (int) or None if none found.
    """
    if seed is not None:
        random.seed(seed)
    rhs_list = sorted(reversed_map.keys(), key=len, reverse=True)
    best = None

    for t in range(tries):
        mol = target
        steps = 0
        # small jitter to avoid identical behavior each trial
        jitter = random.random()
        while mol != 'e' and steps < max_steps:
            # pick candidate rhs in two-stage way:
            # - mostly pick from top-longest, sometimes anywhere
            if random.random() < 0.8:
                candidates = rhs_list[:max(1, len(rhs_list)//4)]
            else:
                candidates = rhs_list

            # try several candidates to find one occurring in current molecule
            chosen_rhs = None
            chosen_pos = -1
            for _ in range(6):  # try up to 6 candidates per step
                rhs = random.choice(candidates)
                # find all occurrence positions
                positions = []
                start = mol.find(rhs)
                while start != -1:
                    positions.append(start)
                    start = mol.find(rhs, start + 1)
                if positions:
                    chosen_rhs = rhs
                    chosen_pos = random.choice(positions)
                    break

            if chosen_rhs is None:
                # no candidate occurs; break this trial early
                break

            lhs_candidates = reversed_map[chosen_rhs]
            lhs = random.choice(lhs_candidates)
            mol = mol[:chosen_pos] + lhs + mol[chosen_pos + len(chosen_rhs):]
            steps += 1

        if mol == 'e':
            if best is None or steps < best:
                best = steps
        # Optional: early return if you find a solution equal to theoretical lower bound
        # if best == theoretical_minimum: return best

    return best

# print('-- Part 2 Improved --')
# print(f'Test: {greedy_random_reverse_improved(t_molecule.strip(), _parse_mappings_dict(raw_mappings_t), tries=5000, seed=42)}')
# print(f'Data: {greedy_random_reverse_improved(d_molecule.strip(), _parse_mappings_dict(raw_mappings), tries=100000, seed=42)}')