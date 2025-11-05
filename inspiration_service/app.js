const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');  // 👈 para llamar al microservicio de lyrics

const app = express();
app.use(bodyParser.json());

const inspirations = [];

app.post('/inspire', async (req, res) => {
  const user = req.body.user;

  // Crear inspiración sencilla y en estilo de las otras apps
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

  // Intentamos avisar al servicio de letras (si está disponible), pero no bloqueamos si falla
  try {
    await axios.post('http://lyrics:5001/write', {
      user: user,
      mood: inspirationData.mood,
      theme: inspirationData.theme,
      lyrics: `Una historia de ${inspirationData.theme.toLowerCase()} llena de energía.`
    });
  } catch (err) {
    console.warn('⚠️ No se pudo notificar a lyrics service:', err.message);
  }

  res.status(200).json({ message: `Inspiración generada para ${user}`, inspiration: inspirationData });
});

app.post('/cancel', (req, res) => {
  const user = req.body.user;

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
