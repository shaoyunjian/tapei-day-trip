"use strict"
const bookingContainer = document.querySelector(".booking-container")
const noItinerary = document.querySelector(".no-itinerary")
const itineraryItems = document.querySelector(".itinerary-items")
const itineraryItem = document.querySelectorAll(".itinerary-item")
const greeting = document.querySelector(".greeting")
const greetingUsername = document.querySelector(".greeting-username")
const totalAmount = document.querySelector(".total-amount")


// ------------ Check login status ------------

document.addEventListener("DOMContentLoaded", ()=> {
  loginStatus()
  async function loginStatus(){
    await checkLoginStatus() 
    if (isLoggedIn) {
      initialLoad()
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
    headers: {"Content-Type": "application/json"}
  })
  const jsonData = await response.json()
  if(jsonData.data !== null){
    greetingUsername.textContent= jsonData.data.name
  }
}

// ---------------- Initial load ---------------------

async function initialLoad(){
  const response = await fetch("/api/booking",{
    method: "GET",
    headers: {"Content-Type": "application/json"}
  })

  const jsonData = await response.json()

  if (!jsonData.data){
    noItinerary.style.display = "block"
    bookingContainer.style.display = "none"
  } else {
    let totalPrice = 0
    jsonData.data.forEach((item)=>{
      loadItineraryItem(item)
      totalPrice += item.price
    })
    totalAmount.innerHTML = `總價：新台幣 ${totalPrice} 元`
    deleteItineraryItem()
  }
}

// ------------- Load itinerary -----------------

function loadItineraryItem(data){
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


// ------------------ delete items--------------------

function deleteItineraryItem(){
  const deleteBtns = document.querySelectorAll(".delete-icon")
  for (let deleteBtn of deleteBtns){
    deleteBtn.addEventListener("click", (event)=> {
      const bookingId = event.target.dataset.id
      checkLoginStatus()
      
      fetchDeleteBookingAPI(bookingId)
      async function fetchDeleteBookingAPI(id){
        const response = await fetch("/api/booking", {
          method: "DELETE",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            booking_id: id
          })
        })
        
        const jsonData = await response.json()
        if(jsonData.ok){
          window.location = window.location.href
        }
    }})
  }
}

