"use strict"
let initialPage = 0
let initialKeyword = ""
let loadAmount = 0
let nextPageArray = []
let attractionArea = document.querySelector(".attraction-area")
let isLoading = false

window.addEventListener("DOMContentLoaded", initialLoad(initialPage, initialKeyword))

// Initial loading
function initialLoad(page, keyword){
  isLoading = true
  fetch(`/api/attractions?page=${page}&keyword=${keyword}`)
    .then(response => {return response.json()})
    .then(data => {
      nextPageArray = []
      let nextPage = data["nextPage"]
      let dataLength = getAttractions(data)[1]

      if(dataLength === 0){
        attractionArea.innerHTML = "沒有相關搜尋結果"
      }

      if(nextPage !== null){
        nextPageArray.push(nextPage)
      }
      
      loadMoreAttractions(nextPage, keyword)
      isLoading = false
    }).catch((error)=>{
      console.log(error)
      isLoading = false
    })
}


// Scroll to load more attraction infos
function loadMoreAttractions(nextPage, keyword){
  const footer = document.querySelector("footer")
  const callback = (entries, observer) => {
  if(entries[0].isIntersecting && isLoading === false){
    loadAmount += 1
    nextPage = nextPageArray.length
    if (loadAmount-nextPage <= 0){
      fetchAPI(nextPage, keyword)
    } else{
      observer.unobserve(footer)
    }}
  }
  const option = {threshold: 0.5} //50% of the target is visible
  const observer = new IntersectionObserver(callback, option)
  observer.observe(footer)
}


// Fetch API
function fetchAPI(page, keyword){
  isLoading = true
  fetch(`/api/attractions?page=${page}&keyword=${keyword}`)
  .then(response => {return response.json()})
  .then(data => {
    let nextPage = getAttractions(data)[0]
    if(nextPage){
      nextPageArray.push(nextPage)}
    isLoading = false
  }).catch((error)=>{
    console.log(error)
    isLoading = false
  })
}


// Get attractions
function getAttractions(data){
  let nextPage = data["nextPage"]
  let dataLength = data["data"].length
  for (let i =0; i < data["data"].length; i++){
    let imgURL = data["data"][i]["images"][0]
    let name = data["data"][i]["name"]
    let mrt = data["data"][i]["mrt"]
    let category = data["data"][i]["category"]

    let attraction = document.createElement("div")
    attraction.classList.add("attraction")
    attractionArea.appendChild(attraction)

    let image = document.createElement("img")
    image.src = imgURL
    image.classList.add("attraction-img")
    attraction.appendChild(image)

    let attractionName = document.createElement("div")
    attractionName.classList.add("attraction-name")
    attractionName.textContent = name
    attraction.appendChild(attractionName)

    let attractionInfo = document.createElement("div")
    attractionInfo.classList.add("attraction-info")
    attraction.appendChild(attractionInfo)

    let transportation = document.createElement("div")
    transportation.classList.add("info-transportation")
    transportation.textContent = mrt
    attractionInfo.appendChild(transportation)

    let infoCategory = document.createElement("div")
    infoCategory.classList.add("info-category")
    infoCategory.textContent = category
    attractionInfo.appendChild(infoCategory)
  }
  return [nextPage, dataLength]
}


// Click search btn to load attraction infos
const keywordInput = document.querySelector("#keyword-input")
const searchBtn = document.querySelector("#search-btn")

searchBtn.addEventListener("click", event => {
  event.preventDefault() 
  let inputValue = keywordInput.value
  attractionArea.innerHTML = ""
  loadAmount = 0
  initialLoad(initialPage, inputValue)
})


// Use category keyword to search attractions
const categoryContainer = document.querySelector(".category-container")

fetch("/api/categories")
.then(response => {return response.json()})
.then(data => {
  for(let i = 0; i< data["data"].length; i++){
    let category = document.createElement("div")
    category.classList.add("category")
    category.textContent = data["data"][i]
    category.setAttribute("data-id", `${i}`)
    categoryContainer.appendChild(category)
  }
  
  categoryContainer.addEventListener("click", (event)=>{
    let categoryID = Number(event.target.dataset.id)
    if(event.target.dataset.id){
    keywordInput.value = data["data"][categoryID]}
  })
})


// Click search btn to open/hide category menu
keywordInput.addEventListener("click", () => {
  categoryContainer.classList.toggle("search-mode")
})


// Close category menu by clicking outside
document.addEventListener("click", (event) => {
  if (event.target !== categoryContainer && event.target !==keywordInput){
    categoryContainer.classList.add("search-mode")
  }
})
