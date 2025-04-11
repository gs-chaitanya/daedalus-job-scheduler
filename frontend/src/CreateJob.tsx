import { useState } from "react";
import { v4 as uuidv4 } from "uuid";

interface JobFormData {
  job_id: string;
  start_time: string;
  payload: string;
  status: string;
  periodic_flag: boolean;
  period_time: number;
  retry_count: number;
  retry_delay: number;
  error_message: string;
  user_id: string;
}

const CreateJob = () => {
  const [formData, setFormData] = useState<JobFormData>({
    job_id: uuidv4(),
    start_time: new Date().toISOString().slice(0, 16),
    payload: "",
    status: "",
    periodic_flag: false,
    period_time: 0,
    retry_count: 0,
    retry_delay: 0,
    error_message: "",
    user_id: "",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;
  
    setFormData((prev) => ({
      ...prev,
      [name]:
        type === "checkbox"
          ? checked
          : ["period_time", "retry_count", "retry_delay"].includes(name)
          ? Number(value)
          : value,
    }));
  };
  

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/jobs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        alert("Job submitted successfully!");
      } else {
        alert("Failed to submit job.");
      }
    } catch (err) {
      alert("Error submitting job.");
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 flex items-center justify-center p-4">
      <form
        onSubmit={handleSubmit}
        className="backdrop-blur-xl bg-white/20 dark:bg-gray-900/40 shadow-2xl rounded-3xl px-8 py-10 w-full max-w-2xl space-y-6 border border-white/30 transition-all duration-300"
      >
        <h1 className="text-4xl font-bold text-white text-center mb-6 tracking-tight">
          Create Your Job
        </h1>

        {/* Grid layout for inputs */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label className="text-white text-sm mb-1 block">User ID</label>
            <input
              name="user_id"
              value={formData.user_id}
              onChange={handleChange}
              className="w-full p-3 rounded-xl bg-white/20 text-white border border-white/30 placeholder-white/70 focus:ring-2 focus:ring-white outline-none"
              placeholder="Enter User ID"
              required
            />
          </div>

          {/* <div>
            <label className="text-white text-sm mb-1 block">Status</label>
            <input
              name="status"
              value={formData.status}
              onChange={handleChange}
              className="w-full p-3 rounded-xl bg-white/20 text-white border border-white/30 placeholder-white/70 focus:ring-2 focus:ring-white outline-none"
              placeholder="Job Status"
              required
            />
          </div> */}

          <div>
            <label className="text-white text-sm mb-1 block">Start Time</label>
            <input
              type="datetime-local"
              name="start_time"
              value={formData.start_time}
              onChange={handleChange}
              className="w-full p-3 rounded-xl bg-white/20 text-white border border-white/30 focus:ring-2 focus:ring-white outline-none"
              required
            />
          </div>

          <div className="flex items-center mt-2 sm:mt-0 space-x-3">
            <input
              type="checkbox"
              name="periodic_flag"
              checked={formData.periodic_flag}
              onChange={handleChange}
              className="accent-pink-500 scale-125"
            />
            <label className="text-white text-sm">Periodic Job?</label>
          </div>

          <div>
            <label className="text-white text-sm mb-1 block">Period Time (min)</label>
            <input
              type="number"
              name="period_time"
              value={formData.period_time}
              onChange={handleChange}
              className="w-full p-3 rounded-xl bg-white/20 text-white border border-white/30 focus:ring-2 focus:ring-white outline-none"
            />
          </div>

          <div>
            <label className="text-white text-sm mb-1 block">Retry Count</label>
            <input
              type="number"
              name="retry_count"
              value={formData.retry_count}
              onChange={handleChange}
              className="w-full p-3 rounded-xl bg-white/20 text-white border border-white/30 focus:ring-2 focus:ring-white outline-none"
            />
          </div>

          <div>
            <label className="text-white text-sm mb-1 block">Retry Delay (sec)</label>
            <input
              type="number"
              name="retry_delay"
              value={formData.retry_delay}
              onChange={handleChange}
              className="w-full p-3 rounded-xl bg-white/20 text-white border border-white/30 focus:ring-2 focus:ring-white outline-none"
            />
          </div>
        </div>

        <div>
          <label className="text-white text-sm mb-1 block">Payload</label>
          <textarea
            name="payload"
            value={formData.payload}
            onChange={handleChange}
            rows={4}
            className="w-full p-3 rounded-xl bg-white/20 text-white border border-white/30 placeholder-white/70 focus:ring-2 focus:ring-white outline-none"
            placeholder="Enter job payload..."
            required
          />
        </div>

        {/* <div>
          <label className="text-white text-sm mb-1 block">Error Message</label>
          <textarea
            name="error_message"
            value={formData.error_message}
            onChange={handleChange}
            rows={3}
            className="w-full p-3 rounded-xl bg-white/20 text-white border border-white/30 placeholder-white/70 focus:ring-2 focus:ring-white outline-none"
            placeholder="Optional error details..."
          />
        </div> */}

        <button
          type="submit"
          className="w-full bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 text-white text-lg font-semibold py-3 rounded-xl shadow-lg transition duration-300 ease-in-out transform hover:scale-105"
        >
           Submit Job
        </button>
      </form>
    </div>
  );
};

export default CreateJob;
