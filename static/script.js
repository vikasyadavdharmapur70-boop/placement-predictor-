// ============================================================
// Placement Predictor — script.js
// 1) Particle network + shooting stars background
// 2) Title letters + typewriter
// 3) 3D tilt card + glare + orbs parallax
// 4) Magnetic button + ripple
// 5) Form logic + neon gauge + confetti
// 6) Custom cursor + AI scan + power bar + glitch reveal
// ============================================================

// Motion kam chahiye to heavy animations skip karo
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const canHover = window.matchMedia("(hover: hover)").matches;

/* ------------------------------------------------------------
   1) PARTICLE NETWORK BACKGROUND + SHOOTING STARS
------------------------------------------------------------ */
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

  const N = 70; // particles ki sankhya
  const pts = Array.from({ length: N }, () => ({
    x: Math.random() * W,
    y: Math.random() * H,
    vx: (Math.random() - 0.5) * 0.5,
    vy: (Math.random() - 0.5) * 0.5,
    r: Math.random() * 1.8 + 0.6,
  }));

  // Shooting stars
  const stars = [];

  function spawnStar() {
    stars.push({
      x: W * 0.15 + Math.random() * W * 0.75,
      y: Math.random() * H * 0.3,
      vx: -(5 + Math.random() * 4), // left-down jhonka
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

    // Orbs ka parallax — background cursor ke saath halka chalta hai
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

    // dots ko move karao aur banao
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

    // paas wale dots ke beech lines
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

    // mouse ke paas wale dots se cyan connection
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

    // shooting stars ko banayein (tail ke saath)
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

      // chamakta hua sir (head)
      bctx.beginPath();
      bctx.arc(s.x, s.y, 1.6, 0, Math.PI * 2);
      bctx.fillStyle = `rgba(255, 255, 255, ${s.life})`;
      bctx.fill();
    }

    requestAnimationFrame(bgTick);
  }
  bgTick();
}

/* ------------------------------------------------------------
   2) TITLE LETTERS + TYPEWRITER
------------------------------------------------------------ */
const title = document.getElementById("mainTitle");

if (!reducedMotion && title) {
  // Har letter ko span me wrap karo — phir ek-ek karke entrance + wave
  const nodes = Array.from(title.childNodes);
  const frag = document.createDocumentFragment();
  let idx = 0;

  for (const node of nodes) {
    for (const ch of Array.from(node.textContent)) {
      if (ch === " ") {
        frag.appendChild(document.createTextNode(" "));
        idx++;
        continue;
      }
      const span = document.createElement("span");
      span.className = "letter";
      span.textContent = ch;
      // pehla delay = entrance, doosra = wave
      span.style.animationDelay = `${idx * 45}ms, ${idx * 110 + 500}ms`;
      frag.appendChild(span);
      idx++;
    }
  }
  title.textContent = "";
  title.appendChild(frag);
}

const tagline = document.getElementById("tagline");

if (!reducedMotion && tagline) {
  // Typewriter effect — text akshar-akshar likhta hai
  const text = tagline.textContent;
  tagline.textContent = "";

  const caret = document.createElement("span");
  caret.className = "caret";
  tagline.appendChild(caret);

  let i = 0;
  const timer = setInterval(() => {
    if (i < text.length) {
      caret.insertAdjacentText("beforebegin", text[i]);
      i++;
    } else {
      clearInterval(timer);
    }
  }, 28);
}

/* ------------------------------------------------------------
   3) 3D TILT CARD + GLARE
------------------------------------------------------------ */
const container = document.querySelector(".container");

if (!reducedMotion && canHover && container) {
  const glare = container.querySelector(".glare");

  container.addEventListener("mousemove", (e) => {
    const r = container.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width;
    const py = (e.clientY - r.top) / r.height;

    container.style.transform = `perspective(900px) rotateX(${(0.5 - py) * 8}deg) rotateY(${(px - 0.5) * 10}deg)`;
    container.classList.add("tilting");

    if (glare) {
      glare.style.setProperty("--gx", px * 100 + "%");
      glare.style.setProperty("--gy", py * 100 + "%");
    }
  });

  container.addEventListener("mouseleave", () => {
    container.style.transform = "";
    container.classList.remove("tilting");
  });
}

