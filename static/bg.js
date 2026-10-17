// Sirf animated background — login page ke liye
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const bgCanvas = document.getElementById("bgParticles");

if (!reducedMotion && bgCanvas) {
  const bctx = bgCanvas.getContext("2d");
  let W, H;

  function resizeBg() {
    W = bgCanvas.width = window.innerWidth;
    H = bgCanvas.height = window.innerHeight;
  }
  window.addEventListener("resize", resizeBg);
  resizeBg();

  const N = 70;
  const pts = Array.from({ length: N }, () => ({
    x: Math.random() * W,
    y: Math.random() * H,
    vx: (Math.random() - 0.5) * 0.5,
    vy: (Math.random() - 0.5) * 0.5,
    r: Math.random() * 1.8 + 0.6,
  }));

  const stars = [];

  function spawnStar() {
    stars.push({
      x: W * 0.15 + Math.random() * W * 0.75,
      y: Math.random() * H * 0.3,
      vx: -(5 + Math.random() * 4),
      vy: 2.5 + Math.random() * 2,
      life: 1,
      decay: 0.012 + Math.random() * 0.01,
    });
    setTimeout(spawnStar, 2500 + Math.random() * 3500);
  }
  setTimeout(spawnStar, 1800);

  const mouse = { x: null, y: null };
  window.addEventListener("mousemove", (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;

    document.documentElement.style.setProperty(
      "--mx",
      (e.clientX / window.innerWidth - 0.5) * 2
    );
    document.documentElement.style.setProperty(
      "--my",
      (e.clientY / window.innerHeight - 0.5) * 2
    );
  });
  window.addEventListener("mouseout", () => {
    mouse.x = null;
    mouse.y = null;
  });

  function bgTick() {
    bctx.clearRect(0, 0, W, H);

    for (const p of pts) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;

      bctx.beginPath();
      bctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      bctx.fillStyle = "rgba(167, 139, 250, 0.8)";
      bctx.fill();
    }

    for (let i = 0; i < N; i++) {
      for (let j = i + 1; j < N; j++) {
        const a = pts[i];
        const b = pts[j];
        const d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < 110) {
          bctx.strokeStyle = `rgba(139, 92, 246, ${(1 - d / 110) * 0.35})`;
          bctx.lineWidth = 1;
          bctx.beginPath();
          bctx.moveTo(a.x, a.y);
          bctx.lineTo(b.x, b.y);
          bctx.stroke();
        }
      }
    }

    if (mouse.x !== null) {
      for (const p of pts) {
        const d = Math.hypot(p.x - mouse.x, p.y - mouse.y);
        if (d < 140) {
          bctx.strokeStyle = `rgba(34, 211, 238, ${(1 - d / 140) * 0.5})`;
          bctx.lineWidth = 1;
          bctx.beginPath();
          bctx.moveTo(p.x, p.y);
          bctx.lineTo(mouse.x, mouse.y);
          bctx.stroke();
        }
      }
    }

    for (let i = stars.length - 1; i >= 0; i--) {
      const s = stars[i];
      s.x += s.vx;
      s.y += s.vy;
      s.life -= s.decay;

      if (s.life <= 0 || s.x < -60 || s.y > H + 60) {
        stars.splice(i, 1);
        continue;
      }

      const TAIL = 10;
      const grad = bctx.createLinearGradient(
        s.x, s.y,
        s.x - s.vx * TAIL, s.y - s.vy * TAIL
      );
      grad.addColorStop(0, `rgba(255, 255, 255, ${0.9 * s.life})`);
      grad.addColorStop(1, "rgba(255, 255, 255, 0)");

      bctx.strokeStyle = grad;
      bctx.lineWidth = 2;
      bctx.lineCap = "round";
      bctx.beginPath();
      bctx.moveTo(s.x, s.y);
      bctx.lineTo(s.x - s.vx * TAIL, s.y - s.vy * TAIL);
      bctx.stroke();

      bctx.beginPath();
      bctx.arc(s.x, s.y, 1.6, 0, Math.PI * 2);
      bctx.fillStyle = `rgba(255, 255, 255, ${s.life})`;
      bctx.fill();
    }

    requestAnimationFrame(bgTick);
  }
  bgTick();
}
