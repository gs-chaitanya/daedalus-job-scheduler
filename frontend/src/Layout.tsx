import React from "react";
import Navbar from "./Navbar";

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-800 text-gray-900 dark:text-white transition-colors">
      <Navbar />
      <main className="p-4">{children}</main>
    </div>
  );
};

export default Layout;
