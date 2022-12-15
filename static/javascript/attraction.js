"use strict"
const url = window.location.href
const attractionId = url.split("/")[4]
const title = document.querySelector("title")
const slideImageContainer = document.querySelector(".slide-image-container")
const slideImages = document.querySelector(".slide-images")
const attractionName = document.querySelector(".attraction-name")
const categoryMrt = document.querySelector(".category-mrt")
const attractionIntro = document.querySelector(".attraction-intro")
const addressDetail = document.querySelector(".address-detail")
const transportationDetail = document.querySelector(".transportation-detail")
const attractionImages = []

attractionName.textContent = ""
categoryMrt.innerHTML = ""
attractionIntro.textContent = ""
addressDetail.textContent = ""
transportationDetail.textContent = ""

// ----------- Fetch attraction id ------------

fetchAttractionId()
async function fetchAttractionId(){
  const response = await fetch(`/api/attraction/${attractionId}`)
  const jsonData = await response.json()

  const data = jsonData.data
  const images = data.images
  const name = data.name
  const category = data.category
  const mrt = data.mrt
  const description = data.description
  const address = data.address
  const transport = data.transport
  const imageNumber = data.images.length
  const dots = document.querySelector(".dots")

  title.textContent = name + " - 台北一日遊"
  slideImageContainer.innerHTML =`<img src="${images[0]}" alt="attraction-images" class="slide-images">`
  attractionName.textContent = name
  categoryMrt.innerHTML = `${category} at ${mrt}`
  attractionIntro.textContent = description
  addressDetail.textContent = address
  transportationDetail.textContent = transport
  
  // -------- Add dots and attraction images --------

  for(let i = 0; i< imageNumber; i++){
    dots.innerHTML +=`<span class="dot" data-id="${i}"></span>`
    attractionImages.push(images[i])
  }

  // ---------------- Slideshow ----------------

  const leftArrow = document.querySelector(".left-arrow")
  const rightArrow = document.querySelector(".right-arrow")
  const dot = document.querySelector(".dot")
  const classNameIsDot = document.getElementsByClassName("dot");
  dot.classList.add("active")
  let currentIndex = 0


  // ------ Slideshow: left arrow ------ 

  leftArrow.addEventListener("click", ()=>{ 
    currentIndex -= 1
    if(currentIndex < 0){currentIndex = imageNumber - 1} 
    
    slideImageContainer.innerHTML =`
      <img src="${attractionImages[currentIndex]}" alt="attraction-images" class="slide-images">`

    const activeItem = document.querySelector(".active")
    if(activeItem){activeItem.classList.remove("active")}

    classNameIsDot[currentIndex].className += " active"
    if(currentIndex === imageNumber - 1 ){
      classNameIsDot[0].className = classNameIsDot[0].className.replace(" active", "")
    } else {classNameIsDot[currentIndex + 1].className = classNameIsDot[currentIndex + 1].className.replace(" active", "")}
  })


  // ------ Slideshow: right arrow ------ 
  
  rightArrow.addEventListener("click", ()=>{
    currentIndex += 1
    if(currentIndex + 1 > imageNumber){currentIndex = 0} 
    slideImageContainer.innerHTML =`
      <img src="${attractionImages[currentIndex]}" alt="attraction-images" class="slide-images">`

    const activeItem = document.querySelector(".active")
    if(activeItem){activeItem.classList.remove("active")}
    
    classNameIsDot[currentIndex].className += " active"
    if(!currentIndex){
      classNameIsDot[imageNumber - 1].className = classNameIsDot[imageNumber - 1].className.replace(" active", "")
    } else {classNameIsDot[currentIndex - 1].className = classNameIsDot[currentIndex - 1].className.replace(" active", "")}
  })

  
  // ------ Slideshow: dots ------ 

  dots.addEventListener("click", (event)=>{
    for(let i = 0; i < imageNumber; i++){
      if(event.target.dataset.id === `${i}`){
        currentIndex = i
        slideImageContainer.innerHTML =`
          <img src="${attractionImages[i]}" alt="attraction-images" class="slide-images">`

        const activeItem = document.querySelector(".active")
        if(activeItem){activeItem.classList.remove("active")}
        classNameIsDot[i].className += " active"
      }
    }
  })
}

// -------- Click to change itinerary time and price --------

const price = document.querySelector(".price")
const booking = document.querySelector(".booking")

booking.addEventListener("click", (event) => {
  if(event.target.id === "itinerary-morning") {
    price.textContent = `新台幣 2000 元`
    
  } else if(event.target.id === "itinerary-afternoon") 
    price.textContent = `新台幣 2500 元`
})


// -------- Itinerary booking -------------

const startBookingBtn = document.querySelector("#start-booking-btn")

startBookingBtn.addEventListener("click", (event) => {
  event.preventDefault()
  const itineraryDateValue = document.querySelector('input[type="date"]').value
  const itineraryTimeValue = document.querySelector('input[name="itinerary"]:checked').value
  const itineraryPriceValue = (itineraryTimeValue === "morning") ? "2000" : "2500"
  
  checkLoginStatus()
  if (!isLoggedIn){
    openLoginModal()
  } else {
    fetchAddItinerary()
    
    async function fetchAddItinerary(){
      const response = await fetch("/api/booking", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          attractionId: attractionId,
          itineraryDate: itineraryDateValue,
          itineraryTime: itineraryTimeValue,
          itineraryPrice: itineraryPriceValue
        })
      })

      const jsonData = await response.json()

      if (jsonData.ok){
        window.location = "/booking"
      } else if (jsonData.message === "data already exists"){
        const itineraryTime = (itineraryTimeValue === "morning") ? "上半天" : "下半天"
        let message = `
          <div>無法加入</div>
          <div style="font-size: 16px; margin-top: 10px;">
          (※${itineraryDateValue} ${itineraryTime} 已有預定行程)
          </div>
        `
        openMessageModal(message, "重新預定", "")
      } else if (jsonData.message === "input error"){
        openMessageModal("注意：請選擇日期", "好", "")
      }
    }
  }
})
