$(document).ready(function () {
    // DOM elements
    const screen1 = $('#screen1');
    const screen2 = $('#screen2');
    const loading = $('#loading');
    const medicalTextInput = $('#medical-text');
    const processBtn = $('#process-btn');
    const backBtn = $('#back-btn');
    const originalText = $('#original-text');
    const patientId = $('#patient-id');
    const patientTimeline = $('#patient-timeline');
    const analysisResults = $('#analysis-results');

    // Event listeners
    processBtn.on('click', processText);
    backBtn.on('click', goBackToInput);

    // Process text function
    function processText() {
        const text = medicalTextInput.val().trim();

        if (!text) {
            alert('Please enter some text before processing.');
            return;
        }

        // Show loading
        loading.removeClass('d-none');

        // Send data to backend
        $.ajax({
            url: '/api/process',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ text: text }),
            success: handleProcessSuccess,
            error: handleProcessError
        });
    }

    // Handle successful API response
    function handleProcessSuccess(response) {
        if (!response.success) {
            handleProcessError({ responseJSON: response });
            return;
        }

        try {
            // Parse the data from OpenAI
            const data = JSON.parse(response.data);

            // Display original text
            originalText.text(medicalTextInput.val().trim());

            // Extract patient ID if available
            if (data.patientID) {
                patientId.text(data.patientID);
            } else {
                patientId.text('Unknown');
            }

            // Generate timeline from dates
            generateTimeline(data);

            // Display analysis results
            displayResults(data);

            // Switch to screen 2
            screen1.addClass('d-none');
            screen2.removeClass('d-none');
        } catch (e) {
            console.error('Error parsing response:', e);
            alert('Error processing the response. Please try again.');
        }

        // Hide loading
        loading.addClass('d-none');
    }

    // Handle API error
    function handleProcessError(error) {
        console.error('API error:', error);
        let errorMessage = 'An error occurred while processing the text.';

        if (error.responseJSON && error.responseJSON.error) {
            errorMessage += ' ' + error.responseJSON.error;
        }

        alert(errorMessage);
        loading.addClass('d-none');
    }

    // Go back to input screen
    function goBackToInput() {
        screen2.addClass('d-none');
        screen1.removeClass('d-none');

        // Clear highlighted text
        $('.highlighted').removeClass('highlighted');
    }

    // Generate timeline from dates in the data
    function generateTimeline(data) {
        patientTimeline.empty();

        // Extract dates from the data
        let dates = [];
        if (data.dates) {
            dates = Array.isArray(data.dates) ? data.dates : [data.dates];
        } else {
            dates = [];
        }

        // Sort dates and create timeline events
        dates = [...new Set(dates)].sort(); // Remove duplicates and sort

        console.log('Dates found:', dates);

        if (dates.length === 0) {
            patientTimeline.html('<p>No dates found in the data</p>');
            return;
        }

        dates.forEach(date => {
            const event = $('<div class="timeline-event"></div>');
            event.html(`<div>${date}</div>`);
            patientTimeline.append(event);
        });
    }

    // Display analysis results
    function displayResults(data) {
        analysisResults.empty();

        // Function to recursively render JSON
        function renderJson(obj, parentKey = '') {
            for (const [key, value] of Object.entries(obj)) {
                const fullKey = parentKey ? `${parentKey}.${key}` : key;

                if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
                    // Create a section for nested objects
                    const section = $('<div class="nested-section mb-3"></div>');
                    section.append(`<h6 class="text-primary">${key}:</h6>`);
                    analysisResults.append(section);

                    // Recursive call for nested objects
                    renderJson(value, fullKey);
                } else {
                    // Skip position data in the display
                    if (key === 'position' || key === 'start' || key === 'end') {
                        continue;
                    }

                    const keyValuePair = $('<div class="key-value-pair"></div>');
                    keyValuePair.append(`<div class="key">${key}:</div>`);
                    keyValuePair.append(`<div class="value">${Array.isArray(value) ? value.join(', ') : value}</div>`);

                    // Store position data as attributes for highlighting
                    if (obj.position) {
                        keyValuePair.attr('data-start', obj.position.start);
                        keyValuePair.attr('data-end', obj.position.end);
                    }

                    // Add event handler for hovering
                    keyValuePair.on('mouseenter', highlightText);
                    keyValuePair.on('mouseleave', removeHighlight);

                    analysisResults.append(keyValuePair);
                }
            }
        }

        renderJson(data);
    }

    // Highlight text in the original content
    function highlightText() {
        const start = $(this).attr('data-start');
        const end = $(this).attr('data-end');

        if (start && end) {
            const text = originalText.text();
            const beforeHighlight = text.substring(0, start);
            const highlighted = text.substring(start, end);
            const afterHighlight = text.substring(end);

            originalText.html(
                escapeHtml(beforeHighlight) +
                '<span class="highlighted">' + escapeHtml(highlighted) + '</span>' +
                escapeHtml(afterHighlight)
            );
        }
    }

    // Remove highlight
    function removeHighlight() {
        originalText.text(originalText.text());
    }

    // Helper function to escape HTML
    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}); 