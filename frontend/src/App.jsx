import { useEffect, useState } from "react";
import "./App.css";
import SoftAurora from "./components/SoftAurora";
import { getTasks, addTask, completeTask, deleteTask } from "./api";

function App() {
  const [tasks, setTasks] = useState([]);
  const [taskText, setTaskText] = useState("");
  const [loading, setLoading] = useState(false);

  async function loadTasks() {
    setLoading(true);

    try {
      const data = await getTasks();
      setTasks(data.tasks || []);
    } catch (error) {
      console.error("Error loading tasks:", error);
      alert("Backend is not running. Start Flask first.");
    }

    setLoading(false);
  }

  async function handleAddTask(event) {
    event.preventDefault();

    if (taskText.trim() === "") {
      alert("Please enter a task");
      return;
    }

    await addTask(taskText);
    setTaskText("");
    loadTasks();
  }

  async function handleComplete(taskId) {
    await completeTask(taskId);
    loadTasks();
  }

  async function handleDelete(taskId) {
    await deleteTask(taskId);
    loadTasks();
  }

  useEffect(() => {
    loadTasks();
  }, []);

  return (
    <div className="app">
      <SoftAurora />

      <main className="todo-card">
        <section className="hero">
          <p className="badge">Flask + SQLite + React</p>
          <h1>Soft Aurora To-Do</h1>
          <p>A simple full-stack task manager with a modern React UI.</p>
        </section>

        <form className="task-form" onSubmit={handleAddTask}>
          <input
            type="text"
            placeholder="Enter a new task..."
            value={taskText}
            onChange={(event) => setTaskText(event.target.value)}
          />
          <button type="submit">Add Task</button>
        </form>

        <section className="tasks-section">
          <div className="section-title">
            <h2>Your Tasks</h2>
            <span>{tasks.length} task(s)</span>
          </div>

          {loading ? (
            <p className="empty-message">Loading tasks...</p>
          ) : tasks.length === 0 ? (
            <p className="empty-message">No tasks found. Add your first task.</p>
          ) : (
            <div className="task-list">
              {tasks.map((task) => (
                <div className="task-item" key={task.id}>
                  <div>
                    <h3 className={task.status === "Completed" ? "done-text" : ""}>
                      {task.task}
                    </h3>

                    <span
                      className={
                        task.status === "Completed"
                          ? "status completed"
                          : "status pending"
                      }
                    >
                      {task.status}
                    </span>
                  </div>

                  <div className="actions">
                    {task.status === "Pending" && (
                      <button
                        className="complete-btn"
                        onClick={() => handleComplete(task.id)}
                      >
                        Done
                      </button>
                    )}

                    <button
                      className="delete-btn"
                      onClick={() => handleDelete(task.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
