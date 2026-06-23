const API_URL = "http://127.0.0.1:5000/api";

export async function getTasks() {
  const response = await fetch(`${API_URL}/tasks`);
  return response.json();
}

export async function addTask(task) {
  const response = await fetch(`${API_URL}/tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ task }),
  });

  return response.json();
}

export async function completeTask(taskId) {
  const response = await fetch(`${API_URL}/tasks/${taskId}/complete`, {
    method: "PUT",
  });

  return response.json();
}

export async function deleteTask(taskId) {
  const response = await fetch(`${API_URL}/tasks/${taskId}`, {
    method: "DELETE",
  });

  return response.json();
}
