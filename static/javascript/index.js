"use strict"
const initialPage = 0
const initialKeyword = ""
const attractionArea = document.querySelector(".attraction-area")
let loadAmount = 0
let nextPageArray = []
let isLoading = false

window.addEventListener("DOMContentLoaded", initialLoad(initialPage, initialKeyword))

// Initial loading
async function initialLoad(page, keyword){
  try {
    isLoading = true
    const url = `/api/attractions?page=${page}&keyword=${keyword}`
    const response = await fetch(url)
    const jsonData = await response.json()

    nextPageArray = []
    const nextPage = jsonData.nextPage
    const dataLength = getAttractions(jsonData)[1]

    if(!dataLength){
      attractionArea.innerHTML = "沒有相關搜尋結果"
    }

    if(nextPage){
      nextPageArray.push(nextPage)
    }
    
    loadMoreAttractions(nextPage, keyword)
    isLoading = false
  } catch (error) {
    console.log(error)
  }
}


// Scroll to load more attraction infos
function loadMoreAttractions(nextPage, keyword){
  const footer = document.querySelector("footer")
  const callback = (entries, observer) => {
    if (entries[0].isIntersecting && !isLoading) {
      loadAmount += 1
      nextPage = nextPageArray.length
      if (loadAmount-nextPage <= 0) {
        fetchAttractionsByPageOrKeyword(nextPage, keyword)
      } else {
        observer.unobserve(footer)
      }
    }
  }
  const option = {threshold: 0.5} //50% of the target is visible
  const observer = new IntersectionObserver(callback, option)
  observer.observe(footer)
}


// Fetch attractions by page or keyword
async function fetchAttractionsByPageOrKeyword(page, keyword) {
  try {
    isLoading = true
    const url = `/api/attractions?page=${page}&keyword=${keyword}`
    const response = await fetch(url)
    const jsonData = await response.json()

    let nextPage = getAttractions(jsonData)[0]
    if(nextPage){
      nextPageArray.push(nextPage)
    }
    isLoading = false
  } catch (error) {
    console.log(error)
  }
}


// Get attractions
function getAttractions(data){
  const nextPage = data.nextPage
  const dataLength = data.data.length
  for (let i =0; i < data.data.length; i++){
    const attractionID = data.data[i].id
    const imgURL = data.data[i].images[0]
    const name = data.data[i].name
    const mrt = data.data[i].mrt
    const category = data.data[i].category

    const attraction = document.createElement("a")
    attraction.setAttribute("href", `/attraction/${attractionID}`)
    attraction.classList.add("attraction")
    attractionArea.appendChild(attraction)

    const image = document.createElement("img")
    image.src = imgURL
    image.classList.add("attraction-img")
    attraction.appendChild(image)

    const attractionName = document.createElement("div")
    attractionName.classList.add("attraction-name")
    attractionName.textContent = name
    attraction.appendChild(attractionName)

    const attractionInfo = document.createElement("div")
    attractionInfo.classList.add("attraction-info")
    attraction.appendChild(attractionInfo)

    const transportation = document.createElement("div")
    transportation.classList.add("info-transportation")
    transportation.textContent = mrt
    attractionInfo.appendChild(transportation)

    const infoCategory = document.createElement("div")
    infoCategory.classList.add("info-category")
    infoCategory.textContent = category
    attractionInfo.appendChild(infoCategory)
  }
  return [nextPage, dataLength]
}


// Click search btn to load attraction infos
const keywordInput = document.querySelector("#keyword-input")
const searchBtn = document.querySelector("#search-btn")

searchBtn.addEventListener("click", (event) => {
  event.preventDefault() 
  const inputValue = keywordInput.value
  attractionArea.innerHTML = ""
  loadAmount = 0
  initialLoad(initialPage, inputValue)
})


// Use category keyword to search attractions
const categoryContainer = document.querySelector(".category-container")

fetchCategories()
async function fetchCategories() {
  try {
    const url = "/api/categories"
    const response = await fetch(url)
    const jsonData = await response.json()

    jsonData.data.forEach((element) => {
      const category = document.createElement("div")
      category.classList.add("category")
      category.textContent = element
      category.setAttribute("data-id", `${element}`)
      categoryContainer.appendChild(category)

      categoryContainer.addEventListener("click", (event) => {
        if(event.target.dataset.id === element) {
          keywordInput.value = element
        }
      })
    })
  }
  catch (error) { 
    console.log(error)
  }
}


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

