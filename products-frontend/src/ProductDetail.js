import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:5000/api/products/${id}`)
      .then((res) => {
        setProduct(res.data);
        setLoading(false);
      })
      .catch((err) => {
        setError("Product not found");
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  if (!product) return null;

  return (
    <div>
      <h2>{product.name}</h2>
      <p>
        <strong>Brand:</strong> {product.brand}
      </p>
      <p>
        <strong>Category:</strong> {product.category}
      </p>
      <p>
        <strong>Department:</strong> {product.department}
      </p>
      <p>
        <strong>Retail Price:</strong> {product.retail_price}
      </p>
      <p>
        <strong>Cost:</strong> {product.cost}
      </p>
      <p>
        <strong>SKU:</strong> {product.sku}
      </p>
      <p>
        <strong>Distribution Center ID:</strong>{" "}
        {product.distribution_center_id}
      </p>
      <Link to="/">Back to Products</Link>
    </div>
  );
}

export default ProductDetail;
