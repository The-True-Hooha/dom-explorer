let currentDomainId = null;
let currentPage = 1;
const itemsPerPage = 10;

document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("subdomainModal");
  const closeBtn = modal.querySelector(".close");
  const viewButtons = document.querySelectorAll(".view-btn");

  viewButtons.forEach((button) => {
    button.addEventListener("click", function () {
      currentDomainId = this.getAttribute("data-domain-id");
      currentPage = 1;
      fetchSubdomains(currentDomainId, 0, itemsPerPage);
    });
  });

  closeBtn.addEventListener("click", function () {
    modal.style.display = "none";
  });

  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
});

async function fetchSubdomains(domainId, skip, limit) {
  try {
    const response = await fetch(
      `/api/v1/domains/${domainId}?skip=${skip}&limit=${limit}`
    );
    if (!response.ok) {
      throw new Error("Failed to fetch subdomains");
    }
    const data = await response.json();
    displaySubdomains(data);
  } catch (error) {
    console.error("Error:", error);
    alert("Failed to fetch subdomains. Please try again.");
  }
}

function displaySubdomains(data) {
  const subdomainList = document.getElementById("subdomainList");
  const pagination = document.getElementById("pagination");
  const modal = document.getElementById("subdomainModal");

  // Create table structure
  let tableHTML = `
    <table class="subdomain-table">
      <thead>
        <tr>
          <th>Subdomain Name</th>
          <th>Status</th>
          <th>Created Date</th>
        </tr>
      </thead>
      <tbody>
  `;

  data.sub_domains.forEach((subdomain) => {
    tableHTML += `
      <tr>
        <td>${subdomain.name}</td>
        <td>${subdomain.isActive ? "Active" : "Active"}</td>
        <td>${new Date(subdomain.createdDate).toLocaleString()}</td>
      </tr>
    `;
  });

  tableHTML += `
      </tbody>
    </table>
  `;

  subdomainList.innerHTML = tableHTML;
  updatePagination(data);
  modal.style.display = "block";
}

function updatePagination(data) {
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";
  const totalPages = Math.ceil(data.total_subdomains / itemsPerPage);

  if (currentPage > 1) {
    pagination.innerHTML += `<button onclick="changePage(${
      currentPage - 1
    })">Previous</button>`;
  }

  for (let i = 1; i <= totalPages; i++) {
    if (i === currentPage) {
      pagination.innerHTML += `<span>${i}</span>`;
    } else {
      pagination.innerHTML += `<button onclick="changePage(${i})">${i}</button>`;
    }
  }

  if (currentPage < totalPages) {
    pagination.innerHTML += `<button onclick="changePage(${
      currentPage + 1
    })">Next</button>`;
  }
}

function changePage(newPage) {
  currentPage = newPage;
  const skip = (currentPage - 1) * itemsPerPage;
  fetchSubdomains(currentDomainId, skip, itemsPerPage);
}
