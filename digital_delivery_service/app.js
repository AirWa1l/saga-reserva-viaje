const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

const deliveries = []; // { id, track, user, status, timestamp }
let nextId = 1;

// Simular falla aleatoria
function fallaAleatoria(probabilidad = 0.25) {
  return Math.random() < probabilidad;
}

// Endpoint para entregar una canción
app.post('/deliver', async (req, res) => {
  const { track, user, format = 'mp3' } = req.body;
  if (!track || !user) {
    return res.status(400).json({ message: 'track y user son requeridos' });
  }

  if (fallaAleatoria()) {
    // Simular fallo y responder 500
    return res.status(500).json({ message: `Error al entregar la canción ${track} a ${user}` });
  }

  const id = nextId++;
  const delivery = {
    id,
    track,
    user,
    format,
    status: 'delivered',
    timestamp: new Date().toISOString()
  };
  deliveries.push(delivery);

  // Intentar obtener letra desde lyrics_service (no bloqueante)
  const lyricsServiceUrl = process.env.LYRICS_SERVICE_URL || 'http://lyrics-service:5001';
  try {
    // Node 18+ tiene fetch global; si no está disponible en tu entorno, instala 'node-fetch'
    const resp = await fetch(`${lyricsServiceUrl}/lyrics`);
    if (resp.ok) {
      const all = await resp.json();
      // Buscar letra por usuario o por track (si no hay match, usar la primera disponible)
      const found = all.find(l => l.user === user) || all.find(l => l.theme === track) || all[0] || null;
      if (found) {
        delivery.lyrics = found.lyrics || null;
      }
    }
  } catch (err) {
    // No interrumpir la entrega si lyrics service no está disponible
    console.warn('No se pudo contactar lyrics_service:', err && err.message ? err.message : err);
  }

  // Simular trabajo de transformación / permisos (no real)
  res.status(200).json({ message: `Canción entregada: ${track}`, delivery });
});

// Cancelar entrega (simbolico)
app.post('/cancel', (req, res) => {
  const { id } = req.body;
  const idx = deliveries.findIndex(d => d.id === id);
  if (idx === -1) return res.status(404).json({ message: 'Entrega no encontrada' });
  const [removed] = deliveries.splice(idx, 1);
  res.status(200).json({ message: `Entrega cancelada: ${removed.track}`, removed });
});

app.get('/deliveries', (req, res) => {
  res.status(200).json(deliveries);
});

// Health check
app.get('/health', (req, res) => res.status(200).json({ status: 'ok' }));

// Helper: fetch lyrics from lyrics_service with timeout
const LYRICS_SERVICE_URL = process.env.LYRICS_SERVICE_URL || 'http://lyrics-service:5001';
async function fetchLyricsFromService() {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    const resp = await fetch(`${LYRICS_SERVICE_URL}/lyrics`, { signal: controller.signal });
    clearTimeout(timeout);
    if (!resp.ok) return null;
    const data = await resp.json();
    return Array.isArray(data) ? data : null;
  } catch (err) {
    // network error or timeout
    return null;
  }
}

// Proxy endpoint: get all lyrics from lyrics_service
app.get('/lyrics', async (req, res) => {
  const all = await fetchLyricsFromService();
  if (!all) return res.status(503).json({ message: 'lyrics_service no disponible' });
  res.status(200).json(all);
});

// Proxy endpoint: get lyrics for a specific user
app.get('/lyrics/:user', async (req, res) => {
  const user = req.params.user;
  const all = await fetchLyricsFromService();
  if (!all) return res.status(503).json({ message: 'lyrics_service no disponible' });
  const found = all.find(l => l.user === user);
  if (!found) return res.status(404).json({ message: `No se encontraron letras para ${user}` });
  res.status(200).json(found);
});

const PORT = process.env.PORT || 5009;
app.listen(PORT, () => {
  console.log(`Digital Delivery Service listening on port ${PORT}`);
});
