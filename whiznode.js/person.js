import express from 'express';
import mssql from 'mssql';

const router = express.Router();

// GET all persons
router.get('/', async (req, res) => {
  try {
    const result = await mssql.query`SELECT * FROM Persons`;
    res.status(200).json(result.recordset);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Database query failed' });
  }
});

// POST new person
router.post('/', async (req, res) => {
  const { firstName, lastName } = req.body;
  try {
    const result = await mssql.query`
      INSERT INTO Persons (firstName, lastName)
      OUTPUT INSERTED.*
      VALUES (${firstName}, ${lastName})
    `;
    res.status(201).json(result.recordset[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to insert person' });
  }
});

// GET person by ID
router.get('/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const result = await mssql.query`
      SELECT * FROM Persons WHERE id = ${id}
    `;
    if (result.recordset.length === 0) {
      return res.status(404).json({ error: 'Person not found' });
    }
    res.status(200).json(result.recordset[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Database query failed' });
  }
});

export default router;