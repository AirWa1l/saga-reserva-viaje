const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const deletedSongs = [];

app.post('/delete', (req, res) => {
  const user = req.body.user;

  if (!user) {
    return res.status(400).json({ error: "El campo 'user' es obligatorio" });
  }


  const deleteRecord = { user, deletedAt: new Date().toISOString() };
  deletedSongs.push(deleteRecord);
  console.log(`Canción eliminada para ${user}`);

  res.status(200).json({
    message: `Canción eliminada para ${user}`,
    status: "deleted",
    data: deleteRecord
  });
});

app.post('/cancel', (req, res) => {
  const user = req.body.user;

  if (!user) {
    return res.status(400).json({ error: "El campo 'user' es obligatorio" });
  }

  const index = deletedSongs.findIndex(r => r.user === user);
  if (index !== -1) {
    deletedSongs.splice(index, 1);
    console.log(`Canción restaurada para ${user}`);
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
