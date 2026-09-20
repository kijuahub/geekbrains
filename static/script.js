document.getElementById('add-task-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const input = this.querySelector('input[name="content"]');

    fetch('/add', { method: 'POST', body: new FormData(this) })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const li = document.createElement('li');
                li.dataset.id = data.id;
                li.className = 'animating-in';
                li.innerHTML = `
                    <div class="task-content">
                        <input type="checkbox" onchange="toggleTask(this, ${data.id})">
                        <span class="task-text">${data.content}</span>
                    </div>
                    <div class="actions">
                        <button type="button" class="btn-delete" onclick="softDeleteTask(this, ${data.id})">Удалить</button>
                    </div>
                `;

                document.getElementById('active-tasks').prepend(li);
                document.getElementById('empty-msg').style.display = 'none';
                input.value = '';
                setTimeout(() => li.classList.remove('animating-in'), 300);
            }
        });
});

function toggleTask(checkbox, taskId) {
    const li = checkbox.closest('li');
    const isChecked = checkbox.checked;
    li.classList.add('animating-out');

    fetch('/toggle/' + taskId, { method: 'POST' })
        .then(res => res.json())
        .then(() => {
            setTimeout(() => {
                li.classList.remove('animating-out');
                if (isChecked) {
                    li.classList.add('completed');
                    document.getElementById('completed-tasks').prepend(li);
                } else {
                    li.classList.remove('completed');
                    document.getElementById('active-tasks').prepend(li);
                }
                li.classList.add('animating-in');
                setTimeout(() => li.classList.remove('animating-in'), 300);
            }, 300);
        });
}

function softDeleteTask(btn, taskId) {
    const li = btn.closest('li');
    li.classList.add('animating-out');

    fetch('/delete/' + taskId, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            setTimeout(() => {
                li.classList.remove('animating-out', 'completed');
                li.innerHTML = `
                    <div class="task-content">
                        <span class="task-text" style="color: var(--text-muted);">${data.content}</span>
                    </div>
                    <div class="actions">
                        <button type="button" class="btn-restore" onclick="restoreTask(this, ${taskId})">Восстановить</button>
                        <button type="button" class="btn-delete" onclick="hardDeleteTask(this, ${taskId})">Навсегда</button>
                    </div>
                `;
                document.getElementById('deleted-tasks').prepend(li);
                li.classList.add('animating-in');
                setTimeout(() => li.classList.remove('animating-in'), 300);
            }, 300);
        });
}

function restoreTask(btn, taskId) {
    const li = btn.closest('li');
    li.classList.add('animating-out');

    fetch('/restore/' + taskId, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            setTimeout(() => {
                li.classList.remove('animating-out');
                li.innerHTML = `
                    <div class="task-content">
                        <input type="checkbox" onchange="toggleTask(this, ${taskId})">
                        <span class="task-text">${data.content}</span>
                    </div>
                    <div class="actions">
                        <button type="button" class="btn-delete" onclick="softDeleteTask(this, ${taskId})">Удалить</button>
                    </div>
                `;
                document.getElementById('active-tasks').prepend(li);
                li.classList.add('animating-in');
                setTimeout(() => li.classList.remove('animating-in'), 300);
            }, 300);
        });
}

function hardDeleteTask(btn, taskId) {
    const li = btn.closest('li');
    li.classList.add('animating-out');

    fetch('/hard_delete/' + taskId, { method: 'POST' })
        .then(() => {
            setTimeout(() => {
                li.remove();
            }, 300);
        });
}