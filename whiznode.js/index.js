import express from 'express';
import dotenv from 'dotenv';
import personRouter from './person.js';
import mssql from 'mssql';
import swaggerUi from 'swagger-ui-express';
import YAML from 'yamljs';

// Load environment variables first
dotenv.config({ path: '.env.development' });

// Initialize Express app
const app = express();
const port = process.env.PORT || 3000;

// Load Swagger document
const swaggerDocument = YAML.load('./openapi.yaml');

// Middleware
app.use(express.json());
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Azure SQL configuration
const dbConfig = {
  server: process.env.AZURE_SQL_SERVER,
  database: process.env.AZURE_SQL_DATABASE,
  port: parseInt(process.env.AZURE_SQL_PORT),
  user: process.env.AZURE_SQL_USER,
  password: process.env.AZURE_SQL_PASSWORD,
  options: {
    encrypt: true, // required for Azure
    trustServerCertificate: false,
  },
};

// Connect to Azure SQL
mssql.connect(dbConfig)
  .then(() => console.log('Database connected successfully.'))
  .catch(err => console.error('DB Connection Error:', err));

// Mount routers
app.use('/persons', personRouter);

// Start server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});