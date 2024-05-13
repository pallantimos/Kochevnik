const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
let totalPrice = 0;
cartItems.forEach(item => {
totalPrice += parseInt(item.price) * parseInt(item.quantity);
});
const orderSummaryPrice = document.querySelector('.order__summary-price');
orderSummaryPrice.textContent = totalPrice + ' ₽';

document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // предотвратить отправку формы


    let formData = {};
    // собираем значения полей формы и добавляем их в объект formData
    document.querySelectorAll('.order').forEach(function(p) {
        formData[p.name] = p.value;
    });

    let jsonData = JSON.stringify(formData); // преобразуем объект в JSON строку

    // отправляем данные на сервер с помощью AJAX
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/ordersubmit', true); // указываем метод POST и адрес сервера
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
    xhr.send(jsonData); // отправляем JSN данные на сервOер
});