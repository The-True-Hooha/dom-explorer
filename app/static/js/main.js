document.addEventListener("DOMContentLoaded", function () {
  const searchForm = document.getElementById("searchForm");
  const resultsSection = document.getElementById("results");
  const resultsContent = document.getElementById("resultsContent");
  const loader = document.getElementById("loader");

  loader.classList.add("hidden");

  searchForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const domain = document.getElementById("domainInput").value;

    // Show loader only when search is initiated
    loader.classList.remove("hidden");
    resultsSection.classList.add("hidden");

    try {
      const response = await fetch(
        `/api/v1/search?domain=${encodeURIComponent(domain)}`
      );

      if (response.status === 401) {
        window.location.href = "/auth/login";
        return;
      }

      if (!response.ok) {
        throw new Error("Search failed");
      }

      const data = await response.json();
      displayResults(data);
    } catch (error) {
      console.error("Error:", error);
      resultsContent.innerHTML =
        "<p>An error occurred while searching. Please try again.</p>";
      resultsSection.classList.remove("hidden");
    } finally {
      loader.classList.add("hidden");
    }
  });

  function displayResults(data) {
    let html = `
            <p>Total subdomains found: ${data.count}</p>
            <h4>Regular Subdomains:</h4>
            <ul>
                ${data.regular
                  .map((subdomain) => `<li>${subdomain}</li>`)
                  .join("")}
            </ul>
            <h4>Wildcard Subdomains:</h4>
            <ul>
                ${data.wildcards
                  .map((subdomain) => `<li>${subdomain}</li>`)
                  .join("")}
            </ul>
        `;

    resultsContent.innerHTML = html;
    resultsSection.classList.remove("hidden");
  }
});
