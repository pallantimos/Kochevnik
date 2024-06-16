function bookRoom() {
    // Получаем данные из формы бронирования
    const roomName = 'СТАНДАРТ с одной широкой кроватью'; // Замените на название номера
    const checkinDate = document.getElementById('checkin-date').value;
    const checkoutDate = document.getElementById('checkout-date').value;

    // Отправляем данные на сервер через POST-запрос
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/indhotel', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ roomName, checkinDate, checkoutDate }));

    // Обработка ответа сервера
    xhr.onload = function() {
      if (xhr.status === 200) {
          window.location.href= "/verbron"
        alert("В доработке")
      } else {
        // Произошла ошибка при отправке данных
        alert('Произошла ошибка при бронировании. Пожалуйста, попробуйте еще раз.');
      }
    };
}