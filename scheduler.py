import sys
from collections import deque

sys.stdout = open("output_A.txt", "w")

#Read process.txt
def read_processes(filename):
    procs = []
    with open(filename) as f:
        for line in f:
            parts = line.split()
            if len(parts) == 3:
                procs.append([parts[0], int(parts[1]), int(parts[2])])
    procs.sort(key=lambda p: p[1])
    return procs

#First Come, First Served
def fcfs(procs):
    gantt = []
    time = 0
    for pid, arrival, burst in procs:
        if time < arrival:
            time = arrival
        gantt.append((pid, time, time + burst))
        time += burst
    return gantt

#Shortest Job First
def sjf(procs):
    gantt = []
    time = 0
    left = procs[:]
    while left:
        ready = [p for p in left if p[1] <= time]
        if not ready:
            time = min(p[1] for p in left)
            continue
        p = min(ready, key=lambda x: (x[2], x[1]))
        gantt.append((p[0], time, time + p[2]))
        time += p[2]
        left.remove(p)
    return gantt

#Round Robin
def round_robin(procs, q):
    gantt = []
    time = 0
    remaining = {p[0]: p[2] for p in procs}
    queue = deque()
    i = 0
    n = len(procs)
    while i < n or queue:
        while i < n and procs[i][1] <= time:
            queue.append(procs[i][0])
            i += 1
        if not queue:
            time = procs[i][1]
            continue
        pid = queue.popleft()
        run = min(q, remaining[pid])
        if gantt and gantt[-1][0] == pid:
            gantt[-1] = (pid, gantt[-1][1], time + run)
        else:
            gantt.append((pid, time, time + run))
        time += run
        remaining[pid] -= run
        while i < n and procs[i][1] <= time:
            queue.append(procs[i][0])
            i += 1
        if remaining[pid] > 0:
            queue.append(pid)
    return gantt

#Print Gantt Chart
def print_results(name, procs, gantt):
    print(name)
    print("| " + " | ".join(f"{pid} {s}-{e}" for pid, s, e in gantt) + " |")

    first = {}
    finish = {}
    for pid, s, e in gantt:
        first.setdefault(pid, s)
        finish[pid] = e

    print("PID  Waiting  Turnaround  Response")
    total_w = total_t = total_r = 0
    for pid, arrival, burst in procs:
        tat = finish[pid] - arrival
        wait = tat - burst
        resp = first[pid] - arrival
        total_w += wait
        total_t += tat
        total_r += resp
        print(f"{pid:<5}{wait:<9}{tat:<12}{resp}")

    n = len(procs)
    print(f"Average waiting: {total_w / n:.2f}")
    print(f"Average turnaround: {total_t / n:.2f}")
    print(f"Average response: {total_r / n:.2f}")
    print()


filename = sys.argv[1] if len(sys.argv) > 1 else "processes.txt"
quantum = int(sys.argv[2]) if len(sys.argv) > 2 else 2
procs = read_processes(filename)

print_results("FCFS", procs, fcfs(procs))
print_results("SJF", procs, sjf(procs))
print_results(f"Round Robin (q={quantum})", procs, round_robin(procs, quantum))
