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
  console.log(item)
  console.log(cartItems)
  let cartItemsJson = JSON.stringify(item);
  let xhr = new XMLHttpRequest();
  xhr.open('POST', '/menu', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function() {
    if (xhr.status === 200) {
      console.log('Данные отправилисьь');
    } else {
      console.log('Че-то не так:', xhr.responseText);
    }
  };
  xhr.send(cartItemsJson);
}

