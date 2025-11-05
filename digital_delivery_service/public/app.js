const playBtn = document.getElementById('playBtn');
const progressEl = document.getElementById('progress');
const deliverBtn = document.getElementById('deliverBtn');
const logs = document.getElementById('logs');

let playing = false;
let progress = 0;
let timer;

function appendLog(text) {
  const li = document.createElement('li');
  li.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
  logs.prepend(li);
}

playBtn.addEventListener('click', () => {
  playing = !playing;
  playBtn.textContent = playing ? '❚❚' : '▶';
  if (playing) {
    timer = setInterval(() => {
      progress = Math.min(100, progress + Math.random() * 6);
      progressEl.style.width = progress + '%';
      if (progress >= 100) { clearInterval(timer); playing = false; playBtn.textContent = '▶'; appendLog('Reproducción finalizada'); progress = 0; progressEl.style.width = '0%'; }
    }, 400);
  } else { clearInterval(timer); }
});

async function deliver() {
  deliverBtn.disabled = true;
  appendLog('Iniciando entrega...');
  try {
    const res = await fetch('/deliver', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ track: 'Canción de Ejemplo', user: 'usuario_demo', format: 'mp3' })
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.message || 'Error desconocido');
    appendLog('Entrega exitosa: ' + json.delivery.track + ' -> ' + json.delivery.user);
  } catch (err) {
    appendLog('Fallo en entrega: ' + err.message);
  } finally {
    deliverBtn.disabled = false;
  }
}

deliverBtn.addEventListener('click', deliver);
