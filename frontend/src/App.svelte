<script>
  import Matrix from './components/matrix.svelte';
  import Score from './Score.svelte';
  import Methodology from './pages/Methodology.svelte';

  let activeTab = 'score';

  function select(tab) {
    activeTab = tab;
  }
</script>

<Matrix />

<main class="survey-card">
  <nav class="menu">
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
    <Score />
  {:else}
    <Methodology />
  {/if}
</main>
