let rainInterval;
let intervalDelay = 50;
let mouseX = window.innerWidth / 2;

function randomText(useEmoji = false) {
  const emoji = ["☔", "⛆", "🌧"];
  const text = "アカサタナハマヤラワ0123456789!@#$%^&*()";
  const set = useEmoji ? emoji : text;
  return set[Math.floor(Math.random() * set.length)];
}

function rain() {
  const container = document.querySelector(".container");
  const drop = document.createElement("div");
  drop.classList.add("drop");

  const useEmoji = document.getElementById("useEmojis").checked;
  drop.innerText = randomText(useEmoji);

  const cloud = document.querySelector(".cloud-svg");
  const cloudRect = cloud.getBoundingClientRect();
  const left = cloudRect.left + Math.random() * cloudRect.width;

  drop.style.left = `${left}px`;

  const fontSize = 14 + Math.random() * 10;
  drop.style.fontSize = `${fontSize}px`;

  const windDrift = document.getElementById("windDrift").checked;
  const bounce = document.getElementById("bounceEffect").checked;

  if (!bounce) {
    drop.style.animation = "fall-straight 2s ease-in forwards";
  }

  container.appendChild(drop);

  // Wind drift tracking
  if (windDrift) {
    const driftStrength = 40;
    const updateDrift = () => {
      const currentX = parseFloat(drop.style.left);
      const diff = mouseX - currentX;
      const sway = (diff / window.innerWidth) * driftStrength;
      drop.style.transform = `translate(${sway}px, 0)`;
    };

    const interval = setInterval(() => {
      if (!document.body.contains(drop)) {
        clearInterval(interval);
      } else {
        updateDrift();
      }
    }, 30);
  }

  setTimeout(() => {
    drop.remove();
  }, 2000);
}

// Mouse tracker for wind drift
window.addEventListener("mousemove", (e) => {
  mouseX = e.clientX;
});

function toggleTooltip() {
  const tip = document.getElementById("tooltip");
  tip.style.display = tip.style.display === "block" ? "none" : "block";
}

function startRain() {
  clearInterval(rainInterval);
  rainInterval = setInterval(rain, intervalDelay);
}

document.getElementById("rainSpeed").addEventListener("input", function () {
  intervalDelay = parseInt(this.value);
  startRain();
});

startRain();
