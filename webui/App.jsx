import React, { useEffect, useState } from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import ParametersForm from "./ParametersForm";

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
    <div className="container py-4">
      <div className="row mb-4">
        <div className="col">
          <h2 className="mb-3">Trading Algo Control Panel</h2>
          <div className="d-flex align-items-center mb-3">
            <b>Status:</b>
            <span className={`ms-2 fw-bold text-${status === "running" ? "success" : "danger"}`}>{status}</span>
            <button onClick={startAlgo} disabled={status === "running"} className="btn btn-success btn-sm ms-3">Start</button>
            <button onClick={stopAlgo} disabled={status === "stopped"} className="btn btn-danger btn-sm ms-2">Stop</button>
          </div>
        </div>
      </div>
      <div className="row mb-4">
        <div className="col-md-10">
          <h4>Parameters</h4>
          <ParametersForm
            params={params}
            form={form}
            handleChange={handleChange}
            updateParams={updateParams}
          />
        </div>
      </div>
      <div className="row">
        <div className="col-md-10">
          <h4>Live Orders</h4>
          <table className="table table-striped table-bordered table-sm">
            <thead className="table-light">
              <tr>
                <th>Order ID</th><th>Symbol</th><th>Qty</th><th>Price</th><th>Time</th><th>Type</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(o => (
                <tr key={o.order_id}>
                  <td>{o.order_id}</td>
                  <td>{o.symbol}</td>
                  <td>{o.quantity}</td>
                  <td>{o.market_price}</td>
                  <td>{o.timestamp}</td>
                  <td><span className={`badge bg-${o.paper_trade ? "secondary" : "success"}`}>{o.paper_trade ? "Paper" : "Live"}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default App;
