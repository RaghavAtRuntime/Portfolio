// App.js
import React, { useState } from "react";
import "./App.css"; // Import the CSS file

const App = () => {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");
  const [error, setError] = useState("");

  const addTask = () => {
    if (newTask.trim() !== "") {
      if (!checkDuplicate(newTask)) {
        setTasks([...tasks, newTask]);
        setNewTask("");
        setError("");
      } else {
        setError("Task already exists!");
        setTimeout(() => {
          setError("");
        }, 2000);
      }
    }
  };

  const removeTask = (index) => {
    const updatedTasks = [...tasks];
    updatedTasks.splice(index, 1);
    setTasks(updatedTasks);
  };
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      addTask();
    }
  };
  const checkDuplicate = (task) => {
    return tasks.includes(task);
  };

  return (
    <div className="AppContainer">
      {" "}
      {/* Update class names */}
      <h1>React To-Do List</h1>
      {error && <div className="Error">{error}</div>}
      <div className="InputContainer">
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Add a new task"
        />
        <button className="TaskButton" onClick={addTask}>
          Add
        </button>
      </div>
      <ul className="TaskList">
        {tasks.map((task, index) => (
          <li className="TaskItem" key={index}>
            {task}
            <button className="TaskButton" onClick={() => removeTask(index)}>
              Done
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default App;
