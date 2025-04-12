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
                patientId.text('Lukáš Novák');
            }

            // Generate timeline from dates
            generateTimeline(data);

            // Add missing required fields to the data object
            if (response.missing_required_fields && response.missing_required_fields.length > 0) {
                data.missing_required_fields = response.missing_required_fields;
            }

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

        // Extract dates and their keys from the data
        let dateEntries = [];
        if (data.dates) {
            if (typeof data.dates === 'object' && !Array.isArray(data.dates)) {
                // Extract both keys and values from the dates object
                dateEntries = Object.entries(data.dates)
                    .filter(([_, value]) => typeof value === 'string' && value)
                    .map(([key, value]) => ({ key, date: value }));
            } else if (Array.isArray(data.dates)) {
                dateEntries = data.dates.map(date => ({ key: '', date }));
            }
        }

        // Sort dates and create timeline events
        dateEntries.sort((a, b) => a.date.localeCompare(b.date));

        if (dateEntries.length === 0) {
            patientTimeline.html('<p>No dates found in the data</p>');
            return;
        }

        // For horizontal timeline, calculate positions
        const totalDates = dateEntries.length;

        dateEntries.forEach((entry, index) => {
            const event = $('<div class="timeline-event"></div>');
            event.html(`
                <div class="date">${entry.date}</div>
                <div class="event-key">${entry.key}</div>
            `);

            // Calculate position percentage for more precise placement
            if (totalDates > 1) {
                // Special handling for first and last elements to avoid overflow
                if (index === 0) {
                    // First element should align to left
                    event.addClass('first-event');
                    event.css({
                        'position': 'absolute',
                        'left': '0',
                        'transform': 'translateX(0)',
                    });
                } else if (index === totalDates - 1) {
                    // Last element should align to right
                    event.addClass('last-event');
                    event.css({
                        'position': 'absolute',
                        'right': '0',
                        'left': 'auto',
                        'transform': 'none',
                    });
                } else {
                    // Middle elements use percentage-based positioning
                    // Adjust range to be between 5% and 95% to avoid edges
                    const position = 5 + (index / (totalDates - 1) * 90);
                    event.css({
                        'position': 'absolute',
                        'left': `${position}%`,
                        'transform': 'translateX(-50%)',
                    });
                }
            }

            patientTimeline.append(event);
        });
    }

    // Display analysis results
    function displayResults(data) {
        analysisResults.empty();

        const missingRequiredFields = new Set();
        if (data.missing_required_fields && data.missing_required_fields.length > 0) {
            // Add each missing field to the set for quick checks later
            data.missing_required_fields.forEach(field => {
                missingRequiredFields.add(field);
            });
        }

        delete data.missing_required_fields;

        // Function to recursively render JSON
        function renderJson(obj, level = 0, parentKey = '') {
            // Create a container for this level with proper indentation
            const container = $('<div class="json-level"></div>').css('margin-left', `${level * 10}px`);

            if (level > 0) {
                container.addClass('nested-container');
            }

            // For arrays, handle differently
            if (Array.isArray(obj)) {
                obj.forEach((item, index) => {
                    if (typeof item === 'object' && item !== null) {
                        const arrayItemSection = $('<div class="array-item mb-2"></div>');
                        arrayItemSection.append(`<h6 class="text-secondary">[${index}]</h6>`);
                        container.append(arrayItemSection);
                        arrayItemSection.append(renderJson(item, level + 1));
                    } else {
                        container.append(`<div class="array-item">[${index}]: ${item}</div>`);
                    }
                });
                return container;
            }

            // For objects
            for (const [key, value] of Object.entries(obj)) {
                const fullKey = parentKey ? `${parentKey}.${key}` : key;

                // Skip position objects in display
                if (key === 'position') {
                    continue;
                }

                if (value !== null && typeof value === 'object') {
                    // Create a section for nested objects/arrays
                    const sectionHeader = $('<div class="section-header"></div>');
                    const sectionTitle = $(`<h6 class="text-primary object-key">${key}:</h6>`);

                    // Add toggle functionality
                    sectionTitle.css('cursor', 'pointer');
                    const toggleIcon = $('<span class="toggle-icon">▼</span>');
                    sectionTitle.prepend(toggleIcon);

                    sectionHeader.append(sectionTitle);
                    container.append(sectionHeader);

                    // Create content section that can be toggled
                    const contentSection = $('<div class="section-content"></div>');
                    contentSection.append(renderJson(value, level + 1, fullKey));
                    container.append(contentSection);

                    // Add click handler for toggling
                    sectionTitle.on('click', function () {
                        contentSection.toggle();
                        toggleIcon.text(contentSection.is(':visible') ? '▼' : '►');
                    });
                } else {
                    // Skip additional position-related fields
                    if (key === 'start' || key === 'end') {
                        continue;
                    }

                    const keyValuePair = $('<div class="key-value-pair"></div>');
                    keyValuePair.append(`<div class="key">${key}:</div>`);
                    keyValuePair.append(`<div class="value">${Array.isArray(value) ? JSON.stringify(value) : value}</div>`);

                    // Add pastel yellow background for null values
                    if (value === null || value === "null") {
                        keyValuePair.addClass('null-value');

                        // Check if this is a required field that is missing
                        if (missingRequiredFields.has(fullKey)) {
                            // Override with the required field style (red background)
                            keyValuePair.removeClass('null-value');
                            keyValuePair.addClass('null-value-required');
                        } else {
                            // Also check if this field matches any part of a missing field path
                            // This helps when the paths might be formatted differently
                            for (const missingField of missingRequiredFields) {
                                // Check if the fullKey is part of a missing field path or vice versa
                                if (missingField.includes(fullKey) || fullKey.includes(missingField)) {
                                    keyValuePair.removeClass('null-value');
                                    keyValuePair.addClass('null-value-required');
                                    break;
                                }
                            }
                        }
                    }

                    // Store position data as attributes for highlighting
                    if (obj.position) {
                        keyValuePair.attr('data-start', obj.position.start);
                        keyValuePair.attr('data-end', obj.position.end);
                    }

                    // Add event handlers for hovering
                    keyValuePair.on('mouseenter', highlightText);
                    keyValuePair.on('mouseleave', removeHighlight);

                    container.append(keyValuePair);
                }
            }

            return container;
        }

        // Render the JSON and append to results container
        analysisResults.append(renderJson(data));

        // Add some CSS for better visualization
        $('<style>')
            .text(`
                .json-level { border-left: 1px dashed #ddd; padding-left: 10px; margin-bottom: 5px; }
                .nested-container { margin-top: 5px; }
                .section-header { margin-top: 10px; }
                .key-value-pair { margin: 3px 0; display: flex; position: relative; padding-right: 70px; min-height: 24px; }
                .key { font-weight: bold; margin-right: 5px; }
                .toggle-icon { margin-right: 5px; }
                .array-item { margin: 2px 0; }
            `)
            .appendTo('head');
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