let cartItems = [];

function loadCartItems() {
  const savedCartItems = localStorage.getItem('cartItems');
  if (savedCartItems) {
    cartItems = JSON.parse(savedCartItems);
  }
  renderCartItems();
}

loadCartItems();

function addItemToCart(image, name, price) {
  const item = { image, name, price, quantity: 1 };
  cartItems.push(item);
  saveCartItems();
  renderCartItems();
}

function renderCartItems() {
  const cartItemsContainer = document.querySelector('.cart__items');
  cartItemsContainer.innerHTML = '';

  cartItems.forEach((item, index) => {
    const cartItem = document.createElement('div');
    cartItem.classList.add('cart__item');

    const image = document.createElement('img');
    image.classList.add('cart__item-image');
    image.src = item.image;
    image.alt = item.name;
    cartItem.appendChild(image);

    const itemInfo = document.createElement('div');
    itemInfo.classList.add('cart__item-info');

    const name = document.createElement('h3');
    name.classList.add('cart__item-name');
    name.textContent = item.name;
    itemInfo.appendChild(name);

    const price = document.createElement('p');
    price.classList.add('cart__item-price');
    price.textContent = `${item.price * item.quantity} ₽`;
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
    kols.textContent = item.quantity;
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
localStorage.setItem('totalPrice', totalPrice);

  updateCartSummary();
}

function changeQuantity(index, delta) {
  cartItems[index].quantity += delta;
  if (cartItems[index].quantity <= 0) {
    removeItemFromCart(index);
  } else {
    saveCartItems();
    renderCartItems();
  }
}

function removeItemFromCart(index) {
  cartItems.splice(index, 1);
  saveCartItems();
  renderCartItems();
}

function saveCartItems() {
  localStorage.setItem('cartItems', JSON.stringify(cartItems));
}

function loadCartItems() {
  const savedCartItems = localStorage.getItem('cartItems');
  if (savedCartItems) {
    cartItems = JSON.parse(savedCartItems);
  }
}

loadCartItems();
renderCartItems();

function updateCartSummary() {
  let totalPrice = 0;
  cartItems.forEach(item => {
    totalPrice += parseInt(item.price) * parseInt(item.quantity);
  });
  const cartSummary = document.querySelector('.cart__summary-price');
  cartSummary.textContent = totalPrice + ' ₽';
}