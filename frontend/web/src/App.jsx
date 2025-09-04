import { useState } from "react";
import { login, me, register } from "./api";

export default function App() {
  const [mode, setMode] = useState("login"); // "login" | "register"
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [info, setInfo] = useState("");

  const onRegister = async (e) => {
    e.preventDefault();
    try {
      const u = await register({ username, email, password });
      setInfo(`Registered: ${u.username} (${u.email})`);
      setMode("login");
    } catch (e) {
      setInfo(`Error: ${e.message}`);
    }
  };

  const onLogin = async (e) => {
    e.preventDefault();
    try {
      const t = await login({ email, password });
      localStorage.setItem("token", t.access_token);
      setToken(t.access_token);
      setInfo("Logged in!");
    } catch (e) {
      setInfo(`Error: ${e.message}`);
    }
  };

  const onMe = async () => {
    try {
      const u = await me(token);
      setInfo(`Me: ${u.username} (${u.email})`);
    } catch (e) {
      setInfo(`Error: ${e.message}`);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "40px auto", fontFamily: "system-ui, sans-serif" }}>
      <h1>TaskHub — Auth Demo</h1>

      <div style={{ marginBottom: 16 }}>
        <button onClick={() => setMode("login")} disabled={mode === "login"}>
          Login
        </button>
        <button onClick={() => setMode("register")} disabled={mode === "register"} style={{ marginLeft: 8 }}>
          Register
        </button>
      </div>

      {mode === "register" ? (
        <form onSubmit={onRegister}>
          <div>
            <label>Username</label><br />
            <input value={username} onChange={(e) => setUsername(e.target.value)} required />
          </div>
          <div>
            <label>Email</label><br />
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div>
            <label>Password</label><br />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <button type="submit" style={{ marginTop: 12 }}>Create account</button>
        </form>
      ) : (
        <form onSubmit={onLogin}>
          <div>
            <label>Email</label><br />
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div>
            <label>Password</label><br />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>
          <button type="submit" style={{ marginTop: 12 }}>Login</button>
        </form>
      )}

      <hr style={{ margin: "16px 0" }} />

      <div>
        <button onClick={onMe} disabled={!token}>Who am I?</button>
        <button
          onClick={() => {
            localStorage.removeItem("token");
            setToken("");
            setInfo("Logged out");
          }}
          style={{ marginLeft: 8 }}
        >
          Logout
        </button>
      </div>

      <pre style={{ background: "#f6f6f6", padding: 12, marginTop: 16 }}>{info}</pre>
    </div>
  );
}
