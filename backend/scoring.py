import json
import itertools

with open("factors.json") as f:
    factors = json.load(f)["factors"]

def score_to_level(score):
    if score < 15:
        return 1
    if score < 30:
        return 2
    if score < 45:
        return 3
    if score < 60:
        return 4
    if score < 75:
        return 5
    if score < 90:
        return 6
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
        if f["type"] == "single-choice":
            contrib = raw
        else:
            contrib = raw * f["weight"]
        total += contrib
        breakdown[f["id"]] = contrib
    score = round(total * 100)
    level = score_to_level(score)
    deltas = []
    for f in factors:
        cur = input_data.get(f["id"], 0)
        cond = f.get("conditional_on")
        if cur == 0 and not (cond and input_data.get(cond["factor"], 0) == 0):
            if f["type"] == "single-choice":
                gain = (1 - cur) * 100
            else:
                gain = (1 - cur) * f["weight"] * 100
            deltas.append((f["id"], round(gain)))
    deltas.sort(key=lambda x: -x[1])
    next_tip = {"factor": deltas[0][0], "delta": deltas[0][1]} if deltas else None
    return {"score": score, "level": level, "breakdown": breakdown, "next_tip": next_tip}

def recommend_next_level(input_data):
    result = calculate_score(input_data)
    current_score = result["score"]
    current_level = result["level"]
    if current_level >= 7:
        return None
    pct_thresholds = [15, 30, 45, 60, 75, 90]
    next_thresh = pct_thresholds[current_level - 1] / 100.0
    gap = next_thresh - (current_score / 100.0)
    if gap <= 0:
        return None
    x, w, feats = {}, {}, []
    for f in factors:
        fid = f["id"]
        val = input_data.get(fid, 0.0)
        cond = f.get("conditional_on")
        if cond and input_data.get(cond["factor"], 0) == 0:
            continue
        if val >= 1.0:
            continue
        feats.append(f)
        x[fid] = val
        w[fid] = f["weight"]
    def greedy_within_subset(subset):
        rem = gap
        deltas = {fid: 0.0 for fid in subset}
        for fid in sorted(subset, key=lambda i: w[i], reverse=True):
            avail = 1.0 - x[fid]
            if avail <= 0:
                continue
            need = rem / w[fid]
            adj = min(avail, need)
            deltas[fid] = adj
            rem -= w[fid] * adj
            if rem <= 1e-8:
                break
        return (sum(deltas.values()), deltas) if rem <= 1e-8 else (None, None)
    best_total, best_deltas = None, None
    ids = [f["id"] for f in feats]
    for r in range(1, len(ids) + 1):
        for subset in itertools.combinations(ids, r):
            total, deltas = greedy_within_subset(subset)
            if total is not None and (best_total is None or total < best_total):
                best_total, best_deltas = total, deltas
    if best_deltas:
        added_score = sum(w[fid] * d for fid, d in best_deltas.items())
        return {
            "factors": list(best_deltas.keys()),
            "deltas": best_deltas,
            "delta_score": round(added_score * 100)
        }
    single = []
    for f in feats:
        fid = f["id"]
        gain = round(f["weight"] * (1.0 - x[fid]) * 100)
        single.append((fid, gain))
    if not single:
        return None
    single.sort(key=lambda x: -x[1])
    fid, gain = single[0]
    return {"factor": fid, "delta_score": gain}
