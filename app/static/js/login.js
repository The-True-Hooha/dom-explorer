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
      console.log(password);
      // document.getElementById("loginMessage").textContent =
        // HandleAuthInputValidation(email, password, "loginMessage");
      const data = await handleAuthRequest(email, password, "login")
      // const data = await loginRequest(email, password)
      document.getElementById("loginMessage").textContent = data
      // try {
      //   const response = await fetch("/api/v1/token", {
      //     method: "POST",
      //     headers: { "Content-Type": "application/x-www-form-urlencoded" },
      //     body: `email=${encodeURIComponent(
      //       email
      //     )}&password=${encodeURIComponent(password)}`,
      //   });
      //   if (response.ok) {
      //     window.location.href = "/profile";
      //   } else {
      //     const data = await response.json();
      //     document.getElementById("loginMessage").textContent =
      //       data.detail || "Login failed";
      //   }
      // } catch (error) {
      //   console.error("Login error:", error);
      //   document.getElementById("loginMessage").textContent =
      //     "An error occurred. Please try again.";
      // }
    });

  document
    .querySelector("#registerForm form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();
      //   const username = document.getElementById("register-username").value;
      const email = document.getElementById("register-email").value;
      const password = document.getElementById("register-password").value;
      const confirmPassword = document.getElementById(
        "register-confirm-password"
      ).value;

      if (password !== confirmPassword) {
        document.getElementById("registerMessage").textContent =
          "Passwords do not match";
        return;
      }

      try {
        const response = await fetch("/api/v1/users", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });
        if (response.ok) {
          document.getElementById("registerMessage").textContent =
            "Registration successful! Please login.";
        } else {
          const data = await response.json();
          document.getElementById("registerMessage").textContent =
            data.detail || "Registration failed";
        }
      } catch (error) {
        console.error("Registration error:", error);
        document.getElementById("registerMessage").textContent =
          "An error occurred. Please try again.";
      }
    });
});

function HandleAuthInputValidation(email, password, element) {
  console.log("hello here", email);
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


/*
test data
{
  "email": "a11@gmail.com",
  "password": "some_password"
}
*/