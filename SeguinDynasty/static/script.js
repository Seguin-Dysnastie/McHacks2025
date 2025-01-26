document.addEventListener('DOMContentLoaded', () => {

  // ------------------------------
  // CHART BUILDING
  // ------------------------------
  console.log("graphData:", graphData);
  const historicalDataPoints = graphData[0]
  const realDataPoints = graphData[1]
  const predDataPoints = graphData[2]
  const extremumPredDataPoints = graphData[4]

  const ctx = document.getElementById('stockGraph').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      datasets: [
        {
          label: 'Historical Stock Prices',
          data: historicalDataPoints,
          borderColor: 'green',
          borderWidth: 2,
          tension: 0.3,
          pointRadius: 3
        },
        {
          label: 'Real Stock Prices',
          data: realDataPoints,
          borderColor: 'blue',
          borderWidth: 2,
          tension: 0.3,
          pointRadius: 3
        },
        {
          label: 'Predicted Stock Prices',
          data: predDataPoints,
          borderColor: 'red',
          borderWidth: 2,
          tension: 0.3,
          pointRadius: 3
        },
        {
          label: 'Prediction Extremums',
          data: extremumPredDataPoints,
          borderColor: 'lightgray',
          borderWidth: 2,
          tension: 0.3,
          pointRadius: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          type: 'time',
          time: {
            parser: 'YYYY-MM-DD',
            unit: 'month'
          },
          title: {
            display: true,
            text: 'Date by month',
            align: 'end' // Aligns the title to the far left
          }
        },
        y: {
          title: {
            display: true,
            text: 'Stock Price ($USD)'
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: `Stock Chart for ${graphData[3][1] || 'N/A'} (${graphData[3][0] || 'N/A'}) - $${graphData[1][0][1] || 'N/A'}`
        }
      }
    }
  });


  // ------------------------------
  // SEARCH HISTORY LOGIC
  // ------------------------------
  const searchForm = document.getElementById('searchForm');
  const searchInput = document.getElementById('searchInput');
  const dataList = document.getElementById('searchHistoryList');

  // 1) Load existing history from localStorage (or empty array if none)
  let history = JSON.parse(localStorage.getItem('searchHistory')) || [];

  // 2) Function to refresh the datalist options
  function updateDataList() {
    // Clear out old <option> elements
    dataList.innerHTML = '';

    // Add each item in history as <option>
    history.forEach(item => {
      const option = document.createElement('option');
      option.value = item;
      dataList.appendChild(option);
    });
  }

  // Populate the datalist on page load
  updateDataList();

  // 3) On search form submit, update history
  searchForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const symbol = searchInput.value.trim();
    if (!symbol) return;

    // Remove existing occurrence of symbol (so we can move it to the front)
    history = history.filter(item => item !== symbol);
    // Add to front
    history.unshift(symbol);

    // Limit the history to 10 entries
    if (history.length > 10) {
      history.pop();
    }

    // Save to localStorage
    localStorage.setItem('searchHistory', JSON.stringify(history));

    // Refresh the datalist
    updateDataList();

    // TODO: fetch new data for 'symbol' if desired
    console.log("User searched for:", symbol);
  });

});
