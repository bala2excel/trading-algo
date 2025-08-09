import React, { useEffect, useState } from "react";

const WS_URL = "ws://127.0.0.1:9000/ws/orders";
const API_URL = "http://127.0.0.1:9000";

function App() {
  const [orders, setOrders] = useState([]);
  const [params, setParams] = useState({});
  const [status, setStatus] = useState("stopped");
  const [form, setForm] = useState({});
  const [ws, setWs] = useState(null);

  // Load parameters and status on mount
  useEffect(() => {
    fetch(`${API_URL}/parameters`).then(res => res.json()).then(data => {
      setParams(data);
      setForm(data); // Initialize form with current params
    });
    fetch(`${API_URL}/status`).then(res => res.json()).then(s => setStatus(s.running ? "running" : "stopped"));
    const socket = new WebSocket(WS_URL);
    socket.onmessage = (e) => {
      setOrders(o => [JSON.parse(e.data), ...o]);
    };
    setWs(socket);
    return () => socket.close();
  }, []);

  // Keep form in sync with params if params change
  useEffect(() => {
    setForm(params);
  }, [params]);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const updateParams = () => {
    fetch(`${API_URL}/parameters`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form)
    })
      .then(res => res.json())
      .then(data => {
        setParams(data.config);
        setForm(data.config); // Reset form to updated params
        alert("Parameters updated successfully!");
      });
  };

  const startAlgo = () => {
    fetch(`${API_URL}/start`, { method: "POST" }).then(() => setStatus("running"));
  };
  const stopAlgo = () => {
    fetch(`${API_URL}/stop`, { method: "POST" }).then(() => setStatus("stopped"));
  };

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h2>Control Panel</h2>
      <div style={{ marginBottom: 20 }}>
        <b>Status:</b> <span style={{ color: status === "running" ? "green" : "red" }}>{status}</span>
        <button onClick={startAlgo} disabled={status === "running"} style={{ marginLeft: 10 }}>Start</button>
        <button onClick={stopAlgo} disabled={status === "stopped"} style={{ marginLeft: 10 }}>Stop</button>
      </div>
      <h3>Parameters</h3>
      {Object.keys(params).length === 0 ? (
        <div style={{ color: 'red', marginBottom: 10 }}>No parameters found. Please check backend or config file.</div>
      ) : (
        <>
          <table><tbody>
            {Object.entries(params).map(([k, v]) => (
              <tr key={k}>
                <td>{k}</td>
                <td><input name={k} defaultValue={v} onChange={handleChange} /></td>
              </tr>
            ))}
          </tbody></table>
          <button onClick={updateParams} style={{ marginTop: 10 }}>Update Parameters</button>
        </>
      )}
      <h3>Live Orders</h3>
      <table border="1" cellPadding="5"><thead>
        <tr>
          <th>Order ID</th><th>Symbol</th><th>Qty</th><th>Price</th><th>Time</th><th>Type</th>
        </tr>
      </thead><tbody>
        {orders.map(o => (
          <tr key={o.order_id}>
            <td>{o.order_id}</td>
            <td>{o.symbol}</td>
            <td>{o.quantity}</td>
            <td>{o.market_price}</td>
            <td>{o.timestamp}</td>
            <td>{o.paper_trade ? "Paper" : "Live"}</td>
          </tr>
        ))}
      </tbody></table>
    </div>
  );
}

export default App;
