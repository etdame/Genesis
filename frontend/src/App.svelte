<script>
  import Matrix from './components/matrix.svelte';
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
  let resultRef, tipRef;

  let rect;
  function handleMousemove(e) {
    if (!rect) rect = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    document.documentElement.style.setProperty('--mouse-x', `${x}%`);
    document.documentElement.style.setProperty('--mouse-y', `${y}%`);
  }

  $: fmap = new Map(factors.map(f => [f.id, f]));

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

<Matrix />

<main class="survey-card" on:mousemove={handleMousemove}>
  <div>Server: {status}</div>

  {#if factors.length}
    <div class="clouds-container">

      <!-- Section 1: Connectivity & Platform -->
      <div class="cloud">
        <h2>Connectivity & Platform</h2>
        <div class="row">
          <label for="network_protection">
            {fmap.get('network_protection').description}
          </label>
          <select
            id="network_protection"
            bind:value={formData.network_protection}
            class="input"
          >
            {#each fmap.get('network_protection').options as o}
              <option value={o.id}>{o.label}</option>
            {/each}
          </select>
        </div>

        {#if formData.network_protection === 'vpn' ||
              formData.network_protection === 'vpn_adv'}
          <div class="row" in:slide={{ duration: 300 }} out:slide={{ duration: 200 }}>
            <div in:fade={{ duration: 300 }}>
              <label for="self_hosted_vpn">
                {fmap.get('self_hosted_vpn').description}
              </label>
            </div>
            <div class="toggle-group" in:fade={{ duration: 300 }}>
              <label class="toggle">
                <input
                  type="radio"
                  name="self_hosted_vpn"
                  bind:group={formData.self_hosted_vpn}
                  value="0"
                /><span>No</span>
              </label>
              <label class="toggle">
                <input
                  type="radio"
                  name="self_hosted_vpn"
                  bind:group={formData.self_hosted_vpn}
                  value="1"
                /><span>Yes</span>
              </label>
            </div>
          </div>
        {/if}

        <div class="row">
          <label for="os_telemetry">
            {fmap.get('os_telemetry').description}
          </label>
          <select
            id="os_telemetry"
            bind:value={formData.os_telemetry}
            class="input"
          >
            {#each fmap.get('os_telemetry').options as o}
              <option value={o.id}>{o.label}</option>
            {/each}
          </select>
        </div>
      </div>

      <div class="connector"></div>

      <!-- Section 2: Account & Authentication -->
      <div class="cloud">
        <h2>Account & Authentication</h2>
        {#each factors.filter(f =>
          ['password_hygiene', 'two_factor_authentication', 'email_practices']
          .includes(f.id)
        ) as f}
          <div class="row">
            <label for={f.id}>{f.description}</label>
            {#if f.options}
              <select id={f.id} bind:value={formData[f.id]} class="input">
                {#each f.options as o}
                  <option value={o.id}>{o.label}</option>
                {/each}
              </select>
            {:else}
              <select id={f.id} bind:value={formData[f.id]} class="input">
                {#each Object.entries(f.labels) as [v, label]}
                  <option value={v / f.scale.max}>{label}</option>
                {/each}
              </select>
            {/if}
          </div>
        {/each}
      </div>

      <div class="connector"></div>

      <!-- Section 3: Software & Data Hygiene -->
      <div class="cloud">
        <h2>Software & Data Hygiene</h2>
        {#each factors.filter(f =>
          ['browser_metadata_hygiene', 'open_source_usage', 'encryption_at_rest']
          .includes(f.id)
        ) as f}
          <div class="row">
            <label for={f.id}>{f.description}</label>
            <select id={f.id} bind:value={formData[f.id]} class="input">
              {#each f.options as o}
                <option value={o.id}>{o.label}</option>
              {/each}
            </select>
          </div>
        {/each}
      </div>

    </div>

    <div class="button-row">
      <button class="btn" on:click={handlePredict} disabled={loading}>
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
        <h2>🔒 Privacy Score</h2>
        <p class="score">{ $animated.toFixed(0) }%</p>
        <p>Level: {level}</p>
      </div>

      {#if showRecBtn}
        <button class="btn level-up" on:click={handleRecommend} disabled={loadingRec}>
          {loadingRec ? 'Loading…' : 'Want to level up?'}
        </button>
      {/if}

      {#if showRec}
        <div class="mt-4" bind:this={tipRef} in:slide={{ duration: 400 }} out:slide={{ duration: 200 }}>
          <div in:fade={{ duration: 300 }}>
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
                Upgrade <strong>{fmap.get(rec.factor).description}</strong>
                to gain ~{rec.delta_score}%.
              </p>
            {/if}
          </div>
        </div>
      {/if}
    </div>
  {/if}
</main>
