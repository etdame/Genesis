<script>
  import { onMount, tick } from 'svelte';
  import { tweened } from 'svelte/motion';
  import { fade, slide } from 'svelte/transition';

  const API = 'http://127.0.0.1:8000';
  let status = 'Connecting…';
  let factors = [];
  let formData = {};
  let loading = false, error = '';
  let showScore = false, score = 0, level = 1;
  let animated = tweened(0, { duration: 800 });
  let showRecBtn = false;
  let rec = null, loadingRec = false, showRec = false;
  let resultRef, tipRef, surveyCard;
  let hasPointer = false;

  const levelTitles = {
    1: "Genesis",
    2: "Light",
    3: "Sky & Water",
    4: "Land & Vegetation",
    5: "Stars & Lights",
    6: "Animals & Humans",
    7: "Rest"
  };

  $: rankTitle = levelTitles[level] || "";
  $: fmap = new Map(factors.map(f => [f.id, f]));

  function handleMousemove(e) {
    const rect = surveyCard.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width * 100).toFixed(2) + '%';
    const y = ((e.clientY - rect.top)  / rect.height * 100).toFixed(2) + '%';
    document.documentElement.style.setProperty('--mouse-x', x);
    document.documentElement.style.setProperty('--mouse-y', y);
    if (!hasPointer) hasPointer = true;
  }

  onMount(async () => {
    try {
      const p = await fetch(`${API}/ping`);
      status = p.ok ? (await p.json()).status : `Error ${p.status}`;
    } catch {
      status = 'Offline';
    }
    try {
      const r = await fetch(`${API}/factors`);
      const j = await r.json();
      factors = j.factors;
      factors.forEach(f => {
        formData[f.id] = f.type === 'single-choice' ? f.options[0].id : 0;
      });
    } catch {
      error = 'Failed to load questionnaire';
    }
  });

  function toNumeric() {
    return Object.fromEntries(
      Object.entries(formData).map(([k, v]) => {
        const f = fmap.get(k);
        if (f.type === 'single-choice') {
          const o = f.options.find(o => o.id === v);
          return [k, o ? o.value : 0];
        }
        return [k, Number(v)];
      })
    );
  }

  async function handlePredict() {
    loading = true; error = ''; showScore = false; showRec = false; showRecBtn = false; animated.set(0);
    const payload = toNumeric();
    try {
      const r = await fetch(`${API}/score`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const j = await r.json();
      score = j.score; level = j.level;
      showScore = true; animated.set(score); await tick();
      resultRef.scrollIntoView({ behavior: 'smooth', block: 'center' });
      showRecBtn = level < 7;
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  async function handleRecommend() {
    loadingRec = true; error = ''; showRec = false; rec = null;
    const payload = toNumeric();
    try {
      const r = await fetch(`${API}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      rec = await r.json();
      showRec = true; await tick();
      tipRef.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } catch (e) {
      error = e.message;
    } finally {
      loadingRec = false;
    }
  }
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
  class="survey-card {hasPointer ? 'has-pointer' : ''}"
  bind:this={surveyCard}
  on:mousemove={handleMousemove}
>
  <div>Server: {status}</div>

  {#if factors.length}
    <div class="clouds-container">
      <!-- Section 1 -->
      <div class="cloud" in:fade={{ delay: 200, duration: 400 }}>
        <h2>Connectivity & Platform</h2>
        <div class="row">
          <label>{fmap.get('network_protection').description}</label>
          <select bind:value={formData.network_protection} class="input">
            {#each fmap.get('network_protection').options as o}
              <option value={o.id}>{o.label}</option>
            {/each}
          </select>
        </div>
        {#if formData.network_protection === 'vpn' || formData.network_protection === 'vpn_adv'}
          <div class="row" in:slide={{ duration: 300 }} out:slide={{ duration: 200 }}>
            <label>{fmap.get('self_hosted_vpn').description}</label>
            <div class="toggle-group">
              <label class="toggle">
                <input type="radio" bind:group={formData.self_hosted_vpn} value="0" />
                <span>No</span>
              </label>
              <label class="toggle">
                <input type="radio" bind:group={formData.self_hosted_vpn} value="1" />
                <span>Yes</span>
              </label>
            </div>
          </div>
        {/if}
        <div class="row">
          <label>{fmap.get('os_telemetry').description}</label>
          <select bind:value={formData.os_telemetry} class="input">
            {#each fmap.get('os_telemetry').options as o}
              <option value={o.id}>{o.label}</option>
            {/each}
          </select>
        </div>
      </div>

      <div class="connector" in:fade={{ delay: 350, duration: 300 }} />

      <!-- Section 2 -->
      <div class="cloud" in:fade={{ delay: 400, duration: 400 }}>
        <h2>Account & Authentication</h2>
        {#each factors.filter(f =>
          ['password_hygiene','two_factor_authentication','email_practices'].includes(f.id)
        ) as f}
          <div class="row">
            <label>{f.description}</label>
            {#if f.options}
              <select bind:value={formData[f.id]} class="input">
                {#each f.options as o}
                  <option value={o.id}>{o.label}</option>
                {/each}
              </select>
            {:else}
              <select bind:value={formData[f.id]} class="input">
                {#each Object.entries(f.labels) as [v,label]}
                  <option value={+v / f.scale.max}>{label}</option>
                {/each}
              </select>
            {/if}
          </div>
        {/each}
      </div>

      <div class="connector" in:fade={{ delay: 650, duration: 300 }} />

      <!-- Section 3 -->
      <div class="cloud" in:fade={{ delay: 700, duration: 400 }}>
        <h2>Software & Data Hygiene</h2>
        {#each factors.filter(f =>
          ['browser_metadata_hygiene','open_source_usage','encryption_at_rest'].includes(f.id)
        ) as f}
          <div class="row">
            <label>{f.description}</label>
            <select bind:value={formData[f.id]} class="input">
              {#each f.options as o}
                <option value={o.id}>{o.label}</option>
              {/each}
            </select>
          </div>
        {/each}
      </div>
    </div>

    <div class="button-row">
      <button
        class="btn"
        on:click={handlePredict}
        disabled={loading}
        in:fade={{ delay: 900, duration: 400 }}
      >
        {loading ? 'Calculating…' : 'Calculate Your Privacy Score'}
      </button>
    </div>
  {:else}
    <p>Loading questions…</p>
  {/if}

  {#if error}
    <div class="error">{error}</div>
  {/if}

  {#if showScore}
    <div class="result-card" bind:this={resultRef}>
      <div in:fade={{ duration: 300 }}>
        <h2>Privacy Score</h2>
        <p class="score">{$animated.toFixed(0)}%</p>
        <p class="level">{rankTitle}</p>
      </div>

      {#if showRecBtn}
        <button class="btn level-up" on:click={handleRecommend} disabled={loadingRec}>
          {loadingRec ? 'Loading…' : 'Want to level up?'}
        </button>
      {/if}

      {#if showRec}
        <div class="mt-4" bind:this={tipRef} in:slide={{ duration: 400 }}>
          <div in:fade={{ duration: 300 }}>
            <h3>Next Tip{rec.factors ? 's' : ''}</h3>
            {#if rec.factors}
              <ul class="list-disc list-inside tip-list">
                {#each rec.factors as fid}
                  <li>{fmap.get(fid).description}</li>
                {/each}
              </ul>
              <p>Gain ~{rec.delta_score}% total.</p>
            {:else}
              <p>
                Upgrade <strong>{fmap.get(rec.factor).description}</strong>
                to gain ~{rec.delta_score}%.
              </p>
            {/if}
          </div>
        </div>
      {/if}
    </div>
  {/if}
</div>
