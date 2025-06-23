import json

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
    total = 0
    breakdown = {}
    for f in factors:
        val = input_data.get(f["id"], 0)
        cond = f.get("conditional_on")
        if cond and input_data.get(cond["factor"]) not in cond["options"]:
            breakdown[f["id"]] = 0
            continue
        contrib = f["weight"] * val
        total += contrib
        breakdown[f["id"]] = contrib
    score = round(total * 100)
    level = score_to_level(score)
    deltas = []
    for f in factors:
        cur = input_data.get(f["id"], 0)
        cond = f.get("conditional_on")
        if cur == 0 and not (cond and input_data.get(cond["factor"]) not in cond["options"]):
            gain = (1 - cur) * f["weight"] * 100
            deltas.append((f["id"], round(gain)))
    deltas.sort(key=lambda x: -x[1])
    next_tip = {"factor": deltas[0][0], "delta": deltas[0][1]} if deltas else None
    return {"score": score, "level": level, "breakdown": breakdown, "next_tip": next_tip}

def recommend_next_level(input_data):
    result = calculate_score(input_data)
    cs, cl = result["score"], result["level"]
    if cl == 7: return None
    thresholds = [15,30,45,60,75,90]
    tgt = thresholds[cl-1]
    total_current = sum(result["breakdown"].values())
    # first try minimal single change to cross
    candidates = []
    for f in factors:
        fid = f["id"]
        val = input_data.get(fid, 0)
        cond = f.get("conditional_on")
        if (cond and input_data.get(cond["factor"]) not in cond["options"]) or val >= 1:
            continue
        new_total = total_current + f["weight"]*(1-val)
        new_score = round(new_total*100)
        if new_score >= tgt:
            candidates.append((fid, new_score-cs))
    if candidates:
        candidates.sort(key=lambda x: x[1])
        return {"factor": candidates[0][0], "delta_score": candidates[0][1]}
    # else pick largest available gain
    deltas = []
    for f in factors:
        fid = f["id"]
        val = input_data.get(fid, 0)
        cond = f.get("conditional_on")
        if (cond and input_data.get(cond["factor"]) not in cond["options"]) or val >= 1:
            continue
        deltas.append((fid, round(f["weight"]*(1-val)*100)))
    if not deltas: return None
    deltas.sort(key=lambda x: -x[1])
    return {"factor": deltas[0][0], "delta_score": deltas[0][1]}
