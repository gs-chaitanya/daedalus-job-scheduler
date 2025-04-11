import React, { useEffect, useRef, useState } from "react";

const JobLogViewer: React.FC = () => {
  const [logs, setLogs] = useState<string[]>([]);
  const logsEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    let socket: WebSocket | null = null;

    const connectWebSocket = () => {
      socket = new WebSocket("ws://localhost:8888/ws/jobs");

      socket.onopen = () => {
        addLog("Connected to WebSocket server!");
      };

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const formatted = JSON.stringify(data, null, 2);
          addLog(`Received job update:\n${formatted}`);
        } catch (error) {
          addLog(`Error parsing message: ${error}`);
        }
      };

      socket.onerror = (error) => {
        addLog(`WebSocket error: ${error}`);
      };

      socket.onclose = () => {
        addLog("WebSocket connection closed. Reconnecting in 5 seconds...");
        setTimeout(connectWebSocket, 5000);
      };
    };

    const addLog = (log: string) => {
      setLogs((prevLogs) => [...prevLogs, log]);
    };

    connectWebSocket();

    return () => {
      if (socket) {
        socket.close();
      }
    };
  }, []);

  useEffect(() => {
    // Auto-scroll to bottom on new log
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [logs]);

  return (
    <div
      style={{
        backgroundColor: "#1e1e1e",
        color: "#0f0",
        padding: "16px",
        borderRadius: "8px",
        height: "700px",
        overflowY: "auto",
        fontFamily: "monospace",
        fontSize: "16px",
      }}
    >
      {logs.map((log, index) => (
        <pre key={index} style={{ margin: 0, whiteSpace: "pre-wrap" }}>
          {log}
        </pre>
      ))}
      <div ref={logsEndRef} />
    </div>
  );
};

export default JobLogViewer;
