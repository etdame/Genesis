import json
import itertools
from bisect import bisect_right

with open("factors.json") as f:
    factors = json.load(f)["factors"]

def score_to_level(score):
    if score < 15: return 1
    if score < 30: return 2
    if score < 45: return 3
    if score < 60: return 4
    if score < 75: return 5
    if score < 90: return 6
    return 7

def calculate_score(input_data):
    total = 0.0
    breakdown = {}
    for f in factors:
        raw = input_data.get(f["id"], 0)
        cond = f.get("conditional_on")
        if cond and input_data.get(cond["factor"], 0) == 0:
            breakdown[f["id"]] = 0
            continue
        contrib = raw if f["type"]=="single-choice" else raw * f["weight"]
        total += contrib
        breakdown[f["id"]] = contrib
    score = round(total * 100)
    level = score_to_level(score)
    return {"score": score, "level": level, "breakdown": breakdown}

def recommend_next_level(input_data):
    result = calculate_score(input_data)
    cs = result["score"] / 100.0
    cl = result["level"]
    if cl >= 7: return None

    thresholds = [15,30,45,60,75,90]
    thresh = thresholds[cl-1] / 100.0
    gap = thresh - cs
    if gap <= 0: return None

    avail = {}
    for f in factors:
        fid = f["id"]
        val = input_data.get(fid, 0.0)
        cond = f.get("conditional_on")
        if cond and input_data.get(cond["factor"], 0) == 0:
            continue
        if f["type"] == "single-choice":
            vals = sorted(o["value"] for o in f["options"])
            pos = bisect_right(vals, val)
            if pos >= len(vals): continue
            step = vals[pos] - val
            gain = step
        else:
            if val >= 1.0: continue
            step = 1.0 - val
            gain = f["weight"] * step
        avail[fid] = (step, gain)

    # single-feature
    singles = [(step, fid, gain) for fid,(step,gain) in avail.items() if gain >= gap]
    if singles:
        step,fid,gain = min(singles, key=lambda x: x[0])
        return {"factor": fid, "delta_score": round(gain*100)}

    # two-feature combinations
    best = None
    for a,b in itertools.combinations(avail, 2):
        sa,ga = avail[a]
        sb,gb = avail[b]
        tot_gain = ga+gb
        if tot_gain < gap: continue
        tot_step = sa+sb
        if best is None or tot_step < best[0]:
            best = (tot_step, (a,b), (sa,sb), tot_gain)
    if best:
        _, (f1,f2), (s1,s2), g = best
        return {
            "factors": [f1,f2],
            "deltas": {f1: s1, f2: s2},
            "delta_score": round(g*100)
        }

    # fallback: largest single
    fid,(step,gain) = max(avail.items(), key=lambda kv: kv[1][1])
    return {"factor": fid, "delta_score": round(gain*100)}
