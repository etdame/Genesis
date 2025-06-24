<script>
  import { fade, slide } from 'svelte/transition';

  const items = [
    {
      title: 'Factor Identification & Weights',
      description:
        'We selected nine core privacy factors (VPN use, email setup, password hygiene, etc.) and assigned each a weight based on its relative impact on your online anonymity.'
    },
    {
      title: 'Weighted Sum & Normalization',
      description:
        'Each factor’s value is multiplied by its weight, summed up, then normalized to a 0–100 scale to give you a single, easy-to-understand score.'
    },
    {
      title: 'Sensitivity Analysis for Top Improvement',
      description:
        'We compute how much each factor would raise your overall score and recommend the smallest combination of changes that will push you to the next level most efficiently.'
    }
  ];

  const levels = [
    { name: '1. Genesis', desc: 'Critical improvements needed.' },
    { name: '2. Light', desc: 'Basics are covered but many gaps remain.' },
    {
      name: '3. Sky & Water',
      desc: 'Basic protections in place, further enhancements recommended.'
    },
    {
      name: '4. Land & Vegetation',
      desc: 'Solid foundation, consider tightening system and browser settings.'
    },
    {
      name: '5. Stars & Lights',
      desc: 'Strong practices overall, with only minor improvements left.'
    },
    {
      name: '6. Animals & Humans',
      desc: 'Almost fully protected—just a few tweaks remain.'
    },
    { name: '7. Rest', desc: 'Best practices fully met, may you rest in private.' }
  ];

  let index = 0;
  function prev() {
    index = (index + levels.length - 1) % levels.length;
  }
  function next() {
    index = (index + 1) % levels.length;
  }
</script>

<section class="method-container" in:fade={{ duration: 400 }}>
  <h1 class="method-title">Methodology</h1>
  <p class="method-subtitle">How your privacy score is determined</p>

  <!-- Row 1 -->
  <div class="method-row">
    <div class="method-card wide" in:fade={{ delay: 200, duration: 400 }}>
      <h2 class="card-heading">{items[0].title}</h2>
      <p class="card-text">{items[0].description}</p>
    </div>
    <div class="method-card narrow" in:fade={{ delay: 350, duration: 400 }}>
      <h2 class="card-heading">{items[1].title}</h2>
      <p class="card-text">{items[1].description}</p>
    </div>
  </div>

  <!-- Row 2 -->
  <div class="method-row">
    <div class="method-card narrow mapping-card" in:fade={{ delay: 500, duration: 400 }}>
      <h2 class="card-heading">Mapping Scores to 7 Intuitive Levels</h2>
      <div class="mapping-carousel">
        <button class="arrow" on:click={prev}>&larr;</button>
        {#each levels as lvl, i}
          {#if i === index}
            <div class="level-card" in:slide={{ duration: 300 }}>
              <h3>{lvl.name}</h3>
              <p>{lvl.desc}</p>
            </div>
          {/if}
        {/each}
        <button class="arrow" on:click={next}>&rarr;</button>
      </div>
    </div>
    <div class="method-card wide" in:fade={{ delay: 650, duration: 400 }}>
      <h2 class="card-heading">{items[2].title}</h2>
      <p class="card-text">{items[2].description}</p>
    </div>
  </div>
</section>
