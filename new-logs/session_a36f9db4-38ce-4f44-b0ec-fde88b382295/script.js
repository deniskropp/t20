document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('task-input');
    const addTaskBtn = document.getElementById('add-task-btn');
    const taskList = document.getElementById('task-list');
    const confirmationModal = document.getElementById('confirmation-modal');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');

    let tasks = [];
    let taskToDelete = null;

    // Load tasks from localStorage if available
    const savedTasks = localStorage.getItem('todoTasks');
    if (savedTasks) {
        tasks = JSON.parse(savedTasks);
        renderTasks();
    }

    // --- Event Listeners --- 

    addTaskBtn.addEventListener('click', addTask);
    taskInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            addTask();
        }
    });

    taskList.addEventListener('click', (event) => {
        const target = event.target;
        const taskElement = target.closest('.task-item');
        if (!taskElement) return;

        const taskId = parseInt(taskElement.dataset.id);

        if (target.classList.contains('checkbox')) {
            toggleTaskComplete(taskId);
        } else if (target.classList.contains('delete-btn')) {
            taskToDelete = taskId;
            showConfirmationModal();
        }
    });

    confirmDeleteBtn.addEventListener('click', () => {
        if (taskToDelete !== null) {
            deleteTask(taskToDelete);
            hideConfirmationModal();
            taskToDelete = null;
        }
    });

    cancelDeleteBtn.addEventListener('click', () => {
        hideConfirmationModal();
        taskToDelete = null;
    });

    // Close modal if clicking outside of content
    confirmationModal.addEventListener('click', (event) => {
        if (event.target === confirmationModal) {
            hideConfirmationModal();
            taskToDelete = null;
        }
    });

    // --- Functions ---

    function addTask() {
        const taskText = taskInput.value.trim();
        if (taskText) {
            const newTask = {
                id: Date.now(), // Simple unique ID
                text: taskText,
                completed: false
            };
            tasks.push(newTask);
            taskInput.value = '';
            saveTasks();
            renderTasks();
        }
    }

    function toggleTaskComplete(id) {
        tasks = tasks.map(task => 
            task.id === id ? { ...task, completed: !task.completed } : task
        );
        saveTasks();
        renderTasks();
    }

    function deleteTask(id) {
        tasks = tasks.filter(task => task.id !== id);
        saveTasks();
        renderTasks();
    }

    function saveTasks() {
        localStorage.setItem('todoTasks', JSON.stringify(tasks));
    }

    function renderTasks() {
        taskList.innerHTML = ''; // Clear existing list
        tasks.forEach(task => {
            const listItem = document.createElement('li');
            listItem.classList.add('task-item');
            if (task.completed) {
                listItem.classList.add('completed');
            }
            listItem.dataset.id = task.id;

            listItem.innerHTML = `
                <div class="checkbox ${task.completed ? 'checked' : ''}" role="checkbox" aria-checked="${task.completed}" tabindex="0"></div>
                <span class="task-text">${task.text}</span>
                <button class="delete-btn" aria-label="Delete task">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2"><polyline points="3 6 12 15 21 6"></polyline><path d="M4 6h16l-3.586 7.174a2 2 0 0 1-1.914 1.174h-4.068a2 2 0 0 1-1.914-1.174L7 6z"></path><line x1="10" y1="10" x2="14" y2="14"></line><line x1="14" y1="10" x2="10" y2="14"></line></svg>
                </button>
            `;
            taskList.appendChild(listItem);
        });
    }

    function showConfirmationModal() {
        confirmationModal.style.display = 'flex';
    }

    function hideConfirmationModal() {
        confirmationModal.style.display = 'none';
    }

    // Accessibility: Add focus handling for checkboxes and delete buttons
    taskList.addEventListener('keydown', (event) => {
        const target = event.target;
        const taskElement = target.closest('.task-item');
        if (!taskElement) return;

        const taskId = parseInt(taskElement.dataset.id);

        if (event.key === 'Enter' || event.key === ' ') {
            if (target.classList.contains('checkbox')) {
                event.preventDefault();
                toggleTaskComplete(taskId);
            } else if (target.classList.contains('delete-btn')) {
                event.preventDefault();
                taskToDelete = taskId;
                showConfirmationModal();
            }
        } else if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
            // Basic navigation between checkbox and delete button within a task item
            if (target.classList.contains('checkbox')) {
                event.preventDefault();
                taskElement.querySelector('.delete-btn').focus();
            } else if (target.classList.contains('delete-btn')) {
                event.preventDefault();
                taskElement.querySelector('.checkbox').focus();
            }
        }
    });

    // Initial focus management for accessibility
    taskInput.focus();
});
