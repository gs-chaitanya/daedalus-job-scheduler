import React, { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";

const Navbar: React.FC = () => {
  const [isDark, setIsDark] = useState<boolean>(() => {
    return localStorage.getItem("theme") === "dark" || false;
  });

  const location = useLocation(); // for route highlighting if needed

  useEffect(() => {
    const root = document.documentElement;
    if (isDark) {
      root.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      root.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [isDark]);

  const toggleDarkMode = () => setIsDark((prev) => !prev);

  return (
    <nav className="w-full px-6 py-4 bg-white dark:bg-gray-900 shadow flex justify-between items-center">
      <h1 className="text-xl font-bold text-gray-800 dark:text-white">
        Job Scheduler
      </h1>

      <div className="flex items-center gap-4">
        <Link
          to="/dashboard"
          className={`text-gray-800 dark:text-white hover:underline ${
            location.pathname === "/dashboard" ? "font-semibold" : ""
          }`}
        >
          Dashboard
        </Link>
        <Link
          to="/"
          className={`text-gray-800 dark:text-white hover:underline ${
            location.pathname === "/" ? "font-semibold" : ""
          }`}
        >
          Submit Jobs
        </Link>

        
      </div>
    </nav>
  );
};

export default Navbar;
