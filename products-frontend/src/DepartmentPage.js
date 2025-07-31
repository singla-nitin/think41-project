import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

function DepartmentPage() {
  const { deptId } = useParams();
  const [department, setDepartment] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:5000/api/departments/${deptId}/products`)
      .then((res) => {
        setDepartment(res.data.department);
        setProducts(res.data.products);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to fetch department or products");
        setLoading(false);
      });
  }, [deptId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h2>{department}</h2>
      <h4>Products in this department:</h4>
      {products.length === 0 ? (
        <div>No products found in this department.</div>
      ) : (
        <ul>
          {products.map((product) => (
            <li key={product.id}>
              <Link to={`/product/${product.id}`}>{product.name}</Link>
            </li>
          ))}
        </ul>
      )}
      <Link to="/departments">Back to Departments</Link> |{" "}
      <Link to="/">All Products</Link>
    </div>
  );
}

export default DepartmentPage;
