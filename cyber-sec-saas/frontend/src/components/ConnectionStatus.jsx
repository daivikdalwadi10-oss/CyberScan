import React from "react";
import { useSocket } from "../context/SocketProvider";

export default function ConnectionStatus() {
  const { connected } = useSocket();
  return (
    <div style={{ position: "fixed", bottom: 16, right: 16, zIndex: 1000 }}>
      <span
        style={{
          display: "inline-block",
          width: 12,
          height: 12,
          borderRadius: "50%",
          background: connected ? "#4ade80" : "#f87171",
          marginRight: 8,
        }}
      />
      <span style={{ color: connected ? "#4ade80" : "#f87171" }}>
        {connected ? "Connected" : "Disconnected"}
      </span>
    </div>
  );
}
