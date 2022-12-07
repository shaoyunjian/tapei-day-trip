"use strict"
// --------------- User Modal  ------------------

const loginModal = document.querySelector(".login-modal")
const registerModal = document.querySelector(".register-modal")
const modalCloseBtn = document.querySelectorAll(".modal-close-btn")
const loginModalFooter = document.querySelector(".login-modal-footer")
const registerModalFooter = document.querySelector(".register-modal-footer")
const navLoginRegisterBtn = document.querySelector(".nav-login-register-btn")

navLoginRegisterBtn.addEventListener("click", openLoginModal)
loginModalFooter.addEventListener("click", openRegisterModal)
registerModalFooter.addEventListener("click", openLoginModal)

modalCloseBtn.forEach((value) => {
  value.addEventListener("click", () => {
    closeModal()
  })
})

document.addEventListener("click", (event) => {
  if(event.target === loginModal || event.target === registerModal){
    closeModal()
  }
})


// ------------- Modal function -----------------

function openLoginModal(event) {
  event.preventDefault()
  loginModal.style.display = "block"
  registerModal.style.display = "none"
}

function openRegisterModal() {
  loginModal.style.display = "none"
  registerModal.style.display = "block"
}

function closeModal() {
  loginModal.style.display = "none"
  registerModal.style.display = "none"
}


// ---------------  Register ---------------------- 

const registerBtn = document.querySelector(".register-btn")
const inputRegisterName = document.querySelector("#input-register-name")
const inputRegisterEmail = document.querySelector("#input-register-email")
const inputRegisterPassword = document.querySelector("#input-register-password")
const registerModalStatus = document.querySelector("#register-modal-status")

registerBtn.addEventListener("click", () => {
  const url = "/api/user"
  const inputRegisterNameValue = inputRegisterName.value
  const inputRegisterEmailValue = inputRegisterEmail.value
  const inputRegisterPasswordValue = inputRegisterPassword.value

  register()
  async function register() {
    const response = await fetch(url, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        name: inputRegisterNameValue,
        email: inputRegisterEmailValue,
        password: inputRegisterPasswordValue
      })
    })
    const jsonData = await response.json()

    if (jsonData["message"] === "email already exists"){
      registerModalStatus.innerHTML = `
      <div class="status-description">電子信箱已註冊</div>`
    } else if (jsonData["message"] === "empty input"){
      registerModalStatus.innerHTML = `
      <div class="status-description">請勿輸入空白</div>`
    } else if(jsonData["ok"] === true){
      registerModalStatus.innerHTML = `
      <div class="status-description">註冊成功</div>`
      registerModalFooter.innerHTML = "點此登入"
      inputRegisterName.value = ""
      inputRegisterEmail.value = ""
      inputRegisterPassword.value= ""
    } else {
      console.log("error")
    }
  }
})


// ------------------- Login ----------------------

const loginBtn = document.querySelector(".login-btn")
const inputLoginEmail = document.querySelector("#input-login-email")
const inputLoginPassword = document.querySelector("#input-login-password")
const loginModalStatus = document.querySelector("#login-modal-status")

loginBtn.addEventListener("click", () => {
  const url = "/api/user/auth"
  const inputLoginEmailValue = inputLoginEmail.value
  const inputLoginPasswordValue = inputLoginPassword.value

  login()
  async function login() {
    const response = await fetch(url, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        email: inputLoginEmailValue,
        password: inputLoginPasswordValue
      })
    })

    const jsonData = await response.json()
    if (jsonData["ok"]) {
     window.location = window.location.href
    } else if (jsonData["message"] === "empty input"){
      loginModalStatus.innerHTML = `
      <div class="status-description">請勿輸入空白</div>`
    } else {
      loginModalStatus.innerHTML = `
      <div class="status-description">電子郵件或密碼輸入錯誤</div>`
    }
  }

  inputLoginEmail.value = ""
  inputLoginPassword.value= ""
})


// ----------- Load and check login status---------

const navLoginLogoutBtn = document.querySelector(".nav-login-logout-btn")

window.addEventListener("DOMContentLoaded", () => {
  const url = "/api/user/auth"

  checkLoginStatus()
  async function checkLoginStatus() {
    const response = await fetch(url, {
      method: "GET",
      headers: {"Content-Type": "application/json"}
    })
    const jsonData = await response.json()
    if(jsonData["data"] !== null){
      navLoginRegisterBtn.style.display="none"
      logoutBtn.style.display="block"
    } 
  }
})


// ------------------ Logout ---------------------

const logoutBtn = document.querySelector(".logout-btn")

logoutBtn.addEventListener("click", (event) => {
  event.preventDefault()
  const url = "/api/user/auth"

  logout()
  async function logout(){
    const response = await fetch(url, {
      method: "DELETE",
      headers: {"Content-Type": "application/json"}
    })
    const jsonData = await response.json()
    window.location = window.location.href
  }

})