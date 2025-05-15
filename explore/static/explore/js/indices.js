async function fetchIndices() {
    const response = await fetch("/explore/api/index-data/");
    const data = await response.json();
    const tbody = document.getElementById('index-body');
    tbody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');

        // Кольори для зміни (вручну, бо API не дає напрямку)
        const closeClass = getColorClass(item.close, item.open);

        row.innerHTML = `
            <td>${item.symbol}</td>
            <td>${item.name || '-'}</td>
            <td>${item.exchange || '-'}</td>
            <td>${item.quote_type || '-'}</td>
            <td>${item.market_cap?.toLocaleString() || '-'}</td>
            <td>${item.open.toFixed(2)}</td>
            <td>${item.high.toFixed(2)}</td>
            <td>${item.low.toFixed(2)}</td>
            <td class="${closeClass}">${item.close.toFixed(2)}</td>
            <td>${item.volume?.toLocaleString() || '-'}</td>
        `;
        tbody.appendChild(row);
    });
}

function getColorClass(close, open) {
    if (close > open) return 'positive';
    else if (close < open) return 'negative';
    return 'neutral';
}

fetchIndices();
setInterval(fetchIndices, 30000);
