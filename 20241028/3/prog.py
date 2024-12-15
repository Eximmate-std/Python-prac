from itertools import product

n = int(input())
sacred_inscriptions = filter(lambda x: x.count('TOR') == 2, map(''.join, product('TOR', repeat=n)))
print(', '.join(sorted(sacred_inscriptions)))
