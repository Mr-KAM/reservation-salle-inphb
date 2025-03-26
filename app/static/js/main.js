// Main JavaScript file for Room Reservation System

document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.getElementById('html-element');

    // Check if theme preference is stored in localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        htmlElement.setAttribute('data-theme', savedTheme);
        themeToggle.checked = savedTheme === 'dark';
    }

    // Toggle theme when the switch is clicked
    themeToggle.addEventListener('change', function() {
        const newTheme = this.checked ? 'dark' : 'light';
        htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
    // Initialize all dropdowns
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('[tabindex="0"]');
        const content = dropdown.querySelector('.dropdown-content');

        if (trigger && content) {
            // Close dropdown when clicking outside
            document.addEventListener('click', function(event) {
                if (!dropdown.contains(event.target)) {
                    content.classList.remove('dropdown-open');
                    trigger.setAttribute('aria-expanded', 'false');
                }
            });
        }
    });

    // Flash message auto-dismiss
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        // Add dismiss button if not present
        if (!message.querySelector('.btn-close')) {
            const dismissBtn = document.createElement('button');
            dismissBtn.className = 'btn btn-sm btn-circle btn-ghost absolute right-2 top-2';
            dismissBtn.innerHTML = '✕';
            dismissBtn.addEventListener('click', () => {
                message.remove();
            });
            message.appendChild(dismissBtn);
        }

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            message.classList.add('opacity-0');
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Date picker enhancement
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        // Set min date to today
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        input.min = `${yyyy}-${mm}-${dd}`;
    });

    // Time picker validation
    const startTimeInputs = document.querySelectorAll('input[name="start_time"]');
    const endTimeInputs = document.querySelectorAll('input[name="end_time"]');

    if (startTimeInputs.length > 0 && endTimeInputs.length > 0) {
        startTimeInputs.forEach((startInput, index) => {
            const endInput = endTimeInputs[index];

            startInput.addEventListener('change', () => {
                if (startInput.value && endInput.value) {
                    const startTime = startInput.value;
                    const endTime = endInput.value;

                    if (startTime >= endTime) {
                        endInput.setCustomValidity('End time must be after start time');
                    } else {
                        endInput.setCustomValidity('');
                    }
                }
            });

            endInput.addEventListener('change', () => {
                if (startInput.value && endInput.value) {
                    const startTime = startInput.value;
                    const endTime = endInput.value;

                    if (startTime >= endTime) {
                        endInput.setCustomValidity('End time must be after start time');
                    } else {
                        endInput.setCustomValidity('');
                    }
                }
            });
        });
    }

    // Add responsive table support
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        if (!table.classList.contains('table-responsive') && table.parentElement.classList.contains('overflow-x-auto')) {
            table.classList.add('table-responsive');
        }
    });
});
