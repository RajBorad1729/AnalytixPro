document.addEventListener('DOMContentLoaded', () => {
    console.log("Dashboard Loaded");

    // Apply Filters Functionality
    const applyFilterButton = document.getElementById('apply-filters');
    if (applyFilterButton) {
        applyFilterButton.addEventListener('click', function () {
            const selectedFilters = {
                city: Array.from(document.querySelectorAll('input[name="city[]"]:checked')).map(el => el.value),
                region: Array.from(document.querySelectorAll('input[name="region[]"]:checked')).map(el => el.value),
                category: Array.from(document.querySelectorAll('input[name="category[]"]:checked')).map(el => el.value),
                year: Array.from(document.querySelectorAll('input[name="year"]:checked')).map(el => el.value),
            };

            const queryString = Object.keys(selectedFilters)
                .map(key => selectedFilters[key].map(value => `${key}=${encodeURIComponent(value)}`).join('&'))
                .filter(query => query.length > 0)
                .join('&');

            fetch(`/filter_data?${queryString}`)
                .then(response => {
                    if (!response.ok) throw new Error(`Failed to fetch filtered data. Status: ${response.status}`);
                    return response.text();
                })
                .then(updatedHTML => {
                    document.documentElement.innerHTML = updatedHTML;
                    console.log("Dashboard updated successfully.");
                })
                .catch(error => {
                    console.error('Error applying filters:', error);
                    // alert("An error occurred while applying filters. Please try again.");
                });
        });
    }

    // Reset Filters Functionality
    const resetButton = document.getElementById('reset-filters');
    if (resetButton) {
        resetButton.addEventListener('click', () => {
            document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                checkbox.checked = false;
            });
            document.querySelectorAll('input[type="radio"]').forEach(radio => {
                radio.checked = false;
            });
            localStorage.removeItem('checkboxState');
            window.location.href = '/reset_filters';
            console.log("Filters reset.");
        });
    }

    // Select All Functionality
    document.querySelectorAll('.select-all').forEach(selectAllCheckbox => {
        selectAllCheckbox.addEventListener('change', function () {
            const filterGroup = this.dataset.filterGroup;
            document.querySelectorAll(`input[name="${filterGroup}[]"]`).forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            console.log(`${filterGroup} - Select All toggled: ${this.checked}`);
        });
    });

    // Maintain checked state after reload
    document.querySelectorAll('input[type="checkbox"], input[type="radio"]').forEach(input => {
        input.addEventListener('change', () => {
            const checkedState = {};
            document.querySelectorAll('input[type="checkbox"], input[type="radio"]').forEach(el => {
                checkedState[el.id] = el.checked;
            });
            localStorage.setItem('checkboxState', JSON.stringify(checkedState));
        });
    });

    const savedState = JSON.parse(localStorage.getItem('checkboxState'));
    if (savedState) {
        Object.keys(savedState).forEach(id => {
            const input = document.getElementById(id);
            if (input) input.checked = savedState[id];
        });
    }

    // Predict Sales Button Functionality
    const predictSalesButton = document.getElementById('predict-sales');
    if (predictSalesButton) {
        predictSalesButton.addEventListener('click', () => {
            window.location.href = '/predict_sales';
            console.log("Navigated to Sales Prediction page.");
        });
    }

    // Drag & Drop File Upload Functionality
    const dragDropArea = document.getElementById('drag-drop-area');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const resetUploadButton = document.getElementById('reset-button');

    if (dragDropArea && fileInput) {
        dragDropArea.addEventListener('dragover', (event) => {
            event.preventDefault();
            dragDropArea.classList.add('drag-over');
        });

        dragDropArea.addEventListener('dragleave', () => {
            dragDropArea.classList.remove('drag-over');
        });

        dragDropArea.addEventListener('drop', (event) => {
            event.preventDefault();
            dragDropArea.classList.remove('drag-over');
            if (event.dataTransfer.files.length > 0) {
                fileInput.files = event.dataTransfer.files;
                fileInfo.textContent = `File: ${event.dataTransfer.files[0].name} - Ready to upload`;
            }
        });

        dragDropArea.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                fileInfo.textContent = `File: ${fileInput.files[0].name} - Ready to upload`;
            }
        });
    }

    if (resetUploadButton) {
        resetUploadButton.addEventListener('click', () => {
            fileInput.value = '';
            fileInfo.textContent = '';
            dragDropArea.textContent = 'Drag & Drop your file here or click to browse';
        });
    }

    // Clear local storage on form submit
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', () => {
            localStorage.removeItem('checkboxState');
        });
    }
});