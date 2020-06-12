from collections import Counter
from math import inf

import requests


def get_times_tabel(id):
    r = requests.get(f"https://mapfw.nl/solutions/progressive/{id}/timestable.csv")
    data = [a.split(",") for a in str(r.content).split("\\n")][1:-1]
    return data


def merge(ids):
    data = [get_times_tabel(id) for id in ids]
    shortest = min(len(x) for x in data)

    times = [[] for x in range(len(data))]

    for x in range(shortest):
        if all(data[n][x][2] for n in range(len(data))):
            for y in range(len(data)):
                times[y].append(int(data[y][x][2]))

    times = [sorted(t) for t in times]

    return times

def cumulative(data):
    cum = []
    for id in range(len(data)):
        cum.append([])
        c = Counter(data[id])
        n = 0
        for x in sorted(list(c)):
            n+=c[x]
            cum[-1].append([x,n])
        print(cum)
    n = [0 for _ in data]
    last = [0 for _ in data]
    out = []
    while any(cum[x] for x in range(len(cum))):
        smallest = inf
        sid = []
        for x in range(len(cum)):
            if cum[x]:
                if cum[x][0][0]<smallest:
                    smallest = cum[x][0][0]
                    sid = [x,]
                if cum[x][0][0]==smallest:
                    sid.append(x)
        out.append([smallest,])
        for x in range(len(cum)):
            if x in sid:
                out[-1].append(cum[x][0][1])
                last[x] = cum[x][0][1]
                cum[x].pop(0)
            else:
                out[-1].append(last[x])

    print(out)
    return out


def to_csv(data, file):
    s = "\n".join(",".join(str(x) for x in r) for r in data)
    with open(file,"w") as f:
        f.write(s)


# get_times_tabel(8738)

# print(merge([8738,8731]))

# to_csv(merge([8738,8731]),"test.csv")
to_csv(cumulative(merge([8737,8596])),"test.csv")