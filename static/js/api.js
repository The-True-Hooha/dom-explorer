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

async function login(username, password) {
  const response = await fetch("/api/v1/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `username=${encodeURIComponent(
      username
    )}&password=${encodeURIComponent(password)}`,
    credentials: "include",
  });
  if (!response.ok) throw new Error("Failed to login");
  return response.json();
}
