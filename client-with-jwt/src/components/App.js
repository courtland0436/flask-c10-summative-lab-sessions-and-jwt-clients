import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import Login from "../pages/Login";

function App() {
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  
  // State for adding tasks
  const [newTitle, setNewTitle] = useState("");
  const [newDescription, setNewDescription] = useState("");

  // --- ADD STATE FOR EDITING ---
  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");
  // -----------------------------

  useEffect(() => {
    // Auto-login check
    const token = localStorage.getItem("token");
    if (token) {
      fetch("/me", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }).then((r) => {
        if (r.ok) {
          r.json().then((user) => {
            setUser(user);
            fetchTasks();
          });
        } else {
          // If token is invalid, clear it
          localStorage.removeItem("token");
        }
      });
    }
  }, []);

  function fetchTasks() {
    const token = localStorage.getItem("token");
    if (!token) return;

    fetch("/tasks", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }).then((r) => {
      if (r.ok) {
        r.json().then((data) => {
          // Access the tasks array from the paginated response
          if (data && Array.isArray(data.tasks)) {
            setTasks(data.tasks);
          } else {
            console.error("API did not return an array of tasks:", data);
            setTasks([]);
          }
        });
      } else {
        console.error("Failed to fetch tasks, status:", r.status);
      }
    });
  }

  const onLogin = (token, user) => {
    localStorage.setItem("token", token);
    setUser(user);
    fetchTasks();
  }

  function handleSubmitTask(e) {
    e.preventDefault();
    const token = localStorage.getItem("token");
    
    if (!token) {
      console.error("No token found!");
      return;
    }

    fetch("/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      // Send title and description
      body: JSON.stringify({ 
        title: newTitle,
        description: newDescription
      }),
    }).then((r) => {
      if (r.ok) {
        r.json().then((task) => {
          setTasks(Array.isArray(tasks) ? [...tasks, task] : [task]);
          // Clear inputs
          setNewTitle("");
          setNewDescription("");
        });
      } else {
        r.json().then(err => console.error("Server Error:", err));
      }
    });
  }

  function handleDeleteTask(id) {
    const token = localStorage.getItem("token");
    
    fetch(`/tasks/${id}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    }).then((r) => {
      if (r.ok) {
        // Remove task from state
        setTasks(tasks.filter((task) => task.id !== id));
      } else {
        console.error("Failed to delete task");
      }
    });
  }

  // --- ADD EDIT FUNCTION ---
  function handleEditTask(id) {
    const token = localStorage.getItem("token");
    
    fetch(`/tasks/${id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ 
        title: editTitle,
        description: editDescription
      }),
    }).then((r) => {
      if (r.ok) {
        r.json().then((updatedTask) => {
          // Update task in state
          setTasks(tasks.map((task) => task.id === id ? updatedTask : task));
          // Reset edit state
          setEditingId(null);
          setEditTitle("");
          setEditDescription("");
        });
      } else {
        console.error("Failed to edit task");
      }
    });
  }

  function startEditing(task) {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description);
  }
  // -------------------------

  if (!user) return <Login onLogin={onLogin} />;

  // --- STYLING OBJECTS ---
  const sharedCardStyle = {
    border: "1px solid #ddd",
    borderRadius: "8px",
    padding: "20px",
    width: "500px",
    backgroundColor: "#fff",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
    marginBottom: "20px",
    boxSizing: "border-box",
  };

  const inputStyle = { padding: "10px", borderRadius: "4px", border: "1px solid #ccc", marginBottom: "10px" };

  return (
    <>
      <NavBar setUser={setUser} />
      <main style={{ padding: "20px", display: "flex", flexDirection: "column", alignItems: "center", backgroundColor: "#f4f4f4", minHeight: "100vh" }}>
        <h2>Welcome, {user.username}!</h2>
        
        <div style={sharedCardStyle}>
          <h3>Add New Task</h3>
          <form onSubmit={handleSubmitTask} style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <input
              type="text"
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="Task title (required)..."
              style={inputStyle}
              required
            />
            <input
              type="text"
              value={newDescription}
              onChange={(e) => setNewDescription(e.target.value)}
              placeholder="Description..."
              style={inputStyle}
            />
            <button type="submit" style={{ padding: "10px", backgroundColor: "deeppink", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>Add Task</button>
          </form>
        </div>

        <div style={{ width: "500px" }}>
          {Array.isArray(tasks) && tasks.map((task) => (
            <div key={task.id} style={{ ...sharedCardStyle, marginBottom: "15px" }}>
              {editingId === task.id ? (
                // --- EDIT FORM ---
                <div style={{ display: "flex", flexDirection: "column", gap: "5px" }}>
                  <input type="text" value={editTitle} onChange={(e) => setEditTitle(e.target.value)} style={inputStyle} />
                  <input type="text" value={editDescription} onChange={(e) => setEditDescription(e.target.value)} style={inputStyle} />
                  <div style={{ display: "flex", gap: "10px" }}>
                    <button onClick={() => handleEditTask(task.id)} style={{ padding: "5px 10px", backgroundColor: "#4CAF50", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>Save</button>
                    <button onClick={() => setEditingId(null)} style={{ padding: "5px 10px", backgroundColor: "#ccc", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>Cancel</button>
                  </div>
                </div>
              ) : (
                // --- DISPLAY MODE ---
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div>
                    <strong>{task.title}</strong>: {task.description}
                  </div>
                  <div style={{ display: "flex", gap: "5px" }}>
                    <button onClick={() => startEditing(task)} style={{ padding: "5px 10px", backgroundColor: "#2196F3", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>Edit</button>
                    <button onClick={() => handleDeleteTask(task.id)} style={{ padding: "5px 10px", backgroundColor: "#ff4d4d", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>Delete</button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </main>
    </>
  );
}

export default App;