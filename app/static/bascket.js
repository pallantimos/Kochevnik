let cartItems = [];

function loadCartItems() {
  fetch('/shoppingcart')
    .then(response => response.json())
    .then(data => {
      cartItems = data;
      renderCartItems();
    })
    .catch(error => console.error('Error:', error));
}

loadCartItems();

function renderCartItems() {
  const cartItemsContainer = document.querySelector('.cart__items');
  cartItemsContainer.innerHTML = '';

  cartItems.forEach((item, index) => {
    const cartItem = document.createElement('div');
    cartItem.classList.add('cart__item');

    const image = document.createElement('img');
    image.classList.add('cart__item-image');
    image.src = item.image;
    image.alt = item.Name;
    cartItem.appendChild(image);

    const itemInfo = document.createElement('div');
    itemInfo.classList.add('cart__item-info');

    const name = document.createElement('h3');
    name.classList.add('cart__item-name');
    name.textContent = item.Name;
    itemInfo.appendChild(name);

    const price = document.createElement('p');
    price.classList.add('cart__item-price');
    price.textContent = `${item.Price * item.Amount} ₽`;
    itemInfo.appendChild(price);

    const quantity = document.createElement('div');
    quantity.classList.add('kolich');

    const minusButton = document.createElement('button');
    minusButton.classList.add('Rectangleleft');
    minusButton.textContent = '-';
    minusButton.addEventListener('click', () => {
      changeQuantity(index, -1);
    });
    quantity.appendChild(minusButton);

    const kols = document.createElement('div');
    kols.classList.add('kols');
    kols.textContent = item.Amount;
    quantity.appendChild(kols);

    const plusButton = document.createElement('button');
    plusButton.classList.add('plus');
    plusButton.textContent = '+';
    plusButton.addEventListener('click', () => {
      changeQuantity(index, 1);
    });
    quantity.appendChild(plusButton);

    itemInfo.appendChild(quantity);
    cartItem.appendChild(itemInfo);

    const removeButton = document.createElement('button');
    removeButton.classList.add('cart__item-remove');
    removeButton.textContent = 'Удалить';
    removeButton.addEventListener('click', () => {
      removeItemFromCart(index);
    });
    cartItem.appendChild(removeButton);

    cartItemsContainer.appendChild(cartItem);
  });

  const totalPrice = document.querySelector('.cart__summary-price').textContent;

  updateCartSummary();
}

// Функция изменения количества элемента корзины
function changeQuantity(index, delta) {
  // Изменение количества элемента корзины на указанное значение
  cartItems[index].Amount += delta;
  cartItems[index].delta = delta;
  let jsonData = JSON.stringify(cartItems[index]);
  let pmk = new XMLHttpRequest();
  pmk.open('POST', '/shoppingcart', true); // указываем метод POST и адрес сервера
  pmk.setRequestHeader('Content-Type', 'application/json');

  // Если количество элемента корзины стало меньше или равно нулю, то удаление элемента корзины
  if (cartItems[index].Amount <= 0) {
    cartItems[index].Amount += 1;
  } else {
    // Сохранение массива cartItems в локальное хранилище
    // Вызов функции renderCartItems() для отрисовки элементов корзины на странице
    renderCartItems();
    pmk.send(jsonData); // отправляем JSN данные на сервOер
  }
}

function removeItemFromCart(index) {
  cartItems[index].delete = "true";
  let jsonData = JSON.stringify(cartItems[index]);
  let pmk = new XMLHttpRequest();
  pmk.open('POST', '/shoppingcart', true); // указываем метод POST и адрес сервера
  pmk.setRequestHeader('Content-Type', 'application/json');
  pmk.send(jsonData); // отправляем JSN данные на сервOер

  cartItems.splice(index, 1);
  renderCartItems();
}

function loadCartItems() {
  fetch('/shoppingcart')
    .then(response => response.json())
    .then(data => {
      cartItems = data;
      renderCartItems();
    })
    .catch(error => console.error('Error:', error));
}

loadCartItems();
renderCartItems();

function updateCartSummary() {
  let totalPrice = 0;
  cartItems.forEach(item => {
    totalPrice += parseInt(item.Price) * parseInt(item.Amount);
  });
  const cartSummary = document.querySelector('.cart__summary-price');
  cartSummary.textContent = totalPrice + ' ₽';
}