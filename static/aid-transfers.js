document.addEventListener('DOMContentLoaded', function() {
    const aidFeed = document.getElementById('aid-feed');

    // Format timestamps
    function formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString();
    }

    // Fetch and render aid transfer feed
    async function fetchAidTransfers() {
        try {
            const res = await fetch('/api/aid-transfers');
            if (!res.ok) throw new Error('Network response was not ok');
            const data = await res.json();
            aidFeed.innerHTML = '';
            data.forEach(transfer => {
                const feedItem = document.createElement('div');
                feedItem.className = 'aid-item';
                feedItem.innerHTML = `
                    <i class="fas fa-hand-holding-usd aid-icon"></i>
                    <div class="aid-details">
                        <div class="aid-title">Aid to ${transfer.wallet.slice(0, 6)}...${transfer.wallet.slice(-4)}</div>
                        <div class="aid-meta">Amount: $${transfer.amount} | Time: ${formatTimestamp(transfer.timestamp)}</div>
                    </div>
                    <span class="aid-level level-info">Tx: ${transfer.transaction_hash.slice(0, 10)}...</span>
                `;
                aidFeed.appendChild(feedItem);
            });
            // Scroll to the bottom to show the latest item
            aidFeed.scrollTop = aidFeed.scrollHeight;
        } catch (e) {
            console.error('fetchAidTransfers error', e);
            aidFeed.innerHTML = '<div class="text-center text-error-color">Failed to load aid transfers.</div>';
        }
    }

    // Initialize
    setInterval(fetchAidTransfers, 5000);
    fetchAidTransfers();
});