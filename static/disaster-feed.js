document.addEventListener('DOMContentLoaded', function() {
    const disasterFeed = document.getElementById('disaster-feed');

    // Format timestamps
    function formatTimestamp(timestamp) {
        const date = new Date(timestamp * 1000);
        return date.toLocaleString();
    }

    // Fetch and render disaster feed
    async function fetchDisasterFeed() {
        try {
            const res = await fetch('/alerts');
            if (!res.ok) throw new Error('Network response was not ok');
            const data = await res.json();
            disasterFeed.innerHTML = '';
            data.forEach(alert => {
                const icon = alert.disaster.toLowerCase().includes('flood') ? 'fa-water' :
                            alert.disaster.toLowerCase().includes('earthquake') ? 'fa-mountain' :
                            alert.disaster.toLowerCase().includes('fire') ? 'fa-fire' : 'fa-exclamation-triangle';
                const levelClass = alert.level >= 7 ? 'level-critical' :
                                 alert.level >= 5 ? 'level-warning' : 'level-info';
                const levelText = alert.level >= 7 ? 'Critical' :
                                 alert.level >= 5 ? 'Warning' : 'Info';

                const feedItem = document.createElement('div');
                feedItem.className = 'disaster-item';
                feedItem.innerHTML = `
                    <i class="fas ${icon} disaster-icon"></i>
                    <div class="disaster-details">
                        <div class="disaster-title">${alert.disaster.toUpperCase()} at ${alert.location}</div>
                        <div class="disaster-meta">${formatTimestamp(alert.timestamp)}</div>
                    </div>
                    <span class="disaster-level ${levelClass}">Lvl ${alert.level} (${levelText})</span>
                `;
                disasterFeed.appendChild(feedItem);
            });
            // Scroll to the bottom to show the latest item
            disasterFeed.scrollTop = disasterFeed.scrollHeight;
        } catch (e) {
            console.error('fetchDisasterFeed error', e);
            disasterFeed.innerHTML = '<div class="text-center text-error-color">Failed to load disaster feed.</div>';
        }
    }

    // Initialize
    setInterval(fetchDisasterFeed, 5000);
    fetchDisasterFeed();
});