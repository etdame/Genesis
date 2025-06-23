# Genesis: Your Personal Privacy Journey

> “In six days God created the heavens and the earth, and on the seventh day He rested.”  
> Securing your data takes effort, but once you reach the summit, you may rest in private.

Genesis is a lightweight two-page web app that quantifies your online anonymity, maps it to one of seven intuitive “creation” levels, and recommends the single highest-impact change to help you climb to the next rung most efficiently.

---

## 🚀 Features

- **Interactive Questionnaire**  
  Self-report on nine key privacy factors via single-choice, boolean or scaled inputs.

- **Real-Time Scoring**  
  FastAPI backend computes a weighted sum, normalizes to 0–100, and returns your score & level instantly.

- **Seven Creation Levels**  
  Inspired by the “six days of creation,” levels 1–6 represent incremental improvements; level 7 (“Rest”) signifies best-practice mastery.

- **Next-Level Tip**  
  Sensitivity analysis identifies which factor tweak (or minimal combination) will push you over the next threshold with the least effort.

- **Svelte Frontend**  
  Modern, animated UI built with Svelte, Tailwind-style CSS, and a subtle interactive Matrix-rain background.

---

## 📊 Methodology

1. **Factor Identification & Weights**  
   Nine core factors chosen for impact on anonymity:
   - Network Protection (VPN, DNS)
   - Self-Hosted VPN/Proxy
   - Email Practices
   - Password Hygiene
   - Browser & Metadata Hygiene
   - Open-Source Software Usage
   - OS Telemetry
   - Two-Factor Authentication
   - Encryption at Rest  

   Each factor assigned a weight (summing to 1.0) based on relative privacy impact.

2. **Weighted Sum & Normalization (0–100)**  
   For each factor _i_, let _xᵢ_ ∈ [0,1] be your selected value and _wᵢ_ its weight.  
   **Score** = round( (∑ wᵢ·xᵢ) · 100 ).

3. **Mapping to 7 Levels**  
   | Level | Score Range | Creation Icon        | Interpretation                            |
   |-------|-------------|----------------------|-------------------------------------------|
   | 1     | 0–14        | Genesis              | Critical improvements needed              |
   | 2     | 15–29       | Light                | Basics covered. Many gaps remain          |
   | 3     | 30–44       | Sky & Water          | Basic protections in place; more needed   |
   | 4     | 45–59       | Land & Vegetation    | Solid foundation; tighten settings        |
   | 5     | 60–74       | Stars & Lights       | Strong practices; minor tweaks remain     |
   | 6     | 75–89       | Animals & Humans     | Almost fully protected; few tweaks left   |
   | 7     | 90–100      | Rest                 | Best practices fully met; you may rest    |

4. **Sensitivity Analysis for Top Improvement**  
   - Compute your **gap** to the next threshold.  
   - Brute-force subsets of upgradable factors, “greedily” pouring just enough into the highest-weight factors to cover the gap.  
   - Recommend the subset whose total adjustments are smallest—so you climb with minimal effort.

---

## 🛠️ Tech Stack

- **Frontend**: Svelte + native CSS (utility-inspired, glassmorphic cards, smooth transitions)  
- **Backend**: Python 3.13, FastAPI, Uvicorn  
- **Data**: `factors.json` configuration drives factor weights, options, and conditional logic  
- **Deployment**: Easily containerized or hosted on any Python-friendly platform  

---

## 📦 Getting Started

1. **Clone & install**  
   ```bash
   git clone https://github.com/your-org/genesis.git
   cd genesis
   # Backend
   cd backend && python -m venv venv && source venv/bin/activate
   pip install fastapi uvicorn
   uvicorn main:app --reload
   # Frontend
   cd ../frontend
   npm install
   npm run dev
