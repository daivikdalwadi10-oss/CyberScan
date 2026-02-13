import { Server } from 'socket.io';
import jwt from 'jsonwebtoken';
import { getMetrics } from '../services/metrics.service.js';
import { getUptime } from '../services/uptime.service.js';
import { getThreats } from '../services/threat.service.js';
import { getAlerts } from '../services/alert.engine.js';

const io = new Server({ cors: { origin: '*' } });

io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  if (!token) return next(new Error('No token'));
  try {
    const user = jwt.verify(token, process.env.SECRET_KEY || 'secret');
    socket.user = user;
    next();
  } catch {
    next(new Error('Invalid token'));
  }
});

function filterDataByRole(role, data) {
  if (role === 'PublicVisitor') return { uptime: data.uptime, system: data.metrics };
  if (role === 'SOCAnalyst') return { alerts: data.alerts, threats: data.threats };
  if (role === 'InfraAdmin') return { metrics: data.metrics, uptime: data.uptime };
  if (role === 'SuperAdmin') return data;
  return {};
}

io.on('connection', async (socket) => {
  const user = socket.user;
  const role = user && user.roles && user.roles[0] ? user.roles[0] : 'PublicVisitor';
  const data = {
    metrics: getMetrics(),
    uptime: getUptime(),
    threats: await getThreats(),
    alerts: getAlerts()
  };
  socket.emit('init', filterDataByRole(role, data));

  // Emit updates
  setInterval(async () => {
    const update = {
      metrics: getMetrics(),
      uptime: getUptime(),
      threats: await getThreats(),
      alerts: getAlerts()
    };
    socket.emit('metricsUpdate', filterDataByRole(role, update));
    socket.emit('alertUpdate', filterDataByRole(role, update));
    socket.emit('uptimeUpdate', filterDataByRole(role, update));
    socket.emit('threatUpdate', filterDataByRole(role, update));
  }, 5000);
});

export function startSocketServer(httpServer) {
  io.attach(httpServer);
}
