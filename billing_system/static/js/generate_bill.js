document.addEventListener('DOMContentLoaded', () => {
  const itemsData = JSON.parse(document.getElementById('items-data').textContent);

  const itemsTableBody = document.querySelector('#itemsTable tbody');
  const addItemBtn = document.getElementById('addItemBtn');
  const deleteBtn = document.getElementById('deleteBtn');
  const selectAllCheckbox = document.getElementById('selectAll');
  const totalPriceInput = document.getElementById('totalPrice');
  const billForm = document.getElementById('billForm'); // your form element
  const warningDiv = document.getElementById('warningMessage'); // div to show warning

  function updateTotal() {
    let total = 0;
    itemsTableBody.querySelectorAll('tr').forEach(row => {
      const totalCell = row.querySelector('.totalCell');
      total += parseFloat(totalCell.textContent) || 0;
    });
    totalPriceInput.value = total.toFixed(2);
    return total;
  }

  function createRow() {
    const tr = document.createElement('tr');

    // Checkbox cell
    const selectCell = document.createElement('td');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    selectCell.appendChild(checkbox);
    tr.appendChild(selectCell);

    // Item No cell
    const itemNoCell = document.createElement('td');
    itemNoCell.textContent = itemsTableBody.children.length + 1;
    tr.appendChild(itemNoCell);

    // Item Name cell - dropdown
    const itemNameCell = document.createElement('td');
    const select = document.createElement('select');
    select.name = 'item';
    select.classList.add('form-select');
    select.innerHTML = `<option value="">Select item</option>`;
    itemsData.forEach(item => {
      select.innerHTML += `<option value="${item.id}" data-price="${item.price}">${item.name}</option>`;
    });
    itemNameCell.appendChild(select);
    tr.appendChild(itemNameCell);

    // Price cell - readonly input
    const priceCell = document.createElement('td');
    const priceInput = document.createElement('input');
    priceInput.type = 'number';
    priceInput.setAttribute('readonly', true);
    priceInput.classList.add('form-control', 'priceInput');
    priceInput.value = '0';
    priceCell.appendChild(priceInput);
    tr.appendChild(priceCell);

    // Quantity cell - editable input
    const qtyCell = document.createElement('td');
    const qtyInput = document.createElement('input');
    qtyInput.type = 'number';
    qtyInput.name = 'quantity';   
    qtyInput.classList.add('form-control', 'qtyInput');
    qtyInput.min = 1;
    qtyInput.value = 1;
    qtyCell.appendChild(qtyInput);
    tr.appendChild(qtyCell);

    // Total cell - readonly span
    const totalCell = document.createElement('td');
    totalCell.classList.add('totalCell');
    totalCell.textContent = '0';
    tr.appendChild(totalCell);

    // Update price & total on item change
    select.addEventListener('change', () => {
      const selectedOption = select.options[select.selectedIndex];
      const price = selectedOption ? parseFloat(selectedOption.getAttribute('data-price')) || 0 : 0;
      priceInput.value = price;
      updateRowTotal();
    });

    qtyInput.addEventListener('input', updateRowTotal);

    function updateRowTotal() {
      const price = parseFloat(priceInput.value) || 0;
      const quantity = parseInt(qtyInput.value) || 0;
      const rowTotal = price * quantity;
      totalCell.textContent = rowTotal.toFixed(2);
      updateTotal();
    }

    updateRowTotal();
    return tr;
  }

  addItemBtn.addEventListener('click', () => {
    const newRow = createRow();
    itemsTableBody.appendChild(newRow);
  });

  deleteBtn.addEventListener('click', () => {
    itemsTableBody.querySelectorAll('tr').forEach(row => {
      const checkbox = row.querySelector('input[type="checkbox"]');
      if (checkbox.checked) {
        row.remove();
      }
    });
    updateTotal();
  });

  selectAllCheckbox.addEventListener('change', (e) => {
    const checked = e.target.checked;
    itemsTableBody.querySelectorAll('input[type="checkbox"]').forEach(cb => {
      cb.checked = checked;
    });
  });

  // ----------------------
  // Form validation
  // ----------------------
  billForm.addEventListener('submit', (e) => {
    const total = updateTotal();
    const selectedItems = Array.from(itemsTableBody.querySelectorAll('tr')).filter(row => {
      const select = row.querySelector('select');
      return select && select.value !== '';
    });

    if (total <= 0 || selectedItems.length === 0) {
      e.preventDefault(); // stop form submission

      if (warningDiv) {
        warningDiv.textContent = 'Cannot generate bill: total is 0 or no items selected!';
        warningDiv.classList.remove('d-none');
      } else {
        alert('Cannot generate bill: total is 0 or no items selected!');
      }
    } else {
      if (warningDiv) warningDiv.classList.add('d-none');
    }
  });
});
