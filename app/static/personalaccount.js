document.querySelectorAll(".item4").forEach(button => {
    button.addEventListener("click", function() {
        // Найти родительский элемент с классом "orderlist"
        const orderlistElement = this.closest(".orderlist");

        // Найти элемент с классом "Item1" внутри этого родительского элемента
        const userIdElement = orderlistElement.querySelector(".item1");
        const userId = userIdElement.textContent;

        fetch(`/personalaccount`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ userId: userId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Успешное обновление статуса
            } else {
                alert("Ошибка обновления статуса");
            }
        });
    });
});