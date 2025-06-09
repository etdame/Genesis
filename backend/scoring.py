import json

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
    total = 0
    breakdown = {}
    for f in factors:
        val = input_data.get(f["id"], 0)
        if f.get("conditional_on") and not input_data.get(f["conditional_on"], 0):
            breakdown[f["id"]] = 0
            continue
        contrib = f["weight"] * val
        total += contrib
        breakdown[f["id"]] = contrib
    score = round(total * 100)
    level = score_to_level(score)
    deltas = []
    for f in factors:
        current = input_data.get(f["id"], 0)
        if current == 0 and not (f.get("conditional_on") and not input_data.get(f["conditional_on"], 0)):
            gain = (1 - current) * f["weight"] * 100
            deltas.append((f["id"], round(gain)))
    deltas.sort(key=lambda x: -x[1])
    next_tip = {"factor": deltas[0][0], "delta": deltas[0][1]} if deltas else None
    return {
        "score": score,
        "level": level,
        "breakdown": breakdown,
        "next_tip": next_tip
    }

def recommend_next_level(input_data):
    result = calculate_score(input_data)
    current_score = result["score"]
    current_level = result["level"]
    if current_level == 7:
        return None
    thresholds = [15,30,45,60,75,90]
    next_threshold = thresholds[current_level-1]
    total_current = sum(result["breakdown"].values())
    candidates = []
    for f in factors:
        fid = f["id"]
        val = input_data.get(fid, 0)
        if f.get("conditional_on") and not input_data.get(f["conditional_on"], 0):
            continue
        if val >= 1:
            continue
        new_total = total_current + f["weight"] * (1 - val)
        new_score = round(new_total * 100)
        if new_score >= next_threshold:
            candidates.append((fid, new_score-current_score))
    if candidates:
        candidates.sort(key=lambda x: x[1])
        return {"factor": candidates[0][0], "delta_score": candidates[0][1]}
    # if none alone reach next level, suggest the single largest gain
    deltas = []
    for f in factors:
        fid = f["id"]
        val = input_data.get(fid, 0)
        if f.get("conditional_on") and not input_data.get(f["conditional_on"], 0):
            continue
        if val >= 1:
            continue
        deltas.append((fid, round(f["weight"] * (1 - val) * 100)))
    if not deltas:
        return None
    deltas.sort(key=lambda x: -x[1])
    return {"factor": deltas[0][0], "delta_score": deltas[0][1]}
