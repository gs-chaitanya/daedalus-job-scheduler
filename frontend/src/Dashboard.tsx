import React, { useEffect, useState } from "react";

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

  useEffect(() => {
    const tasks: GanttTask[] = jobs.map((job, index) => {
      const endTime = new Date(new Date(job.start_time).getTime() + 5 * 60 * 1000); // 5 mins after start
      return {
        id: job.job_id,
        name: job.payload || `Job ${index + 1}`,
        start: job.start_time,
        end: endTime.toISOString(),
        status: job.status || "pending",
        progress: job.status === "success" ? 100 : job.status === "running" ? 50 : 0,
        dependencies: [],
      };
    });
    setGanttTasks(tasks);
  }, [jobs]);

  const fetchJobs = async () => {
    try {
      const res = await fetch(`http://localhost:8000/jobs/${userId}`);
      if (!res.ok) throw new Error("Failed to fetch jobs");
      const data = await res.json();
      setJobs(data.jobs); // ← your response has a `jobs` array
    } catch (err) {
      console.error("Error fetching job:", err);
      alert("Failed to load job. Check user ID or server status.");
    }
  };

  return (
    <div className={`${darkMode ? "dark" : ""}`}>
      <div className="p-6 min-h-screen bg-white text-black dark:bg-gray-900 dark:text-white transition-colors duration-300">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Job Scheduler Dashboard</h1>
        </div>

        <div className="mb-6 flex gap-4 items-center">
          <input
            type="text"
            placeholder="Enter User ID"
            className="border px-3 py-2 rounded-md w-64 dark:bg-gray-800 dark:border-gray-600"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
          />
          <button
            onClick={fetchJobs}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
          >
            Load Jobs
          </button>
        </div>

        <h2 className="text-xl font-semibold mb-2">Job List</h2>
        <table className="w-full border border-gray-300 mb-6 dark:border-gray-600">
          <thead className="bg-gray-100 dark:bg-gray-800">
            <tr>
              <th className="border px-3 py-2">Job ID</th>
              <th className="border px-3 py-2">Payload</th>
              <th className="border px-3 py-2">Start Time</th>
              <th className="border px-3 py-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {jobs.length > 0 ? (
              jobs.map((job) => (
                <tr key={job.job_id} className="dark:border-gray-700">
                  <td className="border px-3 py-2">{job.job_id}</td>
                  <td className="border px-3 py-2">{job.payload}</td>
                  <td className="border px-3 py-2">
                    {new Date(job.start_time).toLocaleString()}
                  </td>
                  <td
  className={`border px-3 py-2 font-semibold ${
    job.status === "done"
      ? "text-green-600"
      : job.status === "queued"
      ? "text-blue-600"
      : "text-yellow-600"
  }`}
>
  {job.status || "pending"}
</td>

                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={4} className="text-center px-3 py-4 text-gray-500">
                  No jobs loaded. Enter a User ID and click "Load Jobs"
                </td>
              </tr>
            )}
          </tbody>
        </table>

        <h2 className="text-xl font-semibold mb-3">Job Execution Timeline</h2>
        {ganttTasks.length > 0 ? (
          <div className="border p-4 rounded bg-gray-50 dark:bg-gray-800 dark:border-gray-600">
            {/* You can replace this with a real Gantt chart later */}
            <pre className="text-sm text-gray-700 dark:text-gray-300 overflow-x-auto">
              {JSON.stringify(ganttTasks, null, 2)}
            </pre>
          </div>
        ) : (
          <p className="text-gray-500">No Gantt tasks to display.</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
