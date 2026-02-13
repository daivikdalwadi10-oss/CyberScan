import { getMetrics } from './metrics.service';
import { getUptime } from './uptime.service';

let alerts: any[] = [];

function checkAlerts() {
  const metrics = getMetrics();
  const uptime = getUptime();
  if (!metrics) return;
  // CPU
  if (metrics.cpu > 85) alerts.push({ id: Date.now() + '-cpu', type: 'CPU', severity: 'HIGH', message: 'CPU usage high', timestamp: Date.now() });
  // Memory
  if (metrics.memory.percentage > 90) alerts.push({ id: Date.now() + '-mem', type: 'MEMORY', severity: 'HIGH', message: 'Memory usage high', timestamp: Date.now() });
  // Disk
  if (metrics.disk.percentage > 90) alerts.push({ id: Date.now() + '-disk', type: 'DISK', severity: 'HIGH', message: 'Disk usage high', timestamp: Date.now() });
  // Uptime
  if (uptime.results.some((r: any) => !r.success)) alerts.push({ id: Date.now() + '-uptime', type: 'UPTIME', severity: 'HIGH', message: 'Uptime check failed', timestamp: Date.now() });
  if (alerts.length > 100) alerts = alerts.slice(-100);
}

setInterval(checkAlerts, 5000);

export function getAlerts() {
  return alerts;
}
