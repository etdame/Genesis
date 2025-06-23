<script>
  import { onMount, tick } from 'svelte';
  import { tweened } from 'svelte/motion';
  import { fade } from 'svelte/transition';

  const API = 'http://127.0.0.1:8000';
  let status = 'Connecting…';
  let factors = [];
  let formData = {};
  let loading = false, error = '';
  let showScore = false, score = 0, level = 1;
  let animated = tweened(0,{duration:800});
  let showRecBtn = false;
  let rec = null, loadingRec = false, showRec = false;
  $: fmap = new Map(factors.map(f=>[f.id,f]));

  onMount(async()=>{
    try{ const p=await fetch(`${API}/ping`); status=p.ok?(await p.json()).status:`Error ${p.status}`; }
    catch{ status='Offline'; }
    try{
      const r=await fetch(`${API}/factors`);
      const j=await r.json();
      factors=j.factors;
      factors.forEach(f=>formData[f.id]=0);
    }catch(e){ error='Failed to load questionnaire'; }
  });

  function toNumeric(){ return Object.fromEntries(Object.entries(formData).map(([k,v])=>[k,Number(v)])); }

  async function handlePredict(){
    loading=true; error=''; showScore=false; showRec=false; showRecBtn=false; animated.set(0);
    const payload=toNumeric();
    try{
      const r=await fetch(`${API}/score`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
      if(!r.ok) throw new Error(`HTTP ${r.status}`);
      const j=await r.json();
      score=j.score; level=j.level;
      showScore=true; animated.set(score); await tick();
      showRecBtn=level<7;
    }catch(e){ error=e.message; }
    finally{ loading=false; }
  }

  async function handleRecommend(){
    loadingRec=true; error=''; showRec=false;
    const payload=toNumeric();
    try{
      const r=await fetch(`${API}/recommend`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
      if(!r.ok) throw new Error(`HTTP ${r.status}`);
      rec=await r.json();
      showRec=!!rec;
    }catch(e){ error=e.message; }
    finally{ loadingRec=false; }
  }
</script>

<main class="max-w-4xl mx-auto p-6">
  <div class="mb-4">Server: {status}</div>
  {#if factors.length}
    <form on:submit|preventDefault={handlePredict} class="space-y-4">
      {#each factors as f}
        {#if !f.conditional_on || f.conditional_on.options.includes(formData[f.conditional_on.factor])}
          <div>
            <label class="block mb-1">{f.description}</label>
            {#if f.type==='single-choice'}
              <select bind:value={formData[f.id]} class="w-full p-2 bg-secondary text-text rounded">
                {#each f.options as o}
                  <option value={o.value}>{o.label}</option>
                {/each}
              </select>
            {:else if f.type==='scale'}
              <select bind:value={formData[f.id]} class="w-full p-2 bg-secondary text-text rounded">
                {#each Array(f.scale.max - f.scale.min +1).fill(0).map((_,i)=>i+f.scale.min) as v}
                  <option value={v/(f.scale.max)}>{f.labels[v]}</option>
                {/each}
              </select>
            {:else if f.type==='boolean'}
              <select bind:value={formData[f.id]} class="w-full p-2 bg-secondary text-text rounded">
                <option value={0}>No</option>
                <option value={1}>Yes</option>
              </select>
            {/if}
          </div>
        {/if}
      {/each}
      <button type="submit" class="mt-4 px-4 py-2 bg-primary text-bg rounded" disabled={loading}>
        {loading?'Calculating…':'Calculate Your Privacy Score'}
      </button>
    </form>
  {:else}
    <p>Loading questions…</p>
  {/if}

  {#if error}
    <div class="mt-4 text-red-500">{error}</div>
  {/if}

  {#if showScore}
    <div class="mt-6 p-4 bg-secondary rounded space-y-2" in:fade>
      <h2 class="text-xl">🔒 Privacy Score</h2>
      <p class="text-4xl font-bold">{$animated.toFixed(0)}%</p>
      <p>Level: {level}</p>
      {#if showRecBtn}
        <button class="mt-2 px-3 py-1 bg-accent text-bg rounded" on:click={handleRecommend} disabled={loadingRec}>
          {loadingRec?'Loading…':'Want to level up?'}
        </button>
      {/if}
      {#if showRec}
        <div class="mt-3">
          <h3 class="font-semibold">💡 Next Tip</h3>
          <p>Enable <strong>{fmap.get(rec.factor).description}</strong> to gain ~{rec.delta_score}% more.</p>
        </div>
      {/if}
    </div>
  {/if}
</main>

<style>
  main { background: var(--tw-color-bg); }
  .secondary { --tw-bg-opacity:1; background-color:rgba(44,47,72,var(--tw-bg-opacity)); }
  .accent    { --tw-bg-opacity:1; background-color:rgba(192,64,47,var(--tw-bg-opacity)); }
  .primary   { --tw-bg-opacity:1; background-color:rgba(242,183,5,var(--tw-bg-opacity)); }
  .text-bg   { color: #12151C; }
</style>
