function submitOrder(){
  console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/order', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ "sumbit": "true" }));

    // Обработка ответа сервера
    xhr.onload = function() {
      if (xhr.status === 200) {
        window.location.href= "/verorder"
      } else {
        // Произошла ошибка при отправке данных
        alert('Произошла ошибка при заказе. Пожалуйста, попробуйте еще раз.');
      }
    };
}
