import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import ProductsList from "./ProductsList";
import ProductDetail from "./ProductDetail";
import DepartmentsList from "./DepartmentsList";
import DepartmentPage from "./DepartmentPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ProductsList />} />
        <Route path="/departments" element={<DepartmentsList />} />
        <Route path="/departments/:deptId" element={<DepartmentPage />} />
        <Route path="/product/:id" element={<ProductDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
