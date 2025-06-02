<script>
  let message = "Not connected yet";

  async function checkConnection() {
    try {
      const res = await fetch("http://localhost:8000/ping");
      const data = await res.json();
      message = `Server says: ${data.status}`;
    } catch (err) {
      message = "❌ Could not connect to backend";
    }
  }
</script>

<main class="p-4">
  <button
    on:click={checkConnection}
    class="bg-blue-600 text-white px-4 py-2 rounded"
  >
    Check Connection
  </button>

  <p class="mt-4">{message}</p>
</main>
