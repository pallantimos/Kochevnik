document.addEventListener("DOMContentLoaded", function() {
    let selectedOrderId = null;

// Открыть модальное окно
document.querySelectorAll(".item6").forEach(button => {
    button.addEventListener("click", function() {
        document.getElementById("my-modal").classList.add("open");
    });
});

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

document.querySelectorAll(".orderlist .item6").forEach(button => {
    button.addEventListener("click", function() {
        const parent = this.closest(".orderlist");
        selectedOrderId = parent.querySelector(".item1").textContent;
        console.log(selectedOrderId);
    });
});


    // Сохранить изменения статуса
  document.querySelector(".btn-save").addEventListener("click", function() {
    const statusId = document.querySelector(".status-list").value;
    const statusList = document.querySelector(".status-list");
    const selectedOption = statusList.options[statusList.selectedIndex];
    const statusName = selectedOption.textContent;
    console.log(statusName)

    fetch(`/adminorder`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ orderId: selectedOrderId, statusId: statusId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("my-modal").classList.remove("open");
            updateOrderStatusInView(selectedOrderId, statusName);
        } else {
            alert("Ошибка обновления статуса");
        }
    });
});

    function updateOrderStatusInView(orderId, statusName) {
    console.log("Сработало!!")
    const orderListElements = document.querySelectorAll('.orderlist');
    for (const orderListElement of orderListElements) {
        const item1Element = orderListElement.querySelector(`.item1`);
        if (item1Element.textContent === orderId) {
            const item5Element = orderListElement.querySelector('.item5');
            if (item5Element) {
                item5Element.textContent = statusName;
            }
        }
    }
}
});
