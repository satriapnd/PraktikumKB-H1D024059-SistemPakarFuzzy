document.addEventListener('DOMContentLoaded', () => {
    
    // --- FUZZY LOGIC PAGE ---
    const fuzzyForm = document.getElementById('fuzzyForm');
    if (fuzzyForm) {
        fuzzyForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // UI State
            const btn = document.getElementById('btnFuzzy');
            const loader = document.getElementById('fuzzyLoader');
            btn.disabled = true;
            loader.classList.remove('d-none');
            
            // Collect Data
            const payload = {
                lvr: parseFloat(document.getElementById('lvr').value),
                cvr: parseFloat(document.getElementById('cvr').value),
                arr: parseFloat(document.getElementById('arr').value),
                sharing: parseFloat(document.getElementById('sharing').value)
            };
            
            try {
                const response = await fetch('/api/fuzzy', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Display Results
                    document.getElementById('fuzzyInitialState').classList.add('d-none');
                    document.getElementById('fuzzyResultBox').classList.remove('d-none');
                    
                    // Animate Score
                    animateValue("loyaltyScore", 0, data.score, 1500);
                    
                    const statusEl = document.getElementById('loyaltyStatus');
                    statusEl.innerText = data.status;
                    
                    // Change Background based on Status
                    const panel = document.querySelector('.result-panel');
                    if (data.status === 'Militan') {
                        panel.style.background = 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)';
                        statusEl.className = 'fw-bold mb-4 px-4 py-2 rounded-pill d-inline-block bg-white text-danger';
                    } else if (data.status === 'Aktif') {
                        panel.style.background = 'linear-gradient(135deg, #10b981 0%, #047857 100%)';
                        statusEl.className = 'fw-bold mb-4 px-4 py-2 rounded-pill d-inline-block bg-white text-success';
                    } else {
                        panel.style.background = 'linear-gradient(135deg, #6b7280 0%, #374151 100%)';
                        statusEl.className = 'fw-bold mb-4 px-4 py-2 rounded-pill d-inline-block bg-white text-secondary';
                    }
                    
                    // Save to SessionStorage for Expert Page
                    sessionStorage.setItem('fluen_loyalty_status', data.status);
                    
                } else {
                    alert("Terjadi kesalahan: " + data.error);
                }
            } catch (error) {
                console.error(error);
                alert("Gagal terhubung ke server.");
            } finally {
                btn.disabled = false;
                loader.classList.add('d-none');
            }
        });
    }
    
    // --- EXPERT SYSTEM PAGE ---
    const expertForm = document.getElementById('expertForm');
    if (expertForm) {
        // Check if there is data from Fuzzy
        const savedStatus = sessionStorage.getItem('fluen_loyalty_status');
        if (savedStatus) {
            const select = document.getElementById('loyalty_status');
            for(let i=0; i<select.options.length; i++) {
                if(select.options[i].value === savedStatus) {
                    select.selectedIndex = i;
                    break;
                }
            }
        }
        
        expertForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // UI State
            const btn = document.getElementById('btnExpert');
            const loader = document.getElementById('expertLoader');
            btn.disabled = true;
            loader.classList.remove('d-none');
            
            // Collect Data
            const payload = {
                loyalty_status: document.getElementById('loyalty_status').value,
                category: document.getElementById('category').value,
                subscriber_tier: document.getElementById('subscriber_tier').value,
                violation_history: document.querySelector('input[name="violation_history"]:checked').value,
                age_demo: document.getElementById('age_demo').value,
                upload_freq: document.getElementById('upload_freq').value
            };
            
            try {
                const response = await fetch('/api/expert', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Display Results
                    document.getElementById('expertInitialState').classList.add('d-none');
                    document.getElementById('expertResultBox').classList.remove('d-none');
                    
                    const statusEl = document.getElementById('finalStatus');
                    const statusBox = document.getElementById('statusBox');
                    statusEl.innerText = data.status;
                    
                    // Styling based on Status
                    statusBox.className = 'mb-4 p-3 bg-dark bg-opacity-25 rounded-3 border-start border-4';
                    if (data.status === 'Sangat Layak') {
                        statusBox.classList.add('border-success');
                        statusEl.className = 'fw-bold mb-0 text-success';
                    } else if (data.status === 'Pertimbangkan') {
                        statusBox.classList.add('border-warning');
                        statusEl.className = 'fw-bold mb-0 text-warning';
                    } else {
                        statusBox.classList.add('border-danger');
                        statusEl.className = 'fw-bold mb-0 text-danger';
                    }
                    
                    document.getElementById('finalRecommendation').innerText = data.recommendation;
                    document.getElementById('finalValue').innerText = data.formatted_value;
                    
                } else {
                    alert("Terjadi kesalahan: " + data.error);
                }
            } catch (error) {
                console.error(error);
                alert("Gagal terhubung ke server.");
            } finally {
                btn.disabled = false;
                loader.classList.add('d-none');
            }
        });
    }
});

// Helper for animating numbers
function animateValue(id, start, end, duration) {
    if (start === end) return;
    const obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = (progress * (end - start) + start).toFixed(2);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// CTA Navigation
function proceedToExpert() {
    window.location.href = '/expert';
}
