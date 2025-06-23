<script>
  import Matrix from './components/matrix.svelte';
  import Score from './Score.svelte';
  import Methodology from './pages/Methodology.svelte';
  import { fade } from 'svelte/transition';

  let activeTab = 'score';
  function select(tab) {
    activeTab = tab;
  }
</script>

<Matrix />

<main class="survey-card" in:fade={{ duration: 400 }}>
  <nav class="menu" in:fade={{ delay: 100, duration: 300 }}>
    <button
      class="menu-button {activeTab === 'score' ? 'active' : ''}"
      on:click={() => select('score')}
    >
      Score
    </button>
    <button
      class="menu-button {activeTab === 'methodology' ? 'active' : ''}"
      on:click={() => select('methodology')}
    >
      Methodology
    </button>
  </nav>

  {#if activeTab === 'score'}
    <div in:fade={{ delay: 400, duration: 400 }}>
      <Score />
    </div>
  {:else}
    <div in:fade={{ delay: 400, duration: 400 }}>
      <Methodology />
    </div>
  {/if}
</main>
