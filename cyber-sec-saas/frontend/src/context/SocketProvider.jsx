import React, { createContext, useContext, useEffect, useRef, useState } from "react";
import { io } from "socket.io-client";

const SocketContext = createContext(null);

export function useSocket() {
  return useContext(SocketContext);
}

export function SocketProvider({ children, token, role }) {
  const [connected, setConnected] = useState(false);
  const [metrics, setMetrics] = useState(null);
  const [uptime, setUptime] = useState(null);
  const [threats, setThreats] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const socketRef = useRef(null);

  useEffect(() => {
    if (!token) return;
    if (socketRef.current) socketRef.current.disconnect();
    const socketUrl = import.meta.env.VITE_SOCKET_URL;
    const socket = io(socketUrl, {
      auth: { token },
      transports: ["websocket"]
    });
    socketRef.current = socket;
    socket.on("connect", () => setConnected(true));
    socket.on("disconnect", () => setConnected(false));
    socket.on("init", (data) => {
      if (data.metrics) setMetrics(data.metrics);
      if (data.uptime) setUptime(data.uptime);
      if (data.threats) setThreats(data.threats);
      if (data.alerts) setAlerts(data.alerts);
    });
    socket.on("metricsUpdate", (data) => data.metrics && setMetrics(data.metrics));
    socket.on("uptimeUpdate", (data) => data.uptime && setUptime(data.uptime));
    socket.on("threatUpdate", (data) => data.threats && setThreats(data.threats));
    socket.on("alertUpdate", (data) => data.alerts && setAlerts(data.alerts));
    return () => socket.disconnect();
  }, [token, role]);

  return (
    <SocketContext.Provider value={{ socket: socketRef.current, connected, metrics, uptime, threats, alerts }}>
      {children}
    </SocketContext.Provider>
  );
}
