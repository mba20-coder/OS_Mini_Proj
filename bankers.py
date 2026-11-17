import sys

def leq(a, b):
    return all(x <= y for x, y in zip(a, b))

def is_safe(available, alloc, need):
    work = available[:]
    finish = [False] * len(alloc)
    seq = []
    print("Work:", work)
    found = True
    while found:
        found = False
        for i in range(len(alloc)):
            if not finish[i] and leq(need[i], work):
                work = [w + a for w, a in zip(work, alloc[i])]
                finish[i] = True
                seq.append(f"P{i}")
                found = True
                print(f"P{i} finishes, Work: {work}")
    stuck = [f"P{i}" for i in range(len(alloc)) if not finish[i]]
    return len(stuck) == 0, seq, stuck


state_file = sys.argv[1] if len(sys.argv) > 1 else "state.txt"
req_file = sys.argv[2] if len(sys.argv) > 2 else "requests.txt"

with open(state_file) as f:
    rows = [list(map(int, line.split())) for line in f if line.strip()]
n, m = rows[0]
available = rows[1]
max_m = rows[2:2 + n]
alloc = rows[2 + n:2 + 2 * n]

# B1 - Need matrix
need = [[max_m[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
print("Need Matrix")
print("    " + " ".join(chr(65 + j) for j in range(m)))
for i in range(n):
    print(f"P{i}  " + " ".join(str(x) for x in need[i]))
print()

# B2 - Safety algorithm
safe, seq, stuck = is_safe(available, alloc, need)
if safe:
    print("SAFE <" + ", ".join(seq) + ">")
else:
    print("UNSAFE, could not finish: " + ", ".join(stuck))
print()

# B3 - Resource requests
with open(req_file) as f:
    for line in f:
        parts = line.split()
        if not parts:
            continue
        p = int(parts[0][1:])
        req = list(map(int, parts[1:]))
        print("Request:", line.strip())
        if not leq(req, need[p]):
            print("ERROR")
        elif not leq(req, available):
            print("WAIT")
        else:
            new_avail = [a - r for a, r in zip(available, req)]
            new_alloc = [row[:] for row in alloc]
            new_need = [row[:] for row in need]
            new_alloc[p] = [a + r for a, r in zip(alloc[p], req)]
            new_need[p] = [x - r for x, r in zip(need[p], req)]
            ok, seq, stuck = is_safe(new_avail, new_alloc, new_need)
            if ok:
                print("GRANT <" + ", ".join(seq) + ">")
            else:
                print("DENY (unsafe)")
        print()