/* ------------------------------------------------------------
   4) MAGNETIC BUTTON + RIPPLE
------------------------------------------------------------ */
const btn = document.getElementById("submitBtn");

if (!reducedMotion && canHover && btn) {
  // Button cursor ki taraf halka khichta hai (magnetic)
  btn.addEventListener("mousemove", (e) => {
    const r = btn.getBoundingClientRect();
    const dx = e.clientX - (r.left + r.width / 2);
    const dy = e.clientY - (r.top + r.height / 2);
    btn.style.transform = `translate(${dx * 0.15}px, ${dy * 0.25}px) scale(1.03)`;
  });

  btn.addEventListener("mouseleave", () => {
    btn.style.transform = "";
  });

  // Click par ripple (pani ki lehar) effect
  btn.addEventListener("click", (e) => {
    const r = btn.getBoundingClientRect();
    const d = Math.max(r.width, r.height);

    const ripple = document.createElement("span");
    ripple.className = "ripple";
    ripple.style.width = ripple.style.height = d + "px";
    ripple.style.left = e.clientX - r.left - d / 2 + "px";
    ripple.style.top = e.clientY - r.top - d / 2 + "px";

    btn.appendChild(ripple);
    setTimeout(() => ripple.remove(), 700);
  });
}

/* ------------------------------------------------------------
   5) CONFETTI (placement hua to celebration 🎉)
------------------------------------------------------------ */
const confettiCanvas = document.getElementById("confetti");
const cctx = confettiCanvas ? confettiCanvas.getContext("2d") : null;
let confettiPieces = [];
let confettiRunning = false;

function resizeConfetti() {
  if (!confettiCanvas) return;
  confettiCanvas.width = window.innerWidth;
  confettiCanvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeConfetti);
resizeConfetti();

function fireConfetti() {
  if (reducedMotion || !cctx) return;

  const colors = ["#22d3ee", "#a78bfa", "#f472b6", "#34d399", "#fbbf24", "#ffffff"];
  const W = confettiCanvas.width;
  const H = confettiCanvas.height;

  // Barish — upar se girta hua confetti
  for (let i = 0; i < 90; i++) {
    confettiPieces.push({
      x: Math.random() * W,
      y: -20 - Math.random() * H * 0.3,
      w: 6 + Math.random() * 6,
      h: 8 + Math.random() * 8,
      vx: (Math.random() - 0.5) * 2,
      vy: 2 + Math.random() * 3.5,
      g: 0.04,
      rot: Math.random() * Math.PI,
      vr: (Math.random() - 0.5) * 0.25,
      color: colors[i % colors.length],
    });
  }

  // Center blast — beech se dhamaka 💥
  for (let i = 0; i < 70; i++) {
    confettiPieces.push({
      x: W / 2,
      y: H / 2,
      w: 6 + Math.random() * 6,
      h: 8 + Math.random() * 8,
      vx: (Math.random() - 0.5) * 11,
      vy: -(3 + Math.random() * 7),
      g: 0.13,
      rot: Math.random() * Math.PI,
      vr: (Math.random() - 0.5) * 0.3,
      color: colors[(i + 2) % colors.length],
    });
  }

  if (!confettiRunning) {
    confettiRunning = true;
    requestAnimationFrame(confettiTick);
  }
}

