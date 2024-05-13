document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('password1');
    const errorText = document.getElementById('error-msg');
    const passwordError = document.getElementById('password-error');

    passwordInput.addEventListener('input', function() {
        const passwordRegex = /^(?=.*\d)(?=.*[a-zа-я])(?=.*[A-ZА-Я])[a-zA-Zа-яА-Я0-9]{6,}$/;
        if (!passwordRegex.test(this.value)) {
            passwordError.style.display = 'block';
        } else {
            passwordError.style.display = 'none';
        }
    });

    confirmPasswordInput.addEventListener('input', function() {
        if (this.value !== passwordInput.value) {
            errorText.textContent = 'Пароли не совпадают';
            errorText.style.display = 'block';
        } else {
            errorText.textContent = '';
            errorText.style.display = 'none';
        }
    });
});

// НЕ ТРОГАТЬ ВСЕ ЧТО СНИЗУ!!!
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // предотвратить отправку формы


    let formData = {};
    // собираем значения полей формы и добавляем их в объект formData
    document.querySelectorAll('.vvod').forEach(function(input) {
         if (input.name !== "confirmPassword") {
        formData[input.name] = input.value;
    }
    });

    let jsonData = JSON.stringify(formData); // преобразуем объект в JSON строку

    // отправляем данные на сервер с помощью AJAX
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/registratesubmit', true); // указываем метод POST и адрес сервера
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 300) {
            location.href = "./"
            console.log('Данные успешно отправлены на сервер!');
            // здесь можно добавить дополнительную обработку успешной отправки данных
        } else if (xhr.status >= 400) {
            const passwordInput = document.getElementById('vvod password');
            const errorMessage = document.getElementById('error-msg')
            let response = JSON.parse(xhr.responseText);
            console.error(response.error);
            passwordInput.style.borderColor = 'red';
            errorMessage.text = xhr.response.JSON.password;
            console.error('Произошла ошибка при отправке данных на сервер.');
        }
    };
    xhr.send(jsonData); // отправляем JSON данные на сервер
});