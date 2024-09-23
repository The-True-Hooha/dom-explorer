async function getProfile() {
  const response = await fetch(`/api/v1/profile/me`, {
    credentials: "include",
  });
  if (!response.ok) throw new Error("Failed to fetch profile");
  return response.json();
}

async function searchSubdomains(domain) {
  const response = await fetch(`/api/v1/search?domain=${domain}`, {
    credentials: "include",
  });
  if (!response.ok) throw new Error("Failed to fetch subdomains");
  return response.json();
}



async function RegisterApi(email, password) {
  try {
    const data = await fetch("/api/v1/signup", {
      headers: AuthHeaders,
    });
  } catch (err) {
    throw err;
  }
}

function AuthHeaders() {
  return {
    "Content-Type": "application/json",
  };
}


