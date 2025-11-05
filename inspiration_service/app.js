const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const inspirations = [];

app.post('/reserve', (req, res) => {
  const user = req.body.user;

  // CREAR INSPIRACIÓN (sin falla aleatoria)
  const inspirationId = `insp_${user}_${inspirations.length + 1}`;
  const inspirationData = {
    user: user,
    inspiration_id: inspirationId,
    status: "inspired", 
    theme: "Amor y aventuras",
    mood: "energético"
  };

  inspirations.push(inspirationData);
  console.log(`✅ Inspiración creada para ${user}: ${inspirationId}`);
  
  res.status(200).json(inspirationData);
});

app.post('/cancel', (req, res) => {
  const user = req.body.user;  
  // Eliminar todas las inspiraciones del usuario
  const initialLength = inspirations.length;
  for (let i = inspirations.length - 1; i >= 0; i--) {
    if (inspirations[i].user === user) {
      inspirations.splice(i, 1);
    }
  }  
  const removedCount = initialLength - inspirations.length;
  console.log(`✅ Inspiración cancelada para ${user}, se eliminaron ${removedCount} inspiraciones`);
  
  res.status(200).json({ 
    message: `Inspiración cancelada para ${user}`,
    removed: removedCount
  });
});

app.get('/inspirations', (req, res) => {
  res.status(200).json(inspirations);
});

app.listen(5008, () => {
  console.log('✨ Inspiration Service ejecutándose en puerto 5008');
});
