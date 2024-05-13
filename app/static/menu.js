let cartItems = [];
const addToCartButtons = document.querySelectorAll('.buttonbasket');
addToCartButtons.forEach(button => {
button.addEventListener('click', () => {
const image = button.dataset.image;
const name = button.dataset.name;
const price = button.dataset.price;
addItemToCart(image, name, price, 1);
});
});

function addItemToCart(image, name, price, quantity) {
  const item = { image, name, price, quantity };
  cartItems.push(item);
  saveCartItems();
}

function saveCartItems() {
  localStorage.setItem('cartItems', JSON.stringify(cartItems));
}

