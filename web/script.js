// ForkMonkey Web Interface

// Initialize particles background
// Initialize particles background
particlesJS('particles-js', {
    particles: {
        number: { value: 40, density: { enable: true, value_area: 800 } },
        color: { value: '#00ff88' },
        shape: { type: 'circle' },
        opacity: {
            value: 0.2,
            random: true,
            anim: { enable: true, speed: 0.5, opacity_min: 0.05, sync: false }
        },
        size: {
            value: 2,
            random: true,
            anim: { enable: true, speed: 1, size_min: 0.1, sync: false }
        },
        line_linked: {
            enable: true,
            distance: 150,
            color: '#00ff88',
            opacity: 0.1,
            width: 1
        },
        move: {
            enable: true,
            speed: 0.5,
            direction: 'none',
            random: true,
            straight: false,
            out_mode: 'out',
            bounce: false
        }
    },
    interactivity: {
        detect_on: 'canvas',
        events: {
            onhover: { enable: true, mode: 'bubble' },
            onclick: { enable: true, mode: 'push' },
            resize: true
        },
        modes: {
            bubble: { distance: 200, size: 4, duration: 2, opacity: 0.4, speed: 3 },
            push: { particles_nb: 4 }
        }
    },
    retina_detect: true
});

// Rarity colors
const rarityColors = {
    common: '#00ff88',
    uncommon: '#ffd93d',
    rare: '#ff6b9d',
    legendary: '#ffd700'
};

// Load monkey data
async function loadMonkeyData() {
    try {
        // Show loading state
        document.body.classList.add('loading');
        
        // Determine base path - always use /monkey_data/ when served from root
        const basePath = '/monkey_data/';
        
        // Load DNA
        const dnaResponse = await fetch(basePath + 'dna.json');
        if (!dnaResponse.ok) throw new Error('DNA file not found');
        const dna = await dnaResponse.json();
        
        // Load stats
        const statsResponse = await fetch(basePath + 'stats.json');
        if (!statsResponse.ok) throw new Error('Stats file not found');
        const stats = await statsResponse.json();
        
        // Load history
        const historyResponse = await fetch(basePath + 'history.json');
        if (!historyResponse.ok) throw new Error('History file not found');
        const history = await historyResponse.json();
        
        // Load SVG
        const svgResponse = await fetch(basePath + 'monkey.svg');
        if (!svgResponse.ok) throw new Error('SVG file not found');
        const svgText = await svgResponse.text();
        
        // Update UI
        updateHeader(dna, stats);
        updateMonkeyDisplay(svgText, dna, stats);
        updateTraits(dna.traits);
        updateHistory(history.entries || []);
        
        // Remove loading state
        document.body.classList.remove('loading');
        
    } catch (error) {
        console.error('Error loading monkey data:', error);
        showError('Failed to load monkey data. Make sure you have initialized a monkey first!');
    }
}

// Update header stats
function updateHeader(dna, stats) {
    document.getElementById('generation').textContent = dna.generation || '1';
    document.getElementById('age').textContent = `${stats.age_days || 0}d`;
    document.getElementById('rarity').textContent = `${(stats.rarity_score || 0).toFixed(1)}%`;
}

// Update monkey display
function updateMonkeyDisplay(svgText, dna, stats) {
    const container = document.getElementById('monkey-svg');
    container.innerHTML = svgText;
    
    document.getElementById('dna-hash').textContent = dna.dna_hash || 'Unknown';
    document.getElementById('mutations').textContent = dna.mutation_count || '0';
    document.getElementById('parent').textContent = dna.parent_id || 'Genesis';
}

// Update traits grid
function updateTraits(traits) {
    const grid = document.getElementById('traits-grid');
    grid.innerHTML = '';
    
    // Sort traits by category
    const sortedTraits = Object.entries(traits).sort((a, b) => {
        return a[0].localeCompare(b[0]);
    });
    
    sortedTraits.forEach(([category, trait]) => {
        const card = createTraitCard(category, trait);
        grid.appendChild(card);
    });
}

