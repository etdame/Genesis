<!-- src/App.svelte -->
<script>
  import { onMount, tick } from 'svelte';
  import { tweened } from 'svelte/motion';
  import { fade } from 'svelte/transition';

  const API_BASE = 'http://127.0.0.1:8000';

  // UI state
  let serverStatus = 'Connecting…';
  let factors = [];
  let formData = {};
  let loading = false;
  let error = '';
  let showScore = false;
  let score = 0;
  let level = 1;
  let animatedScore = tweened(0, { duration: 800 });
  let showButton = false;
  let loadingRecs = false;
  let showRecs = false;
  let recommendation = null;

  // factor lookup map
  $: factorMap = new Map(factors.map(f => [f.id, f]));

  // on mount: health + fetch factors
  onMount(async () => {
    try {
      const ping = await fetch(`${API_BASE}/ping`);
      serverStatus = ping.ok
        ? (await ping.json()).status
        : `Error ${ping.status}`;
    } catch {
      serverStatus = 'Offline';
    }

    try {
      const res = await fetch(`${API_BASE}/factors`);
      const json = await res.json();
      factors = json.factors;
      // initialize all to 0
      for (const f of factors) formData[f.id] = 0;
    } catch (e) {
      console.error('Could not load factors', e);
      error = 'Failed to load questionnaire';
    }
  });

  // helper to numericify formData
  function toNumericData() {
    return Object.fromEntries(
      Object.entries(formData).map(([k,v]) => [k, Number(v)])
    );
  }

  // calculate score
  async function handlePredict() {
    loading = true;
    error = '';
    showScore = false;
    showButton = false;
    showRecs = false;
    animatedScore.set(0);

    const payload = toNumericData();

    try {
      const res = await fetch(`${API_BASE}/score`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const json = await res.json();
      score = json.score;
      level = json.level;

      showScore = true;
      animatedScore.set(score);
      await tick();

      showButton = (level < 7);
      resultRef.scrollIntoView({ behavior:'smooth', block:'start' });
    } catch (e) {
      console.error(e);
      error = e.message;
    } finally {
      loading = false;
    }
  }

  // get recommendation
  async function handleRecommend() {
    loadingRecs = true;
    error = '';
    showRecs = false;
    recommendation = null;

    const payload = toNumericData();

    try {
      const res = await fetch(`${API_BASE}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      recommendation = await res.json();

      showRecs = !!recommendation;
      await tick();
      resultRef.scrollIntoView({ behavior:'smooth', block:'start' });
    } catch (e) {
      console.error(e);
      error = e.message;
    } finally {
      loadingRecs = false;
    }
  }

  let resultRef;
</script>

<main class="container">
  <div class="mb-4">
    <span class="server-status">Server: {serverStatus}</span>
  </div>

  {#if factors.length}
    <form on:submit|preventDefault={handlePredict}>
      {#each factors as f}
        {#if !f.conditional_on || formData[f.conditional_on]}
          <div class="row">
            <label for={f.id}>{f.description}</label>
            <select
              id={f.id}
              bind:value={formData[f.id]}
              class="input"
            >
              <option value="0">No</option>
              <option value="1">Yes</option>
            </select>
          </div>
        {/if}
      {/each}

      <div class="button-row">
        <button type="submit" class="btn" disabled={loading}>
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
    <div bind:this={resultRef} class="mt-6 space-y-4">
      <div in:fade class="result-card">
        <h2>🔒 Privacy Score</h2>
        <p class="score">{$animatedScore.toFixed(0)}%</p>
        <p class="score">Level: {level}</p>
      </div>

      {#if showButton}
        <button
          class="btn level-up"
          on:click={handleRecommend}
          in:fade
          disabled={loadingRecs}
        >
          {loadingRecs ? 'Loading…' : 'Want to level up?'}
        </button>
      {/if}

      {#if showRecs && recommendation}
        <div class="mt-4 space-y-2" in:fade>
          <h2 class="text-lg font-semibold">💡 Next Tip</h2>
          <p>
            Enable <strong>{factorMap.get(recommendation.factor).description}</strong> to gain
            ~{recommendation.delta_score}% more and reach the next level.
          </p>
        </div>
      {/if}
    </div>
  {/if}
</main>

<style>
  /* leave this empty if importing src/app.css */
</style>
