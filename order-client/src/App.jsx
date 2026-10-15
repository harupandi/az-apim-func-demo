
import { useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_ORDERS_API_URL;
const APIM_KEY = import.meta.env.VITE_ORDERS_API_KEY;

function App() {
  const [clientId, setClientId] = useState("");
  const [product, setProduct] = useState("");
  const [amount, setAmount] = useState(1);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Ocp-Apim-Subscription-Key": APIM_KEY
        },
        body: JSON.stringify({
          clientId,
          product,
          amount: Number(amount),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || `Request failed: ${response.status}`
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Something went wrong while creating the order."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <h1>Order Client</h1>
      <p>Create an order using your Azure Function.</p>

      <form onSubmit={handleSubmit}>
        <label htmlFor="clientId">Client ID</label>
        <input
          id="clientId"
          type="text"
          value={clientId}
          onChange={(e) => setClientId(e.target.value)}
          placeholder="client-123"
          required
        />

        <label htmlFor="product">Product</label>
        <input
          id="product"
          type="text"
          value={product}
          onChange={(e) => setProduct(e.target.value)}
          placeholder="coffee"
          required
        />

        <label htmlFor="amount">Amount</label>
        <input
          id="amount"
          type="number"
          min="1"
          step="1"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Creating order..." : "Create Order"}
        </button>
      </form>

      {error && (
        <section className="error">
          <h2>Request failed</h2>
          <p>{error}</p>
        </section>
      )}

      {result && (
        <section className="success">
          <h2>Order created successfully!</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </section>
      )}
    </main>
  );
}

export default App;
