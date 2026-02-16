// Main JavaScript for MedConnect

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-info):not(.alert-warning):not(.ai-result)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Appointment date validation (prevent past dates) - exclude DOB
    const dateInputs = document.querySelectorAll('input[type="date"]:not([name*="birth"])');
    dateInputs.forEach(input => {
        const today = new Date().toISOString().split('T')[0];
        input.setAttribute('min', today);
    });
});

// Notification handler
function markNotificationRead(notificationId) {
    fetch(`/notifications/${notificationId}/mark-read/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`notification-${notificationId}`).remove();
        }
    });
}

// Get CSRF token for AJAX requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Symptom Checker AI interaction
function analyzeSymptoms() {
    const symptoms = document.getElementById('symptoms-input').value;
    const resultDiv = document.getElementById('ai-result');
    
    if (symptoms.trim() === '') {
        alert('Please enter your symptoms');
        return;
    }
    
    resultDiv.innerHTML = '<div class="spinner-border text-primary" role="status"></div><p>Analyzing your symptoms...</p>';
    
    // Simulate AI processing
    setTimeout(() => {
        resultDiv.innerHTML = `
            <div class="alert alert-info">
                <h5>AI Analysis Results</h5>
                <p>Based on your symptoms, we recommend consulting with a specialist.</p>
                <button class="btn btn-primary" onclick="bookAppointment()">Book Appointment</button>
            </div>
        `;
    }, 2000);
}

function bookAppointment() {
    window.location.href = '/appointments/book/';
}

// Department filter
function filterDepartment(specialty) {
    const doctors = document.querySelectorAll('.doctor-card');
    doctors.forEach(doctor => {
        if (specialty === 'all' || doctor.dataset.specialty === specialty) {
            doctor.style.display = 'block';
        } else {
            doctor.style.display = 'none';
        }
    });
}

// Chart initialization for analytics
function initAnalyticsCharts() {
    if (typeof Chart !== 'undefined') {
        // Appointments Chart
        const appointmentCtx = document.getElementById('appointmentsChart');
        if (appointmentCtx) {
            new Chart(appointmentCtx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Appointments',
                        data: [12, 19, 15, 25, 22, 30],
                        borderColor: '#4A90E2',
                        tension: 0.4
                    }]
                }
            });
        }
    }
}

// Call init function
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAnalyticsCharts);
} else {
    initAnalyticsCharts();
}
