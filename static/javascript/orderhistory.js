// ------------ Check login status ------------

const orders = document.querySelector(".orders")
const orderHistoryArray = []

document.addEventListener("DOMContentLoaded", () => {
  loginStatus()
  async function loginStatus() {
    await checkLoginStatus()
    if (isLoggedIn) {
      await get_history_order_number()
    } else {
      window.location = "/"
    }
  }
})

// ------------- Get order number --------------

async function get_history_order_number() {
  const response = await fetch("/api/orderhistory", {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  })
  const jsonData = await response.json()
  if (jsonData.data) {
    const data = jsonData.data.historyOrderNumber

    data.forEach((value) => {
      orderNumber = value
      orderHistoryArray.push(value)
    })

    orderHistoryArray.forEach((orderNumber) => {
      getOrderInfoByOrderNumber(orderNumber)
    })
  } else {
    orders.innerHTML = `
    <div class="no-order-history">尚未有訂購紀錄</div>`
  }
}

// ------- Get order information by order number ----------

async function getOrderInfoByOrderNumber(orderNumber) {
  const response = await fetch(`/api/order/${orderNumber}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  })
  const jsonData = await response.json()

  getOrderInfo(jsonData.data)
}


// ---------------- Get order information -----------------

function getOrderInfo(data) {
  const orderContainer = document.createElement("div")
  orderContainer.classList.add("order-container")

  const orderNumber = document.createElement("div")
  orderNumber.classList.add("order-number")
  orderNumber.innerHTML = ` <b>訂單編號：</b>${data.number}`
  orderContainer.appendChild(orderNumber)

  const orderTotalAmount = document.createElement("div")
  orderTotalAmount.classList.add("order-total-amount")
  orderTotalAmount.innerHTML = ` <b>總金額：</b>${data.price}`
  orderContainer.appendChild(orderTotalAmount)

  data.trip.forEach((value) => {
    const orderItineraryContainer = document.createElement("div")
    orderItineraryContainer.classList.add("order-itinerary-container")

    const orderAttractionImage = document.createElement("div")
    orderAttractionImage.classList.add("order-attraction-image")
    const AttractionImage = document.createElement("img")
    AttractionImage.src = value.attraction.image
    orderAttractionImage.appendChild(AttractionImage)

    const orderInfoDetails = document.createElement("div")
    orderInfoDetails.classList.add("order-info-details")

    const orderAttractionName = document.createElement("div")
    const orderDate = document.createElement("div")
    const orderTime = document.createElement("div")
    const orderPrice = document.createElement("div")
    const orderAttractionAddress = document.createElement("div")

    orderAttractionName.classList.add("order-attraction-name")
    orderDate.classList.add("order-date")
    orderTime.classList.add("order-time")
    orderPrice.classList.add("order-price")
    orderAttractionAddress.classList.add("order-attraction-address")

    const tripTime = (value.time === "morning") ? "早上 8 點至 12 點" : "下午 2 點至 6 點"
    orderAttractionName.textContent = `${value.attraction.name}`
    orderDate.innerHTML = `<b>日期：</b> ${value.date}`
    orderTime.innerHTML = `<b>時間：</b> ${tripTime}`
    orderPrice.innerHTML = `<b>費用：</b> ${value.price}`
    orderAttractionAddress.innerHTML = `<b>地點：</b> ${value.attraction.address}`

    orderInfoDetails.appendChild(orderAttractionName)
    orderInfoDetails.appendChild(orderDate)
    orderInfoDetails.appendChild(orderTime)
    orderInfoDetails.appendChild(orderPrice)
    orderInfoDetails.appendChild(orderAttractionAddress)

    orderItineraryContainer.appendChild(orderAttractionImage)
    orderItineraryContainer.appendChild(orderInfoDetails)

    orderContainer.appendChild(orderItineraryContainer)
    orders.appendChild(orderContainer)
  })
}
