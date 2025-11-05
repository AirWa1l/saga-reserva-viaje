const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
app.use(bodyParser.json());

const LYRICS_URL = "http://lyrics-service:5001";

const deletedSongs = [];

app.post('/delete', async (req, res) => {
  const user = req.body.user;

  if (!user) {
    return res.status(400).json({ error: "El campo 'user' es obligatorio" });
  }

  try {
    const lyricsRes = await axios.post(`${LYRICS_URL}/erase`, { user });
    console.log(`Letra eliminada para ${user}:`, lyricsRes.data.message);

    const deleteRecord = { user, deletedAt: new Date().toISOString() };
    deletedSongs.push(deleteRecord);
    console.log(`Canción eliminada para ${user}`);

    res.status(200).json({
      message: `Canción y letra eliminadas para ${user}`,
      status: "deleted",
      data: deleteRecord
    });

  } catch (error) {
    console.error(`⚠️ Error al eliminar datos para ${user}:`, error.message);
    res.status(500).json({ 
      message: `Error al eliminar canción o letra para ${user}`,
      error: error.message
    });
  }
});

app.post('/cancel', (req, res) => {
  const user = req.body.user;

  if (!user) {
    return res.status(400).json({ error: "El campo 'user' es obligatorio" });
  }

  const index = deletedSongs.findIndex(r => r.user === user);
  if (index !== -1) {
    deletedSongs.splice(index, 1);
    console.log(` Canción restaurada para ${user}`);
    return res.status(200).json({
      message: `Canción restaurada para ${user}`,
      status: "restored"
    });
  }

  res.status(404).json({ message: "No se encontró canción eliminada para restaurar" });
});


app.get('/deleted', (req, res) => {
  res.status(200).json(deletedSongs);
});


app.get('/health', (req, res) => {
  res.status(200).json({ status: "healthy" });
});

app.listen(5006, () => {
  console.log('Delete Service ejecutándose en puerto 5006');
});
