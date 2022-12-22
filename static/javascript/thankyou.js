const url = window.location.href
const orderNumber = url.split("=")[1]

const orderNumberContainer = document.querySelector(".order-number")
orderNumberContainer.textContent = orderNumber
