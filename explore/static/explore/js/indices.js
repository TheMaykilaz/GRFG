async function fetchIndices() {
    try {
        const response = await fetch("/explore/api/index-data/");
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        const tbody = document.getElementById('index-body');
        tbody.innerHTML = '';

        data.forEach(item => {
            const row = document.createElement('tr');
            row.style.cursor = 'pointer';
            row.addEventListener('click', () => {
                window.location.href = `/explore/index/${item.symbol}/`;
            });

            // Кольори для зміни
            const closeClass = getColorClass(item.close, item.open);
            const changePercent = calculateChangePercent(item.close, item.open);

            row.innerHTML = `
                <td>${item.symbol}</td>
                <td>${item.name || '-'}</td>
                <td>${item.exchange || '-'}</td>
                <td>${item.quote_type || '-'}</td>
                <td>${item.market_cap ? formatNumber(item.market_cap) : '-'}</td>
                <td>${item.open.toFixed(2)}</td>
                <td>${item.high.toFixed(2)}</td>
                <td>${item.low.toFixed(2)}</td>
                <td class="${closeClass}">${item.close.toFixed(2)}</td>
                <td class="${closeClass}">${changePercent}%</td>
                <td>${item.volume ? formatNumber(item.volume) : '-'}</td>
            `;
            tbody.appendChild(row);
        });

        // Додаємо обробник подвійного кліку (якщо потрібно)
        tbody.querySelectorAll('tr').forEach(row => {
            row.addEventListener('dblclick', (e) => {
                e.stopPropagation();
                const symbol = row.cells[0].textContent;
                window.open(`/explore/index/${symbol}/`, '_blank');
            });
        });

    } catch (error) {
        console.error('Error fetching indices:', error);
        document.getElementById('index-body').innerHTML = `
            <tr>
                <td colspan="11" class="error-message">Failed to load data. Please try again later.</td>
            </tr>
        `;
    }
}

// Допоміжні функції
function getColorClass(close, open) {
    if (close > open) return 'positive';
    if (close < open) return 'negative';
    return 'neutral';
}

function calculateChangePercent(close, open) {
    if (open === 0) return '0.00';
    return (((close - open) / open) * 100).toFixed(2);
}

function formatNumber(num) {
    return num.toLocaleString('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    });
}

// Ініціалізація та оновлення кожні 30 секунд
document.addEventListener('DOMContentLoaded', () => {
    fetchIndices();
    setInterval(fetchIndices, 30000);
    
    // Додаємо обробник для кнопки оновлення (якщо є)
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', fetchIndices);
    }
});