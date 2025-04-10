import { Routes, Route } from "react-router-dom";
import Navbar from "./Navbar";
import CreateJob from "./CreateJob";
import Dashboard from "./Dashboard";

const App = () => {
  return (
    <>
        <Navbar />
        <Routes>
          <Route path="/" element={<CreateJob />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
    </>
  );
};

export default App;
