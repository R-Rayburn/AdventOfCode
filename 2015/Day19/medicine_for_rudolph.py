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


def reverse_mapping(m):
    r_map = {}
    for key, values in m.items():
        for v in values:
            r_map[v] = key
    return r_map

import random

def find_mutation_count_randomized(m, molecule):
    r_map = reverse_mapping(m)
    best_steps = float('inf')
    
    # Run many iterations until a valid path to 'e' is found
    while best_steps == float('inf'):
        current_molecule = molecule
        steps = 0
        
        # Keep going until 'e' or a dead end
        while current_molecule != 'e':
            found_match = False
            keys = list(r_map.keys())
            random.shuffle(keys)
            
            for key in keys:
                if key in current_molecule:
                    index = current_molecule.rfind(key)
                    current_molecule = current_molecule[:index] + r_map[key] + current_molecule[index + len(key):]
                    steps += 1
                    found_match = True
                    break

            if not found_match:
                # Dead end reached, break the inner while loop and restart the whole process
                break
        
        # If we successfully reached 'e', update best_steps (will only run once as it's the first time)
        if current_molecule == 'e':
            best_steps = steps
            
    return best_steps

print('Test:', find_mutation_count_randomized(t_mappings, t_molecule))
print('Data:', find_mutation_count_randomized(d_mappings, d_molecule))
