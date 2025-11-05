const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
app.use(bodyParser.json());

const LYRICS_URL = "http://lyrics-service:5001";
const mixes = [];

app.post('/reserve', async (req, res) => {
  const user = req.body.user;
  if (!user) return res.status(400).json({ error: "El campo 'user' es obligatorio" });

  try {
    const response = await axios.get(`${LYRICS_URL}/lyrics`);
    const lyrics = response.data;
    const hasLyrics = lyrics.some(l => l.user === user);

    if (!hasLyrics) {
      return res.status(400).json({ error: `No existe letra para el usuario ${user}` });
    }

    const mix = {
      user: user,
      track: `mix_${user}_${mixes.length + 1}`,
      status: "mixed"
    };
    mixes.push(mix);

    console.log(`🎧 Mezcla creada para ${user}`);
    res.status(200).json({ message: `Mezcla creada para ${user}`, data: mix });

  } catch (err) {
    console.error("Error conectando a Lyrics Service:", err.message);
    res.status(500).json({ error: "No se pudo conectar con el servicio de letras" });
  }
});

app.post('/cancel', async (req, res) => {
  const user = req.body.user;
  if (!user) return res.status(400).json({ error: "El campo 'user' es obligatorio" });

  try {
    const index = mixes.findIndex(m => m.user === user);
    if (index !== -1) {
      mixes.splice(index, 1);
      console.log(`Mezcla eliminada para ${user}`);
    }

    await axios.post(`${LYRICS_URL}/erase`, { user });
    res.status(200).json({ message: `Mezcla y letra eliminadas para ${user}` });
  } catch (err) {
    console.error("Error al cancelar mezcla:", err.message);
    res.status(500).json({ error: "Fallo al cancelar mezcla o eliminar letra" });
  }
});

app.get('/reservas', (req, res) => {
  res.status(200).json(mixes);
});

app.listen(5007, () => {
  console.log('Mixing Service escuchando en puerto 5007');
});
