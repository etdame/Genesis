<script>
  import { onMount, tick } from 'svelte'
  import { tweened } from 'svelte/motion'
  import { fade } from 'svelte/transition'

  const API = 'http://127.0.0.1:8000'
  let status = 'Connecting…'
  let factors = []
  let formData = {}
  let loading = false, error = ''
  let showScore = false, score = 0, level = 1
  let animated = tweened(0, { duration: 800 })
  let showRecBtn = false
  let rec = null, loadingRec = false, showRec = false
  let resultRef
  $: fmap = new Map(factors.map(f => [f.id, f]))

  onMount(async () => {
    try {
      const p = await fetch(`${API}/ping`)
      status = p.ok ? (await p.json()).status : `Error ${p.status}`
    } catch {
      status = 'Offline'
    }
    try {
      const r = await fetch(`${API}/factors`)
      const j = await r.json()
      factors = j.factors
      factors.forEach(f => {
        formData[f.id] = f.type === 'single-choice' ? f.options[0].id : 0
      })
    } catch {
      error = 'Failed to load questionnaire'
    }
  })

  function toNumeric() {
    return Object.fromEntries(
      Object.entries(formData).map(([k, v]) => {
        const f = fmap.get(k)
        if (f.type === 'single-choice') {
          const o = f.options.find(o => o.id === v)
          return [k, o ? o.value : 0]
        }
        return [k, Number(v)]
      })
    )
  }

  async function handlePredict() {
    loading = true; error = ''; showScore = false; showRec = false; showRecBtn = false; animated.set(0)
    const payload = toNumeric()
    try {
      const r = await fetch(`${API}/score`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!r.ok) throw new Error(`HTTP ${r.status}`)
      const j = await r.json()
      score = j.score; level = j.level
      showScore = true; animated.set(score); await tick()
      resultRef.scrollIntoView({ behavior: 'smooth', block: 'start' })
      showRecBtn = level < 7
    } catch (e) {
      error = e.message
    } finally {
      loading = false
    }
  }

  async function handleRecommend() {
    loadingRec = true; error = ''; showRec = false; rec = null
    const payload = toNumeric()
    try {
      const r = await fetch(`${API}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!r.ok) throw new Error(`HTTP ${r.status}`)
      rec = await r.json(); showRec = !!rec; await tick()
      resultRef.scrollIntoView({ behavior: 'smooth', block: 'start' })
    } catch (e) {
      error = e.message
    } finally {
      loadingRec = false
    }
  }
</script>

<main class="survey-card">
  <div>Server: {status}</div>

  {#if factors.length}
    <form on:submit|preventDefault={handlePredict}>
      {#each factors as f}
        {#if !f.conditional_on || f.conditional_on.options.includes(formData[f.conditional_on.factor])}
          <div class="row">
            <label for={f.id}>{f.description}</label>

            {#if f.type === 'single-choice'}
              <select id={f.id} bind:value={formData[f.id]} class="input">
                {#each f.options as o}
                  <option value={o.id}>{o.label}</option>
                {/each}
              </select>

            {:else if f.type === 'scale'}
              <select id={f.id} bind:value={formData[f.id]} class="input">
                {#each Object.entries(f.labels) as [v, label]}
                  <option value={v / f.scale.max}>{label}</option>
                {/each}
              </select>

            {:else}
              <div class="toggle-group">
                <label class="toggle">
                  <input
                    type="radio"
                    name={f.id}
                    bind:group={formData[f.id]}
                    value="0"
                  />
                  <span>No</span>
                </label>
                <label class="toggle">
                  <input
                    type="radio"
                    name={f.id}
                    bind:group={formData[f.id]}
                    value="1"
                  />
                  <span>Yes</span>
                </label>
              </div>
            {/if}

          </div>
        {/if}
      {/each}

      <div class="button-row">
        <button class="btn" disabled={loading}>
          {loading ? 'Calculating…' : 'Calculate Your Privacy Score'}
        </button>
      </div>
    </form>
  {:else}
    <p>Loading questions…</p>
  {/if}

  {#if error}
    <div class="error">{error}</div>
  {/if}

  {#if showScore}
    <div class="result-card" bind:this={resultRef} in:fade>
      <h2>🔒 Privacy Score</h2>
      <p class="score">{$animated.toFixed(0)}%</p>
      <p>Level: {level}</p>

      {#if showRecBtn}
        <button
          class="btn level-up"
          on:click={handleRecommend}
          disabled={loadingRec}
        >
          {loadingRec ? 'Loading…' : 'Want to level up?'}
        </button>
      {/if}

      {#if showRec}
        <div class="mt-4">
          <h3>💡 Next Tip{rec.factors ? 's' : ''}</h3>
          {#if rec.factors}
            <ul class="list-disc list-inside">
              {#each rec.factors as fid}
                <li>{fmap.get(fid).description}</li>
              {/each}
            </ul>
            <p>Gain ~{rec.delta_score}% total.</p>
          {:else}
            <p>
              Upgrade
              <strong>{fmap.get(rec.factor).description}</strong>
              to gain ~{rec.delta_score}%.
            </p>
          {/if}
        </div>
      {/if}
    </div>
  {/if}
</main>
