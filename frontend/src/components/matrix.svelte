<script>
  import { onMount } from 'svelte';

  let canvas;

  onMount(() => {
    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;
    let columns = Math.floor(width / 20);
    const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
    const charArray = characters.split('');
    let drops = Array(columns).fill(1);

    const frameRate = 25;
    let lastFrame = Date.now();

    function draw() {
      // slightly more opaque background so trails fade quicker
      ctx.fillStyle = 'rgba(0,0,0,0.08)';
      ctx.fillRect(0, 0, width, height);
      // lighter, purple-green tint
      ctx.fillStyle = 'rgba(127,90,240,0.6)';
      ctx.font = '18px monospace';
      for (let i = 0; i < drops.length; i++) {
        const text = charArray[Math.floor(Math.random() * charArray.length)];
        ctx.fillText(text, i * 20, drops[i] * 20);
        if (drops[i] * 20 > height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    }

    function loop() {
      const now = Date.now();
      if (now - lastFrame > 1000 / frameRate) {
        draw();
        lastFrame = now;
      }
      requestAnimationFrame(loop);
    }
    loop();

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      columns = Math.floor(width / 20);
      drops = Array(columns).fill(1);
    };

    const isMobile = /Mobi/i.test(navigator.userAgent);
    if (!isMobile) window.addEventListener('resize', handleResize);
    return () => {
      if (!isMobile) window.removeEventListener('resize', handleResize);
    };
  });
</script>

<canvas bind:this={canvas} class="matrix-canvas" />

<style>
  .matrix-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -2;
  }
</style>
