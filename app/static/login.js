document.getElementById('login-form').addEventListener('submit', function(event) {
  event.preventDefault(); // предотвратить отправку формы

  let formData = {};
  // собираем значения полей формы и добавляем их в объект formData
  document.querySelectorAll('.vvod').forEach(function(input) {
    formData[input.name] = input.value;
  });

  let jsonData = JSON.stringify(formData); // преобразуем объект в JSON строку

  // отправляем данные на сервер с помощью AJAX
  let xhr = new XMLHttpRequest();
  xhr.open('POST', '/login', true); // указываем метод POST и адрес сервера
  xhr.setRequestHeader('Content-Type', 'application/json');

  xhr.onload = function() {
    if (xhr.status >= 200 && xhr.status < 300) {
      console.log('Данные успешно отправлены на сервер!');
      window.location.href= "/user"
      let response = JSON.parse(xhr.responseText);
      // Check if the response indicates success
      if (response.success) {
      // Redirect the user to the index page
    }}
    else {
      let response = JSON.parse(xhr.responseText);
      console.error(response.error);
    }
  };
  xhr.send(jsonData); // отправляем JSON данные на сервер
});