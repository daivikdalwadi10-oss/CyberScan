import express from 'express';
import http from 'http';
import cors from 'cors';
import { getMetrics } from './services/metrics.service.js';
import { getUptime } from './services/uptime.service.js';
import { getThreats } from './services/threat.service.js';
import { getAlerts } from './services/alert.engine.js';
import { startSocketServer } from './websocket/socket.js';

const app = express();
app.use(cors());

app.get('/api/metrics', (req, res) => {
  res.json(getMetrics());
});

app.get('/api/uptime', (req, res) => {
  res.json(getUptime());
});

app.get('/api/threats', async (req, res) => {
  res.json(await getThreats());
});

app.get('/api/alerts', (req, res) => {
  res.json(getAlerts());
});

const server = http.createServer(app);
startSocketServer(server);

const PORT = process.env.PORT || 9000;
server.listen(PORT, () => {
  console.log(`Node backend running on port ${PORT}`);
});
