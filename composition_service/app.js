const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const compositions = [];

// Simular falla aleatoria
function fallaAleatoria(probabilidad = 0.2) {
  return Math.random() < probabilidad;
}

app.post('/reserve', (req, res) => {
  const user = req.body.user;

  if (fallaAleatoria()) {
    return res.status(500).json({ error: "Servicio de composición falló aleatoriamente" });
  }

  const compositionId = `comp_${user}_${compositions.length + 1}`;
  const compositionData = {
    user: user,
    composition_id: compositionId,
    status: "composed",
    melody: "Progresión en Do mayor",
    chords: "I-V-vi-IV"
  };

  compositions.push(compositionData);
  console.log(` Composición creada para ${user}: ${compositionId}`);
  
  res.status(200).json(compositionData);
});

app.post('/cancel', (req, res) => {
  const user = req.body.user;  
  // Eliminar todas las composiciones del usuario
  const initialLength = compositions.length;
  for (let i = compositions.length - 1; i >= 0; i--) {
    if (compositions[i].user === user) {
      compositions.splice(i, 1);
    }
  }  
  const removedCount = initialLength - compositions.length;
  console.log(` Composición cancelada para ${user}, se eliminaron ${removedCount} composiciones`);
  
  res.status(200).json({ 
    message: `Composición cancelada para ${user}`,
    removed: removedCount
  });
});

app.get('/compositions', (req, res) => {
  res.status(200).json(compositions);
});

app.listen(5002, () => {
  console.log('Composition Service ejecutándose en puerto 5002');
});