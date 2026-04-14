import random
import json

with open('data.json', 'r', encoding='utf-8') as f:
    personas = json.load(f)['personalities']

with open('patterns.json', 'r', encoding='utf-8') as f:
    patterns = json.load(f)['patterns']

def calc_dim_score():
    return random.choice([1,2,3]) + random.choice([1,2,3]) + random.choice([1,2,3])

def score_to_level(s):
    if s <= 5:
        return '低'
    elif s <= 6:
        return '中'
    else:
        return '高'

def get_level_score(u, p):
    if u == p:
        return 3
    levels = ['低', '中', '高']
    diff = abs(levels.index(u) - levels.index(p))
    if diff == 1:
        return 2
    return 1

def simulate(dimensions):
    user_levels = {dim: score_to_level(dimensions[dim]) for dim in dimensions}
    best_score = 0
    best_match = None
    for p in patterns:
        score = sum(get_level_score(user_levels[d], p['dimensions'][d]) for d in dimensions)
        if score > best_score:
            best_score = score
            best_match = p['code']
    return best_match

N = 100000
dims = list(patterns[0]['dimensions'].keys())
counts = {p['code']: 0 for p in patterns}

for _ in range(N):
    dim_scores = {d: calc_dim_score() for d in dims}
    best_code = simulate(dim_scores)
    counts[best_code] += 1

print("=" * 60)
print("New: L(3-5) | M(6) | H(7-9)  N={}".format(N))
print("=" * 60)

sorted_counts = sorted(counts.items(), key=lambda x: -x[1])

for i, (code, cnt) in enumerate(sorted_counts, 1):
    name = next(p['name'] for p in personas if p['code'] == code)
    prob = cnt / N * 100
    bar = '#' * int(prob * 2)
    print("{:2}. {:10} {:6}  {:5.2f}%  {}".format(i, name, cnt, prob, bar))

print("=" * 60)
print("Theory (1/21) = 4.76%")
print("Max: {:.2f}%  Min: {:.2f}%  Ratio: {:.1f}x".format(
    sorted_counts[0][1]/N*100,
    sorted_counts[-1][1]/N*100,
    sorted_counts[0][1]/sorted_counts[-1][1]))