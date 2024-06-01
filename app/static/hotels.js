let hotelItems = [];
const addToCartButtons = document.querySelectorAll('.hotelm');
addToCartButtons.forEach(button => {
button.addEventListener('click', () => {
const image = button.dataset.image;
const name = button.dataset.name;
addItemToCart(image, name);
});
});

function addItemToCart(image, name) {
  const item = { image, name };
  cartItems.push(item);
  saveCartItems();
}

function saveCartItems() {
  localStorage.setItem('cartItems', JSON.stringify(cartItems));
}

