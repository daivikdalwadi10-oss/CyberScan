import si from 'systeminformation';
import os from 'os';

let latestMetrics = null;

async function collectMetrics() {
  const [cpu, mem, disk] = await Promise.all([
    si.currentLoad(),
    si.mem(),
    si.fsSize()
  ]);
  const usedDisk = disk.reduce((acc, d) => acc + d.used, 0);
  const totalDisk = disk.reduce((acc, d) => acc + d.size, 0);
  latestMetrics = {
    cpu: cpu.currentLoad,
    memory: {
      used: mem.active,
      total: mem.total,
      percentage: (mem.active / mem.total) * 100
    },
    disk: {
      used: usedDisk,
      total: totalDisk,
      percentage: (usedDisk / totalDisk) * 100
    },
    uptime: os.uptime(),
    timestamp: Date.now()
  };
}

setInterval(collectMetrics, 5000);
collectMetrics();

export function getMetrics() {
  return latestMetrics;
}
