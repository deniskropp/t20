document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('task-input');
    const saveTaskBtn = document.getElementById('save-task-btn');
    const cancelTaskBtn = document.getElementById('cancel-task-btn');
    const addTaskBtn = document.getElementById('add-task-btn');
    const addTaskFromEmptyBtn = document.getElementById('add-task-from-empty-btn');
    const taskInputArea = document.getElementById('task-input-area');
    const taskList = document.getElementById('task-list');
    const emptyState = document.getElementById('empty-state');

    let tasks = [];

    // Load tasks from localStorage
    const loadTasks = () => {
        const storedTasks = localStorage.getItem('tasks');
        tasks = storedTasks ? JSON.parse(storedTasks) : [];
        renderTasks();
    };

    // Save tasks to localStorage
    const saveTasks = () => {
        localStorage.setItem('tasks', JSON.stringify(tasks));
    };

    // Render all tasks
    const renderTasks = () => {
        taskList.innerHTML = ''; // Clear current list
        tasks.forEach(task => {
            const taskElement = createTaskElement(task);
            taskList.appendChild(taskElement);
        });
        updateEmptyState();
    };

    // Create a single task element
    const createTaskElement = (task) => {
        const li = document.createElement('li');
        li.classList.add('task-item');
        if (task.completed) {
            li.classList.add('completed');
        }
        li.setAttribute('data-id', task.id);

        li.innerHTML = `
            <div class="checkbox" role="checkbox" aria-checked="${task.completed}" tabindex="0">
                ${task.completed ? '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>' : ''}
            </div>
            <span class="task-description">${task.text}</span>
            <button class="delete-btn" aria-label="Delete Task">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 12 15 21 6"></polyline><path d="M4 6h16M10 11v6M14 11v6"></path></svg>
            </button>
        `;

        // Add event listeners to the elements within the task item
        const checkbox = li.querySelector('.checkbox');
        const deleteBtn = li.querySelector('.delete-btn');

        checkbox.addEventListener('click', () => toggleTaskCompletion(task.id));
        checkbox.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleTaskCompletion(task.id);
            }
        });

        deleteBtn.addEventListener('click', () => deleteTask(task.id));

        return li;
    };

    // Add a new task
    const addTask = () => {
        const text = taskInput.value.trim();
        if (text) {
            const newTask = {
                id: Date.now(), // Simple unique ID
                text: text,
                completed: false
            };
            tasks.push(newTask);
            saveTasks();
            renderTasks();
            taskInput.value = ''; // Clear input
            hideInputArea();
        }
    };

    // Toggle task completion
    const toggleTaskCompletion = (id) => {
        tasks = tasks.map(task =>
            task.id === id ? { ...task, completed: !task.completed } : task
        );
        saveTasks();
        renderTasks();
    };

    // Delete a task
    const deleteTask = (id) => {
        tasks = tasks.filter(task => task.id !== id);
        saveTasks();
        renderTasks();
    };

    // Show the input area
    const showInputArea = () => {
        taskInputArea.classList.remove('hidden');
        taskInput.focus();
    };

    // Hide the input area
    const hideInputArea = () => {
        taskInputArea.classList.add('hidden');
        taskInput.value = ''; // Clear input
    };

    // Update visibility of empty state
    const updateEmptyState = () => {
        if (tasks.length === 0) {
            emptyState.classList.remove('hidden');
            taskList.classList.add('hidden');
        } else {
            emptyState.classList.add('hidden');
            taskList.classList.remove('hidden');
        }
    };

    // Event Listeners
    addTaskBtn.addEventListener('click', showInputArea);
    addTaskFromEmptyBtn.addEventListener('click', showInputArea);
    saveTaskBtn.addEventListener('click', addTask);
    cancelTaskBtn.addEventListener('click', hideInputArea);

    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTask();
        }
    });

    // Initial load
    loadTasks();
});
