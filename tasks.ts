interface Task {
  id: number;
  description: string;
  status: 'pending' | 'in-progress' | 'completed';
}

class TaskManager {
  private tasks: Task[] = [];

  addTask(id: number, description: string): void {
    const newTask: Task = { id, description, status: 'pending' };
    this.tasks.push(newTask);
    console.log(`Task ${id} added: ${description}`);
  }

  removeTask(id: number): void {
    this.tasks = this.tasks.filter(task => task.id !== id);
    console.log(`Task ${id} removed`);
  }

  listTasks(): void {
    console.log('Tasks:');
    this.tasks.forEach(task => {
      console.log(`ID: ${task.id}, Description: ${task.description}, Status: ${task.status}`);
    });
  }

  updateTaskStatus(id: number, status: 'pending' | 'in-progress' | 'completed'): void {
    const task = this.tasks.find(task => task.id === id);
    if (task) {
      task.status = status;
      console.log(`Task ${id} status updated to ${status}`);
    } else {
      console.log(`Task ${id} not found`);
    }
  }
}

// Example usage:
const taskManager = new TaskManager();
taskManager.addTask(1, 'Task 1 description');
taskManager.addTask(2, 'Task 2 description');
taskManager.listTasks();
taskManager.updateTaskStatus(1, 'in-progress');
taskManager.listTasks();
taskManager.removeTask(2);
taskManager.listTasks();