function confettiTick() {
  cctx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
  confettiPieces = confettiPieces.filter((p) => p.y < confettiCanvas.height + 30);

  for (const p of confettiPieces) {
    p.vy += p.g; // gravity
    p.x += p.vx;
    p.y += p.vy;
    p.rot += p.vr;
    cctx.save();
    cctx.translate(p.x, p.y);
    cctx.rotate(p.rot);
    cctx.fillStyle = p.color;
    cctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
    cctx.restore();
  }

  if (confettiPieces.length) {
    requestAnimationFrame(confettiTick);
  } else {
    confettiRunning = false;
    cctx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
  }
}

/* ------------------------------------------------------------
   6) CUSTOM NEON CURSOR (sirf desktop/pointer devices par)
------------------------------------------------------------ */
const cursorDot = document.getElementById("cursorDot");
const cursorRing = document.getElementById("cursorRing");

if (!reducedMotion && canHover && cursorDot && cursorRing) {
  document.body.classList.add("custom-cursor");

  let rx = -100, ry = -100; // ring ka position (thoda late chalta hai)
  let mx = -100, my = -100;

  window.addEventListener("mousemove", (e) => {
    mx = e.clientX;
    my = e.clientY;
    // dot turant cursor par
    cursorDot.style.transform = `translate(${mx}px, ${my}px)`;
  });

  // ring ko dhire-dhire dot ke piche lao (lerp)
  function ringLoop() {
    rx += (mx - rx) * 0.18;
    ry += (my - ry) * 0.18;
    cursorRing.style.transform = `translate(${rx}px, ${ry}px)`;
    requestAnimationFrame(ringLoop);
  }
  ringLoop();

  // interactive element par hover karne par ring badh jaye
  document.addEventListener("mouseover", (e) => {
    const hot = e.target.closest("a, button, input, select, label");
    cursorRing.classList.toggle("hovering", !!hot);
  });
}

/* ------------------------------------------------------------
   7) PROFILE POWER BAR — jitni fields utni energy ⚡
------------------------------------------------------------ */
const chargeFill = document.getElementById("chargeFill");
const chargePct = document.getElementById("chargePct");
const chargeBox = document.querySelector(".charge");
const formEl = document.getElementById("predictForm");

if (chargeFill && formEl) {
  const fieldEls = Array.from(formEl.querySelectorAll("input, select"));
  let wasFull = false;

  function updateCharge() {
    let filled = 0;
    for (const f of fieldEls) {
      const done = f.value !== "" && f.checkValidity();
      if (done) filled++;
      const lbl = f.previousElementSibling;
      if (lbl && lbl.tagName === "LABEL") lbl.classList.toggle("filled", done);
    }

    const pct = Math.round((filled / fieldEls.length) * 100);
    chargeFill.style.width = pct + "%";
    chargePct.textContent = pct + "%";

    // 100% pehli baar — to ek baar flash karo
    const isFull = filled === fieldEls.length;
    if (isFull && !wasFull && chargeBox) {
      chargeBox.classList.remove("full");
      void chargeBox.offsetWidth;
      chargeBox.classList.add("full");
    }
    wasFull = isFull;

    btn && btn.classList.toggle("charged", isFull);
  }

  formEl.addEventListener("input", updateCharge);
  formEl.addEventListener("change", updateCharge);
  updateCharge();
}

/* ------------------------------------------------------------
   8) AI SCAN + HOLOGRAM GLITCH REVEAL (submit ke waqt)
------------------------------------------------------------ */
let scanTimers = [];

function startScan() {
  if (!container || reducedMotion) return;
  stopScan();
  container.classList.add("scanning");

  // Har field ko ek-ek karke scan line ke saath highlight karo
  const fieldEls = Array.from(formEl.querySelectorAll("input, select"));
  fieldEls.forEach((f, i) => {
    scanTimers.push(
      setTimeout(() => {
        f.classList.add("scanned");
        scanTimers.push(setTimeout(() => f.classList.remove("scanned"), 520));
      }, 150 + i * 150)
    );
  });
}

function stopScan() {
  scanTimers.forEach(clearTimeout);
  scanTimers = [];
  if (container) container.classList.remove("scanning");
  if (formEl) {
    formEl.querySelectorAll(".scanned").forEach((f) => f.classList.remove("scanned"));
  }
}

