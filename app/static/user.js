function logout() {
        window.location.href = '/logout';
  }


  function editProfile() {
    // Показываем модальное окно
    $('#edit-profile-modal').modal('show');
  }

  function saveProfile() {
    // Получаем данные из формы
    const formData = new FormData($('#edit-profile-form')[0]);
    // Отправляем запрос на сервер
    fetch('/profile', {
      method: 'PUT',
      body: formData,
    })
    .then((response) => {
      if (response.ok) {
        // Обновляем информацию о пользователе в локальном хранилище
        response.json().then((data) => {
          localStorage.setItem('user', JSON.stringify(data));
          // Обновляем информацию о пользователе на странице
          $('.surname p').text(data.surname);
          $('.name p').text(data.name);
          $('.number p').text(data.phone);
          $('.email p').text(data.email);
          // Закрываем модальное окно
          $('#edit-profile-modal').modal('hide');
        });
      } else {
        alert('Ошибка при сохранении личных данных');
      }
    })
    .catch((error) => {
      console.error('Ошибка:', error);
      alert('Ошибка при сохранении личных данных');
    });
  }