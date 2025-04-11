import React, { useEffect, useState } from "react";
import JobLogViewer from "./joblogsviewer";
type Job = {
  job_id: string;
  start_time: string;
  user_id: string;
  payload: string;
  status: string;
  periodic_flag: boolean;
  period_time: number | null;
  retry_count: number;
  retry_delay: number;
  error_message: string | null;
  duration?: number;
  result?: string;
};

type GanttTask = {
  id: string;
  name: string;
  start: string;
  end: string;
  status: string;
  progress: number;
  dependencies: string[];
};

const Dashboard: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [userId, setUserId] = useState<string>("");
  const [ganttTasks, setGanttTasks] = useState<GanttTask[]>([]);
  const [darkMode, setDarkMode] = useState<boolean>(false);

  // useEffect(() => {
  //   let socket: WebSocket | null = null;
  //   let reconnectAttempts = 0;
  //   let reconnectTimeout: ReturnType<typeof setTimeout> | null = null;
  
  //   // const connectWebSocket = () => {
  //   //   socket = new WebSocket("ws://localhost:8888/ws/jobs");
  
  //   //   socket.onopen = () => {
  //   //     console.log("WebSocket connection established");
  //   //     reconnectAttempts = 0; // Reset on successful connection
  //   //   };
  
  //   //   // socket.onmessage = (message) => {
  //   //   //   try {
  //   //   //     console.log("Job updates received")
  //   //   //     const data = JSON.parse(message.data);
  //   //   //     console.log(data)
  //   //   //     if (!data.job_id) {
  //   //   //       console.warn("Received invalid job update:", data);
  //   //   //       return;
  //   //   //     }
  
  //   //   //     setJobs((prevJobs) => {
  //   //   //       const jobExists = prevJobs.find(
  //   //   //         (job) => job.job_id === data.job_id
  //   //   //       );
  
  //   //   //       if (jobExists) {
  //   //   //         return prevJobs.map((job) =>
  //   //   //           job.job_id === data.job_id ? { ...job, ...data } : job
  //   //   //         );
  //   //   //       } else {
  //   //   //         return [...prevJobs, data];
  //   //   //       }
  //   //   //     });
  //   //   //   } catch (err) {
  //   //   //     console.error("Error parsing WebSocket message:", err);
  //   //   //   }
  //   //   // };
      
  //   //   // socket.onmessage = (message) => {
  //   //   //   try {
  //   //   //     console.log("Job updates received");
  //   //   //     const data = JSON.parse(message.data);
  //   //   //     console.log(data);
  //   //   //     if (!data.job_id) {
  //   //   //       console.warn("Received invalid job update:", data);
  //   //   //       return;
  //   //   //     }
      
  //   //   //     setJobs((prevJobs) => {
  //   //   //       const jobIndex = prevJobs.findIndex((job) => job.job_id === data.job_id);
      
  //   //   //       if (jobIndex !== -1) {
  //   //   //         // Job exists, update it
  //   //   //         const updatedJobs = [...prevJobs];
  //   //   //         updatedJobs[jobIndex] = { ...updatedJobs[jobIndex], ...data };
  //   //   //         return updatedJobs;
  //   //   //       } else {
  //   //   //         // Job does not exist, add it
  //   //   //         return [...prevJobs, data];
  //   //   //       }
  //   //   //     });
  //   //   //   } catch (error) {
  //   //   //     console.error("Error parsing WebSocket message:", error);
  //   //   //   }
  //   //   // };
  //   //   socket.onerror = (err) => {
  //   //     console.error("WebSocket error:", err);
  //   //   };
  
  //   //   socket.onclose = (event) => {
  //   //     console.warn("WebSocket closed:", event);
  //   //     socket = null;
  
  //   //     // Try reconnecting with backoff
  //   //     const delay = Math.min(1000 * 2 ** reconnectAttempts, 30000); // max 30s
  //   //     reconnectTimeout = setTimeout(() => {
  //   //       reconnectAttempts++;
  //   //       connectWebSocket();
  //   //     }, delay);
  //   //   };
  //   // };
  
  //   // connectWebSocket();
  
  //   // return () => {
  //   //   if (socket && socket.readyState === WebSocket.OPEN) {
  //   //     socket.close();
  //   //   }
  //   //   if (reconnectTimeout) {
  //   //     clearTimeout(reconnectTimeout);
  //   //   }
  //   // };
  // }, []);
  

  

  const fetchJobs = async () => {
    try {
      const res = await fetch(`http://localhost:8000/jobs/${userId}`);
      if (!res.ok) throw new Error("Failed to fetch jobs");
      const data = await res.json();
      setJobs(data.jobs);
    } catch (err) {
      console.error("Error fetching jobs:", err);
      alert("Failed to load jobs. Check user ID or server status.");
    }
  };

  return (
    <div className={darkMode ? "dark" : ""}>
      <div className="p-6 min-h-screen bg-white text-black dark:bg-gray-900 dark:text-white transition-colors duration-300">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Job Scheduler Dashboard</h1>
        </div>

        
        <h2 className="text-xl font-semibold mb-2">Job Logs</h2>
        
        <JobLogViewer/>
        {/* <pre className="bg-gray-100 dark:bg-gray-800 p-4 rounded-md overflow-x-auto">
          {JSON.stringify(ganttTasks, null, 2)}
        </pre> */}
      </div>
    </div>
  );
};

export default Dashboard;
