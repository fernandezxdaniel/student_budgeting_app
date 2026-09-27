function updateExpense(category) {
  let amount = document.getElementById(category).value;
  fetch('/update', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({category: category, amount: amount})
  })
  .then(res => res.json())
  .then(data => alert(data.message));
}


