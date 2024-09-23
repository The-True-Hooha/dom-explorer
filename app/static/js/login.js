// import { loginRequest } from "./api";

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document
        .querySelectorAll(".tab")
        .forEach((t) => t.classList.remove("active"));
      document
        .querySelectorAll(".tab-content")
        .forEach((c) => c.classList.remove("active"));
      tab.classList.add("active");
      document
        .getElementById(tab.getAttribute("data-tab") + "Form")
        .classList.add("active");
    });
  });

  document
    .querySelector("#loginForm form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("login-email").value;
      console.log(email);
      const password = document.getElementById("login-password").value;
      document.getElementById("loginMessage").textContent =
        HandleAuthInputValidation(email, password, "loginMessage");
      const data = await handleAuthRequest(email, password, "login")
      // const data = await loginRequest(email, password)
      document.getElementById("loginMessage").textContent = data.detail
    });

  document
    .querySelector("#registerForm form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("register-email").value;
      const password = document.getElementById("register-password").value;
    
      document.getElementById("registerMessage").textContent =
        HandleAuthInputValidation(email, password, "registerMessage");
      const data = await handleAuthRequest(email, password, "signup");
      document.getElementById("registerMessage").textContent = data.detail;
    });
});

function HandleAuthInputValidation(email, password, element) {
  const messageElement = document.getElementById(element);
  messageElement.textContent = "";

  const emailCheck = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailCheck.test(email)) {
    return (messageElement.textContent = "Invalid email format");
  }

  const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/;
  if (!passwordPattern.test(password)) {
    return (messageElement.textContent =
      "Password must be at least 6 characters long, contain at least one letter and one number");
  }
}

export async function handleAuthRequest(email, password, type) {
  try {
    const body = {
      email: email,
      password: password,
    };
    const url = type === "login" ? "/api/v1/login" : "/api/v1/signup";
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    const data = await response.json();
    if (response.ok) {
      console.log(data)
      window.location.href = "/profile";
    } else {
      return data.detail || "the server is unreachable at the moment";
    }
  } catch (error) {
    alert(error);
    console.log(error);
  }
}