import { Routes, Route } from "react-router-dom";
import Navbar from "./Navbar";
import CreateJob from "./CreateJob";
import Dashboard from "./Dashboard";
import Logger from "./Logger";

const App = () => {
  return (
    <>
        <Navbar />
        <Routes>
          <Route path="/" element={<CreateJob />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path ="/logger" element={<Logger/>}/>
        </Routes>
    </>
  );
};

export default App;