// Result dikhne par hologram glitch reveal (class tab tak rahegi jab tak result dikhe)
function glitchReveal(el) {
  el.classList.remove("glitch-in");
  void el.offsetWidth;
  el.classList.add("glitch-in");
}

/* ------------------------------------------------------------
   9) FORM LOGIC + NEON GAUGE + RESULT ANIMATIONS
------------------------------------------------------------ */
const GAUGE_CIRC = 2 * Math.PI * 52; // r=52 wale circle ki lambai

// % number ko smooth count-up ke saath dikhao
function countUp(el, target) {
  const startTime = performance.now();
  const duration = 1400;

  function frame(now) {
    const t = Math.min((now - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - t, 3); // ease-out
    el.textContent = (target * eased).toFixed(1) + "%";
    if (t < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

// Result box ka pop animation dobara chalao
function replayPop(el) {
  el.style.animation = "none";
  void el.offsetWidth; // reflow trick
  el.style.animation = "";
}

// Form submit hone par ye function chalega
document.getElementById("predictForm").addEventListener("submit", async function (e) {
  e.preventDefault(); // page reload hone se roko

  // Form ki saari values ek object me lo
  const data = {
    tenth_percent: document.getElementById("tenth_percent").value,
    twelfth_percent: document.getElementById("twelfth_percent").value,
    cgpa: document.getElementById("cgpa").value,
    internships: document.getElementById("internships").value,
    projects: document.getElementById("projects").value,
    aptitude_score: document.getElementById("aptitude_score").value,
    communication_score: document.getElementById("communication_score").value,
    work_experience: document.getElementById("work_experience").value,
  };

  const resultBox = document.getElementById("result");
  const errorBox = document.getElementById("error");

  btn.disabled = true;
  btn.innerHTML =
    '<span class="eq" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>Soch rahe hain...';
  resultBox.classList.add("hidden");
  errorBox.classList.add("hidden");

  // AI scan shuru — scan line card par sweep hoti hai
  startScan();

  // Kam se kam 1.6s dikhao taaki scan animation poori chale
  const minThink = new Promise((r) => setTimeout(r, reducedMotion ? 0 : 1600));

  try {
    // Flask app ko data bhejo
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    await minThink;

    if (!response.ok || !result.prediction) {
      throw new Error(result.message || "Kuch galat ho gaya!");
    }

    stopScan();

    // Result box ka rang set karo
    const isPlaced = result.probability >= 50;
    resultBox.classList.remove("placed", "not-placed");
    resultBox.classList.add(isPlaced ? "placed" : "not-placed");
    resultBox.classList.remove("hidden");
    replayPop(resultBox);
    glitchReveal(resultBox);

    // Neon gauge ko animate karo (0% se actual % tak bharti hai)
    const gaugeFill = document.getElementById("gaugeFill");
    gaugeFill.style.strokeDasharray = GAUGE_CIRC;
    gaugeFill.style.strokeDashoffset = GAUGE_CIRC;
    requestAnimationFrame(() =>
      requestAnimationFrame(() => {
        gaugeFill.style.strokeDashoffset =
          GAUGE_CIRC * (1 - result.probability / 100);
      })
    );

    // % number count-up ke saath gauge ke beech me
    countUp(document.getElementById("probText"), result.probability);

    // Message dikhao
    document.getElementById("predictionText").textContent = result.prediction;
    document.getElementById("messageText").textContent = result.message;

    // Placed hua to CONFETTI! 🎉
    if (isPlaced) fireConfetti();
  } catch (err) {
    // Error dikhao
    stopScan();
    await minThink.catch(() => {});
    errorBox.textContent = "❌ " + err.message;
    errorBox.classList.remove("hidden");
  } finally {
    stopScan();
    btn.disabled = false;
    btn.textContent = "Predict Karo 🔮";
  }
});
