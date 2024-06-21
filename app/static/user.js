function logout() {
        window.location.href = '/logout';
  }
  const surnameInput = document.querySelector('.i1');
  const nameInput = document.querySelector('.i2');
  const phoneInput = document.querySelector('.i3');
  const emailInput = document.querySelector('.i4');
  const saveButton = document.querySelector('#saveButton');


// Открыть модальное окно
document.getElementById("open-modal-btn").addEventListener("click", function() {
document.getElementById("my-modal").classList.add("open");
})

// Закрыть модальное окно
document.getElementById("close-my-modal-btn").addEventListener("click", function() {
document.getElementById("my-modal").classList.remove("open")
})

// Закрыть модальное окно при нажатии на Esc
window.addEventListener('keydown', (e) => {
if (e.key === "Escape") {
  document.getElementById("my-modal").classList.remove("open")
}
});

// Закрыть модальное окно при клике вне его
document.querySelector("#my-modal .modal__box").addEventListener('click', event => {
event._isClickWithInModal = true;
});
document.getElementById("my-modal").addEventListener('click', event => {
if (event._isClickWithInModal) return;
event.currentTarget.classList.remove('open');
});

saveButton.addEventListener('click', () => {
  // Получение значений из полей ввода
  const surname = surnameInput.value;
  const name = nameInput.value;
  const phone = phoneInput.value;
  const email = emailInput.value;

  // Создание объекта с данными для отправки на сервер
  const data = { surname, name, phone, email };

  // Отправка данных на сервер через запрос POST
  fetch('/user', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
      .then(response=>
  {
    // Обработка ответа от сервера
    if (response.success) {
      window.location.href = "/user"
    } else {
      console.error('Ошибка при обновлении данных');
    }
  })
  .catch(error => {
    console.error('Ошибка при отправке данных:', error);
  });
});

