"use strict"
const loader = document.querySelector(".loader")
const bookingContainer = document.querySelector(".booking-container")
const noItinerary = document.querySelector(".no-itinerary")
const itineraryItems = document.querySelector(".itinerary-items")
const itineraryItem = document.querySelectorAll(".itinerary-item")
const greeting = document.querySelector(".greeting")
const greetingUsername = document.querySelector(".greeting-username")
const totalAmount = document.querySelector(".total-amount")
let isLoading


// ------------ Check login status ------------

document.addEventListener("DOMContentLoaded", () => {
  loginStatus()
  async function loginStatus() {
    await checkLoginStatus()
    if (isLoggedIn) {
      await initialLoad()
      if (!isLoading) {
        loader.classList.add("display-none")
      }
    } else {
      greeting.style.display = "none"
      bookingContainer.style.display = "none"
      window.location = "/"
    }
  }
})

// ------------ Show username ------------

showUsername()
async function showUsername() {
  const response = await fetch("/api/user/auth", {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  })
  const jsonData = await response.json()
  if (jsonData.data) {
    greetingUsername.textContent = jsonData.data.name
  }
}

// ---------------- Initial load ---------------------
let bookingArray = []
let totalBookingPrice = ""
async function initialLoad() {
  isLoading = true
  const response = await fetch("/api/booking", {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  })

  const jsonData = await response.json()

  if (!jsonData.data) {
    noItinerary.style.display = "block"
    bookingContainer.style.display = "none"
  } else {
    let totalPrice = 0
    jsonData.data.forEach((item) => {
      loadItineraryItem(item)
      totalPrice += item.price
      bookingArray.push(item)
    })
    totalAmount.innerHTML = `總價：新台幣 ${totalPrice} 元`
    totalBookingPrice = totalPrice
    deleteItineraryItem()
  }
  isLoading = false
}

// ------------- Load itinerary -----------------

function loadItineraryItem(data) {
  const time = (data.time === "morning") ? "早上 8 點至 12 點" : "下午 2 點至 6 點"
  itineraryItems.innerHTML += `
    <div class="itinerary-item">
      <div class="booking-attraction-image">
        <img src=" ${data.attraction.image}">
      </div>
      <div class="itinerary-details">
        <div class="booking-attraction-title">台北一日遊：${data.attraction.name}</div>
        <div><b>日期：</b>${data.date}</div>
        <div><b>時間：</b>${time}</div>
        <div><b>費用：</b>新台幣 ${data.price} 元</div>
        <div><b>地點：</b> ${data.attraction.address}</div>
      </div>
      <div class="delete-icon-container">
        <img src="/static/images/icon_delete.png" alt="" class="delete-icon" data-id='${data.booking_id}'>
      </div>
    </div>
  `
}


// ------------------ Delete items--------------------

function deleteItineraryItem() {
  const deleteBtns = document.querySelectorAll(".delete-icon")
  for (let deleteBtn of deleteBtns) {
    deleteBtn.addEventListener("click", (event) => {
      const bookingId = event.target.dataset.id
      checkLoginStatus()

      fetchDeleteBookingAPI(bookingId)
      async function fetchDeleteBookingAPI(id) {
        const response = await fetch("/api/booking", {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            booking_id: id
          })
        })

        const jsonData = await response.json()
        if (jsonData.ok) {
          window.location = window.location.href
        }
      }
    })
  }
}

// ------------- Contact info ----------------

const inputName = document.querySelector("#input-name")
const inputEmail = document.querySelector("#input-email")
const inputPhone = document.querySelector("#input-phone")
const inputNameMessage = document.querySelector("#input-name-message")
const inputEmailMessage = document.querySelector("#input-email-message")
const inputPhoneMessage = document.querySelector("#input-phone-message")


inputName.addEventListener("input", (event) => {
  const inputNameValue = inputName.value.trim()
  if (!inputNameValue) {
    inputNameMessage.textContent = "＊請不要空白"
    event.target.classList.add("error-input")
  } else {
    inputNameMessage.textContent = ""
    event.target.classList.remove("error-input")
  }
})

inputEmail.addEventListener("input", (event) => {
  const inputEmailValue = inputEmail.value.trim()
  if (!inputEmailValue) {
    inputEmailMessage.textContent = "＊請不要空白"
    event.target.classList.add("error-input")
  } else {
    inputEmailMessage.textContent = ""
    event.target.classList.remove("error-input")
  }
})

inputPhone.addEventListener("input", (event) => {
  const inputPhoneValue = inputPhone.value.trim()
  if (!inputPhoneValue) {
    inputPhoneMessage.textContent = "＊請不要空白"
    event.target.classList.add("error-input")
  } else {
    inputPhoneMessage.textContent = ""
    event.target.classList.remove("error-input")
  }
})

// -------------- TapPay area ----------------

TPDirect.setupSDK(
  126866,
  "app_TkD1So34n96TIzrFmQSqgcmLiwvsPGUo244E0FckQWCnfXRVJ8iLicFIbe1o",
  "sandbox")

let fields = {
  number: {
    // css selector
    element: "#card-number",
    placeholder: "**** **** **** ****"
  },
  expirationDate: {
    // DOM object
    element: document.getElementById("card-expiration-date"),
    placeholder: "MM / YY"
  },
  ccv: {
    element: "#card-ccv",
    placeholder: "ccv"
  }
}

TPDirect.card.setup({
  fields: fields,
  styles: {
    // Styling ccv field
    "input.ccv": {
      "font-size": "16px"
    },
    // Styling expiration-date field
    "input.expiration-date": {
      "font-size": "16px"
    },
    // Styling card-number field
    "input.card-number": {
      "font-size": "16px"
    },
    // style focus state
    ":focus": {
      "color": "black"
    },
    // style valid state
    ".valid": {
      "color": "green"
    },
    // style invalid state
    ".invalid": {
      "color": "red"
    }
  },
  // after filling out the correct credit card number, the middle eight digits will be hidden
  isMaskCreditCardNumber: true,
  maskCreditCardNumberRange: {
    beginIndex: 4,
    endIndex: 11
  }
})

// ----------------------------------

const submitButton = document.querySelector("#submit-button")
const input = document.querySelectorAll("input")

submitButton.addEventListener("click", () => {
  const inputNameValue = inputName.value.trim()
  const inputEmailValue = inputEmail.value.trim()
  const inputPhoneValue = inputPhone.value.trim()

  if (!inputNameValue || !inputEmailValue || !inputPhoneValue) {
    openMessageModal("請不要有空白", "好")
  }

  const tappayStatus = TPDirect.card.getTappayFieldsStatus()
  if (tappayStatus.status.number != 0 ||
    tappayStatus.status.expiry != 0 ||
    tappayStatus.status.ccv != 0) {
    openMessageModal("請填入正確的信用卡資訊", "好")
  }

  // Get prime
  TPDirect.card.getPrime((result) => {
    if (result.status === 0) {
      const cardPrime = result.card.prime

      fetchCreateOrderAPI()
      async function fetchCreateOrderAPI() {
        const response = await fetch("/api/orders", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            prime: cardPrime,
            order: {
              totalAmount: totalBookingPrice,
              trip: bookingArray,
              contact: {
                name: inputNameValue,
                email: inputEmailValue,
                phone: inputPhoneValue
              }
            }
          })
        })
        const jsonData = await response.json()
        const orderNumber = jsonData.data.number
        window.location = `/thankyou?number=${orderNumber}`
      }
    }
  })

})
