import { useEffect, useMemo, useRef, useState } from "react";
import { getWebSocketUrl } from "../services/websocket.js";
import { useAuth } from "./useAuth.js";

export const useWebSocket = () => {
  const { accessToken } = useAuth();
  const [status, setStatus] = useState("disconnected");
  const [messages, setMessages] = useState([]);
  const socketRef = useRef(null);

  const url = useMemo(() => getWebSocketUrl(accessToken), [accessToken]);

  useEffect(() => {
    if (!accessToken || !url) return undefined;

    const socket = new WebSocket(url);
    socketRef.current = socket;
    setStatus("connecting");

    socket.onopen = () => setStatus("connected");
    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        setMessages((prev) => [payload, ...prev].slice(0, 20));
      } catch (error) {
        setMessages((prev) => [{ type: "raw", payload: event.data }, ...prev].slice(0, 20));
      }
    };
    socket.onerror = () => setStatus("error");
    socket.onclose = () => setStatus("disconnected");

    return () => {
      socket.close();
    };
  }, [accessToken, url]);

  const send = (payload) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(payload));
    }
  };

  return { status, messages, send };
};
