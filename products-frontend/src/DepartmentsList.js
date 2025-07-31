import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

function DepartmentsList() {
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/api/departments")
      .then((res) => {
        setDepartments(res.data.departments);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to fetch departments");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h2>Departments</h2>
      <ul>
        {departments.map((dept) => (
          <li key={dept.id}>
            <Link to={`/departments/${dept.id}`}>
              {dept.name} ({dept.product_count})
            </Link>
          </li>
        ))}
      </ul>
      <Link to="/">Back to Products</Link>
    </div>
  );
}

export default DepartmentsList;
