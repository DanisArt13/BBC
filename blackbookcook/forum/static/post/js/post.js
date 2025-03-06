document.querySelectorAll('.toggle-comments').forEach(button => {
        button.addEventListener('click', function() {
            const commentsList = this.nextElementSibling;
            const addCommentForm = commentsList.nextElementSibling;

            if (commentsList.style.display === 'none') {
                commentsList.style.display = 'block';
                addCommentForm.style.display = 'block';
                this.textContent = 'Скрыть комментарии';
            } else {
                commentsList.style.display = 'none';
                addCommentForm.style.display = 'none';
                this.textContent = 'Показать комментарии';
            }
        });
    });

    document.querySelectorAll('.comment-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Предотвращаем стандартное поведение формы

            const formData = new FormData(this); // Собираем данные из формы

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Указываем, что запрос AJAX
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Создаем новый элемент списка для комментария
                    const newComment = document.createElement('li');
                    newComment.className = 'comment-item';
                    newComment.innerHTML = `<strong>${data.author}:</strong> ${data.content} <br><small>Дата: ${data.created_at}</small>`;
                    // Добавляем новый комментарий в список
                    const commentsList = this.parentElement.previousElementSibling; // Список комментариев
                    commentsList.appendChild(newComment);
                    // Очищаем текстовое поле
                    this.querySelector('textarea').value = '';
                }
            })
            .catch(error => console.error('Ошибка:', error));
        });
    });
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.querySelector('.toggle-comments');
    const commentsList = document.querySelector('.comments-list');
    const addCommentForm = document.querySelector('.add-comment-form');

    toggleButton.addEventListener('click', function() {
        // Переключение видимости списка комментариев
        if (commentsList.style.display === 'none') {
            commentsList.style.display = 'block';
            toggleButton.textContent = 'Скрыть комментарии';
        } else {
            commentsList.style.display = 'none';
            toggleButton.textContent = 'Показать комментарии';
        }

        // Также можно показать или скрыть форму добавления комментария
        if (addCommentForm.style.display === 'none') {
            addCommentForm.style.display = 'block';
        } else {
            addCommentForm.style.display = 'none';
        }
    });
});