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

            // Display original text with line breaks preserved
            const formattedText = medicalTextInput.val().trim().replace(/\n/g, '<br>');
            originalText.html(formattedText);

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
                // Extract both keys and values from the dates object, filtering out null values
                dateEntries = Object.entries(data.dates)
                    .filter(([_, value]) => typeof value === 'string' && value && value.toLowerCase() !== 'null')
                    .map(([key, value]) => ({ key, date: value }));
            } else if (Array.isArray(data.dates)) {
                dateEntries = data.dates
                    .filter(date => date && date.toLowerCase() !== 'null')
                    .map(date => ({ key: '', date }));
            }
        }

        // Sort dates and create timeline events
        dateEntries.sort((a, b) => a.date.localeCompare(b.date));

        if (dateEntries.length === 0) {
            patientTimeline.html('<p>No dates found in the data</p>');
            return;
        }

        // Format date from YYYY-MM-DD to DD.m.YYYY (without leading zeroes in day and month)
        function formatDate(dateStr) {
            if (!dateStr || typeof dateStr !== 'string') return dateStr;

            // Check if date is in YYYY-MM-DD format
            const dateMatch = dateStr.match(/^(\d{4})-(\d{2})-(\d{2})$/);
            if (dateMatch) {
                const [_, year, month, day] = dateMatch;
                // Remove leading zeroes from both day and month
                const dayWithoutZero = day.replace(/^0+/, '');
                const monthWithoutZero = month.replace(/^0+/, '');
                return `${dayWithoutZero}.${monthWithoutZero}.${year}`;
            }

            return dateStr;
        }

        // For horizontal timeline, calculate positions
        const totalDates = dateEntries.length;

        dateEntries.forEach((entry, index) => {
            const event = $('<div class="timeline-event"></div>');
            event.html(`
                <div class="date">${formatDate(entry.date)}</div>
                <div class="event-key">${entry.key}</div>
            `);

            // Add click event listener to the date element
            event.on('click', function (e) {
                // e.stopPropagation();
                searchAndHighlightText(formatDate(entry.date));
                console.log(entry.date);
            });

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

        // Variables to track null values
        let nullValueCount = 0;
        let nullRequiredValueCount = 0;

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
                        nullValueCount++;

                        // Make the value div editable
                        const valueDiv = keyValuePair.find('.value');
                        valueDiv.attr('contenteditable', 'true');
                        valueDiv.attr('data-original-value', 'null');

                        // Add click handler to clear the null value when clicked
                        valueDiv.on('click', function (e) {
                            // Only clear if the content is null
                            if ($(this).text().trim() === "null") {
                                $(this).text('');
                                // Set focus back to the element
                                $(this).focus();
                            }
                            // Stop event propagation to prevent parent click handlers
                            e.stopPropagation();
                        });

                        // Add keydown handler to save value on Enter
                        valueDiv.on('keydown', function (e) {
                            // If Enter key is pressed
                            if (e.which === 13 || e.keyCode === 13) {
                                e.preventDefault(); // Prevent default behavior (new line)
                                $(this).blur(); // Trigger blur event which saves the value
                            }
                        });

                        // Add input change handler
                        valueDiv.on('blur', function () {
                            const newValue = $(this).text().trim();
                            const keyValuePairElement = $(this).closest('.key-value-pair');

                            // Check if the input is still null/empty
                            if (newValue === "" || newValue === "null") {
                                // If this is a required field
                                if (keyValuePairElement.hasClass('null-value-required')) {
                                    // Keep the required field styling
                                    $(this).removeClass('valid-input');
                                } else {
                                    // For optional fields, keep the null-value class
                                    keyValuePairElement.addClass('null-value');
                                    $(this).removeClass('valid-input');
                                }
                            } else {
                                // Remove both null-value classes and add valid-input class
                                keyValuePairElement.removeClass('null-value');
                                keyValuePairElement.removeClass('null-value-required');
                                $(this).addClass('valid-input');
                            }
                        });

                        // Check if this is a required field that is missing
                        if (missingRequiredFields.has(fullKey)) {
                            // Override with the required field style (red background)
                            keyValuePair.removeClass('null-value');
                            keyValuePair.addClass('null-value-required');
                            nullRequiredValueCount++;

                            // Make the value div editable for required fields too
                            const valueDiv = keyValuePair.find('.value');
                            valueDiv.attr('contenteditable', 'true');
                            valueDiv.attr('data-original-value', 'null');

                            // Add click handler to clear the null value when clicked
                            valueDiv.on('click', function (e) {
                                // Only clear if the content is null
                                if ($(this).text().trim() === "null") {
                                    $(this).text('');
                                    // Set focus back to the element
                                    $(this).focus();
                                }
                                // Stop event propagation to prevent parent click handlers
                                e.stopPropagation();
                            });

                            // Add keydown handler to save value on Enter
                            valueDiv.on('keydown', function (e) {
                                // If Enter key is pressed
                                if (e.which === 13 || e.keyCode === 13) {
                                    e.preventDefault(); // Prevent default behavior (new line)
                                    $(this).blur(); // Trigger blur event which saves the value
                                }
                            });

                            // Add Validovat button
                            const validateButton = $('<button class="validate-btn">Validovat</button>');
                            keyValuePair.append(validateButton);

                            // Add click handler for validation button
                            validateButton.on('click', function (e) {
                                e.stopPropagation(); // Prevent triggering the parent click handler

                                // Check if there's already an output element
                                let outputElement = $(this).closest('.key-value-pair').next('.validation-output');
                                if (!outputElement.length) {
                                    // Create new output element if it doesn't exist
                                    outputElement = $('<div class="validation-output" style="margin-left: 20px; margin-top: 5px;"></div>');
                                    $(this).closest('.key-value-pair').after(outputElement);
                                }

                                // Show the element and start generating text
                                outputElement.show();
                                outputElement.html('<div class="generating"><i class="spinner-border spinner-border-sm"></i> Generování validace...</div>');

                                // Get the field name and original medical text
                                const fieldName = $(this).closest('.key-value-pair').find('.key').text().replace(':', '');
                                const originalMedicalText = medicalTextInput.val().trim();

                                // Call the validation API
                                $.ajax({
                                    url: '/api/validate',
                                    type: 'POST',
                                    contentType: 'application/json',
                                    data: JSON.stringify({
                                        text: originalMedicalText,
                                        field: fieldName
                                    }),
                                    success: function (response) {
                                        if (response.success) {
                                            outputElement.html(response.suggestion);
                                        } else {
                                            outputElement.html('Chyba validace: ' + (response.error || 'Neznámá chyba'));
                                        }
                                    },
                                    error: function (error) {
                                        outputElement.html('Chyba validace: ' + (error.responseJSON?.error || 'Neznámá chyba'));
                                    }
                                });
                            });
                        } else {
                            // Also check if this field matches any part of a missing field path
                            // This helps when the paths might be formatted differently
                            for (const missingField of missingRequiredFields) {
                                // Check if the fullKey is part of a missing field path or vice versa
                                if (missingField.includes(fullKey) || fullKey.includes(missingField)) {
                                    keyValuePair.removeClass('null-value');
                                    keyValuePair.addClass('null-value-required');
                                    nullRequiredValueCount++;

                                    // Make the value div editable for required fields too
                                    const valueDiv = keyValuePair.find('.value');
                                    valueDiv.attr('contenteditable', 'true');
                                    valueDiv.attr('data-original-value', 'null');

                                    // Add click handler to clear the null value when clicked
                                    valueDiv.on('click', function (e) {
                                        // Only clear if the content is null
                                        if ($(this).text().trim() === "null") {
                                            $(this).text('');
                                            // Set focus back to the element
                                            $(this).focus();
                                        }
                                        // Stop event propagation to prevent parent click handlers
                                        e.stopPropagation();
                                    });

                                    // Add keydown handler to save value on Enter
                                    valueDiv.on('keydown', function (e) {
                                        // If Enter key is pressed
                                        if (e.which === 13 || e.keyCode === 13) {
                                            e.preventDefault(); // Prevent default behavior (new line)
                                            $(this).blur(); // Trigger blur event which saves the value
                                        }
                                    });

                                    // Add Validovat button
                                    const validateButton = $('<button class="validate-btn">Validovat</button>');
                                    keyValuePair.append(validateButton);

                                    // Add click handler for validation button
                                    validateButton.on('click', function (e) {
                                        e.stopPropagation(); // Prevent triggering the parent click handler

                                        // Check if there's already an output element
                                        let outputElement = $(this).closest('.key-value-pair').next('.validation-output');
                                        if (!outputElement.length) {
                                            // Create new output element if it doesn't exist
                                            outputElement = $('<div class="validation-output" style="margin-left: 20px; margin-top: 5px;"></div>');
                                            $(this).closest('.key-value-pair').after(outputElement);
                                        }

                                        // Show the element and start generating text
                                        outputElement.show();
                                        outputElement.html('<div class="generating"><i class="spinner-border spinner-border-sm"></i> Generování validace...</div>');

                                        // Get the field name and original medical text
                                        const fieldName = $(this).closest('.key-value-pair').find('.key').text().replace(':', '');
                                        const originalMedicalText = medicalTextInput.val().trim();

                                        // Call the validation API
                                        $.ajax({
                                            url: '/api/validate',
                                            type: 'POST',
                                            contentType: 'application/json',
                                            data: JSON.stringify({
                                                text: originalMedicalText,
                                                field: fieldName
                                            }),
                                            success: function (response) {
                                                if (response.success) {
                                                    outputElement.html(response.suggestion);
                                                } else {
                                                    outputElement.html('Chyba validace: ' + (response.error || 'Neznámá chyba'));
                                                }
                                            },
                                            error: function (error) {
                                                outputElement.html('Chyba validace: ' + (error.responseJSON?.error || 'Neznámá chyba'));
                                            }
                                        });
                                    });
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

                    // Add click handler for searching and highlighting text
                    keyValuePair.on('click', function () {
                        const valueElement = $(this).find('.value');
                        if (valueElement.length) {
                            const value = valueElement.text();
                            if (value && value !== "null") {
                                searchAndHighlightText(value);
                            }
                        }
                    });

                    container.append(keyValuePair);
                }
            }

            return container;
        }

        // Render the JSON and append to results container
        analysisResults.append(renderJson(data));

        // Create the null values summary
        const summaryContainer = $('<div class="null-summary-container mt-3 p-2 border rounded"></div>');
        const nullValuesSpan = $(`<span class="null-value-count px-2 py-1 mx-1 rounded">Volitelné: ${nullValueCount}</span>`).css({
            'background-color': '#fff3cc',
            'color': '#856404',
            'font-weight': 'bold'
        });
        const nullRequiredValuesSpan = $(`<span class="null-required-value-count px-2 py-1 mx-1 rounded">Povinné: ${nullRequiredValueCount}</span>`).css({
            'background-color': '#ffcccc',
            'color': '#dc3545',
            'font-weight': 'bold'
        });

        summaryContainer.append($('<strong>Chybějící hodnoty: </strong>'));
        summaryContainer.append(nullRequiredValuesSpan);
        summaryContainer.append(nullValuesSpan);


        // Append the summary container to the card-body element (parent of analysisResults)
        analysisResults.parent().append(summaryContainer);

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
                .timeline-event { cursor: pointer; transition: transform 0.2s; }
                .timeline-event:hover { transform: scale(1.5); }
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
        // Store current scroll position and the highlighted element's position
        const scrollPos = originalText.scrollTop();
        const highlightedElement = originalText.find('.highlighted');
        let highlightPosition = null;
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

    // Search for text in the original content and highlight it if found
    function searchAndHighlightText(searchText) {
        if (!searchText) return;

        // Remove all existing highlights first
        const currentContent = originalText.html();
        originalText.html(currentContent.replace(/<span class="highlighted">(.*?)<\/span>/g, '$1'));

        // Create a temporary div to work with the HTML content
        const tempDiv = $('<div>').html(originalText.html());
        const textNodes = [];

        // Function to collect all text nodes within an element
        function collectTextNodes(element) {
            $(element).contents().each(function () {
                if (this.nodeType === 3) { // Text node
                    textNodes.push(this);
                } else if (this.nodeType === 1) { // Element node
                    collectTextNodes(this);
                }
            });
        }

        collectTextNodes(tempDiv);

        // Search for the text in the collected text nodes
        let found = false;
        for (let i = 0; i < textNodes.length; i++) {
            const node = textNodes[i];
            const nodeText = node.nodeValue;
            const index = nodeText.indexOf(searchText);

            if (index !== -1) {
                // Split the text node into three parts
                const beforeText = document.createTextNode(nodeText.substring(0, index));
                const highlightedSpan = document.createElement('span');
                highlightedSpan.className = 'highlighted';
                highlightedSpan.textContent = nodeText.substring(index, index + searchText.length);
                const afterText = document.createTextNode(nodeText.substring(index + searchText.length));

                // Replace the original text node with these three parts
                const parentNode = node.parentNode;
                parentNode.insertBefore(beforeText, node);
                parentNode.insertBefore(highlightedSpan, node);
                parentNode.insertBefore(afterText, node);
                parentNode.removeChild(node);

                found = true;
                break;
            }
        }

        if (found) {
            // Update the original text with the modified HTML
            originalText.html(tempDiv.html());

            // Scroll to the highlighted element
            const highlightedElement = originalText.find('.highlighted');
            if (highlightedElement.length) {
                // Calculate the scroll position to center the highlighted text
                const elementTop = highlightedElement.offset().top - originalText.offset().top;
                const elementHeight = highlightedElement.outerHeight();
                const containerHeight = originalText.height();
                const scrollTo = elementTop - (containerHeight / 2) + (elementHeight / 2) + originalText.scrollTop();

                // Smooth scroll with animation (300ms duration)
                originalText.animate({
                    scrollTop: scrollTo
                }, 300);
            }
        }
    }
}); 