// Create trait card
function createTraitCard(category, trait) {
    const card = document.createElement('div');
    card.className = `trait-card ${trait.rarity}`;
    
    // Format category name
    const formattedCategory = category
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
    
    // Format trait value
    const formattedValue = trait.value
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
    
    card.innerHTML = `
        <div class="trait-info">
            <div class="trait-category">${formattedCategory}</div>
            <div class="trait-value">${formattedValue}</div>
        </div>
        <div class="trait-rarity">${trait.rarity}</div>
    `;
    
    return card;
}

// Update history timeline
function updateHistory(entries) {
    const timeline = document.getElementById('history-timeline');
    const count = document.getElementById('history-count');
    
    count.textContent = entries.length;
    timeline.innerHTML = '';
    
    if (entries.length === 0) {
        timeline.innerHTML = `
            <div class="nes-container is-rounded">
                <p>No evolution history yet. Your monkey will evolve daily!</p>
            </div>
        `;
        return;
    }
    
    // Show most recent entries first
    const recentEntries = entries.slice().reverse().slice(0, 10);
    
    recentEntries.forEach(entry => {
        const historyEntry = createHistoryEntry(entry);
        timeline.appendChild(historyEntry);
    });
}

// Create history entry
function createHistoryEntry(entry) {
    const div = document.createElement('div');
    div.className = 'history-entry';
    
    // Format date
    const date = new Date(entry.timestamp);
    const formattedDate = date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    div.innerHTML = `
        <div class="history-date">${formattedDate}</div>
        <div class="history-content">
            <div class="history-story">${entry.story || 'Evolution occurred'}</div>
            <div class="history-stats">
                <span>Gen: ${entry.generation}</span>
                <span>•</span>
                <span>Mutations: ${entry.mutation_count}</span>
                <span>•</span>
                <span>Rarity: ${(entry.rarity_score || 0).toFixed(1)}%</span>
            </div>
        </div>
    `;
    
    return div;
}

// Download monkey SVG
function downloadMonkey() {
    const svgElement = document.querySelector('#monkey-svg svg');
    if (!svgElement) {
        alert('No monkey to download!');
        return;
    }
    
    const svgData = new XMLSerializer().serializeToString(svgElement);
    const blob = new Blob([svgData], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `forkmonkey-${Date.now()}.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Show error message
function showError(message) {
    const container = document.getElementById('monkey-svg');
    container.innerHTML = `
        <div class="nes-container is-rounded is-dark">
            <p style="color: #ff6b9d;">${message}</p>
            <br>
            <p style="font-size: 0.8rem;">Run: <code>python src/cli.py init</code></p>
        </div>
    `;
}

// Auto-refresh every 60 seconds
let autoRefreshInterval;

function startAutoRefresh() {
    autoRefreshInterval = setInterval(() => {
        loadMonkeyData();
    }, 60000); // 60 seconds
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // R key to refresh
    if (e.key === 'r' || e.key === 'R') {
        loadMonkeyData();
    }
    
    // D key to download
    if (e.key === 'd' || e.key === 'D') {
        downloadMonkey();
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadMonkeyData();
    startAutoRefresh();
    
    // Add visual feedback for loading
    console.log('%c🐵 ForkMonkey Web Interface Loaded!', 'color: #00ff88; font-size: 20px; font-weight: bold;');
    console.log('%cKeyboard shortcuts:', 'color: #ffd93d; font-weight: bold;');
    console.log('%c  R - Refresh data', 'color: #fff;');
    console.log('%c  D - Download SVG', 'color: #fff;');
});

// Handle page visibility (pause auto-refresh when tab is hidden)
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        stopAutoRefresh();
    } else {
        startAutoRefresh();
        loadMonkeyData();
    }
});

// Export functions for global access
window.loadMonkeyData = loadMonkeyData;
window.downloadMonkey = downloadMonkey;
