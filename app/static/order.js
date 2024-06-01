let cartItems = [];

function loadCartItems() {
  fetch('/shoppingcart')
    .then(response => response.json())
    .then(data => {
      cartItems = data;
      calculateTotalPrice();
    })
    .catch(error => console.error('Error:', error));
}

loadCartItems()

function calculateTotalPrice() {
  let totalPrice = 0;
  cartItems.forEach(item => {
    totalPrice += parseInt(item.price) * parseInt(item.quantity);
  });
  const orderSummaryPrice = document.querySelector('.order__summary-price');
  console.log(totalPrice)
  orderSummaryPrice.textContent = totalPrice + ' ₽';
}

calculateTotalPrice()

function submitOrder(){
  console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/order', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ "sumbit": "true" }));

    // Обработка ответа сервера
    xhr.onload = function() {
      if (xhr.status === 200) {
        window.location.href= "/verbron"
      } else {
        // Произошла ошибка при отправке данных
        alert('Произошла ошибка при заказе. Пожалуйста, попробуйте еще раз.');
      }
    };
}
