document.addEventListener("DOMContentLoaded", function() {
  const table = document.getElementById("billTable");
  const rows = table.querySelectorAll("tbody tr");
  const rowsPerPage = 8;
  let currentPage = 1;

  function displayTable(page) {
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;

    rows.forEach((row, index) => {
      row.style.display = (index >= start && index < end) ? "" : "none";
    });

    document.getElementById("pageInfo").textContent =
      `Page ${page} of ${Math.ceil(rows.length / rowsPerPage)}`;

    document.getElementById("prevBtn").disabled = (page === 1);
    document.getElementById("nextBtn").disabled = (page === Math.ceil(rows.length / rowsPerPage));
  }

  document.getElementById("prevBtn").addEventListener("click", function() {
    if (currentPage > 1) {
      currentPage--;
      displayTable(currentPage);
    }
  });

  document.getElementById("nextBtn").addEventListener("click", function() {
    if (currentPage < Math.ceil(rows.length / rowsPerPage)) {
      currentPage++;
      displayTable(currentPage);
    }
  });

  displayTable(currentPage);
});
