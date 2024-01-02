function acknowledgeAlert(alertId) {
    // Prepare the data to be sent in the request body
    var requestData = {
    alert_id: alertId
    };

    // Send a PUT request using jQuery Ajax
    $.ajax({
    type: 'PUT',
    url: '/api/acknowledge_alert/',
    contentType: 'application/json',
    data: JSON.stringify(requestData),
    success: function (response) {
        // Handle success response
        console.log(response);
        // Optionally update the UI or perform other actions on success

        // Refresh the page after a short delay (e.g., 500 milliseconds)
        setTimeout(function () {
        location.reload();
        }, 500);
    },
    error: function (error) {
        // Handle error response
        console.error(error);
        // Optionally show an error message or perform other actions on error
    }
    });
}

function unacknowledgeAlert(alertId) {
    // Prepare the data to be sent in the request body
    var requestData = {
        alert_id: alertId
    };

    // Send a PUT request using jQuery Ajax
    $.ajax({
        type: 'PUT',
        url: '/api/unacknowledge_alert/',
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        success: function (response) {
        // Handle success response
        console.log(response);
        // Optionally update the UI or perform other actions on success

        // Refresh the page after a short delay (e.g., 500 milliseconds)
        setTimeout(function () {
            location.reload();
        }, 500);
        },
        error: function (error) {
        // Handle error response
        console.error(error);
        // Optionally show an error message or perform other actions on error
        }
    });
}

function archiveAlert(alertId) {
    // Prepare the data to be sent in the request body
    var requestData = {
        alert_id: alertId
    };

    // Send a PUT request using jQuery Ajax
    $.ajax({
        type: 'PUT',
        url: '/api/close_alert/',
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        success: function (response) {
        // Handle success response
        console.log(response);
        // Optionally update the UI or perform other actions on success

        // Refresh the page after a short delay (e.g., 500 milliseconds)
        setTimeout(function () {
            location.reload();
        }, 500);
        },
        error: function (error) {
        // Handle error response
        console.error(error);
        // Optionally show an error message or perform other actions on error
        }
    });
}

function archiveAllExpiredAlert() {    
    // Send a PUT request using jQuery Ajax
    $.ajax({
        type: 'PUT',
        url: '/api/close_expired_alerts/',
        contentType: 'application/json',
        data: JSON.stringify({}),
        success: function (response) {
        // Handle success response
        console.log(response);
        // Optionally update the UI or perform other actions on success

        // Refresh the page after a short delay (e.g., 500 milliseconds)
        setTimeout(function () {
            location.reload();
        }, 500);
        },
        error: function (error) {
        // Handle error response
        console.error(error);
        // Optionally show an error message or perform other actions on error
        }
    });
}

// Function to handle bulk acknowledgment
function acknowledgeSelectedAlerts() {
    var selectedAlerts = getSelectedAlerts();
    
    // Prepare the JSON data with selected alert IDs
    const requestData = {
        alert_ids: selectedAlerts
    };

    // Send a PUT request using jQuery Ajax
    $.ajax({
        type: 'PUT',
        url: '/api/acknowledge_alerts_bulk/',
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        success: function (response) {
            // Handle success response
            console.log(response);
            // Optionally update the UI or perform other actions on success

            // Refresh the page after a short delay (e.g., 500 milliseconds)
            setTimeout(function () {
                location.reload();
            }, 500);
        },
        error: function (error) {
            // Handle error response
            console.error(error);
            // Optionally show an error message or perform other actions on error
        }
    });
    console.log("Acknowledge selected alerts:", selectedAlerts);
}

// Function to handle bulk closure
function closeSelectedAlerts() {
    var selectedAlerts = getSelectedAlerts();
    // Perform bulk closure logic using selectedAlerts array
    // Prepare the JSON data with selected alert IDs
    const requestData = {
        alert_ids: selectedAlerts
    };

    // Send a PUT request using jQuery Ajax
    $.ajax({
        type: 'PUT',
        url: '/api/close_alerts_bulk/',
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        success: function (response) {
            // Handle success response
            console.log(response);
            // Optionally update the UI or perform other actions on success

            // Refresh the page after a short delay (e.g., 500 milliseconds)
            setTimeout(function () {
                location.reload();
            }, 500);
        },
        error: function (error) {
            // Handle error response
            console.error(error);
            // Optionally show an error message or perform other actions on error
        }
    });
    console.log("Close selected alerts:", selectedAlerts);
}

// Function to get an array of selected alert IDs
function getSelectedAlerts() {
    var selectedAlerts = [];
    // Iterate through all checkboxes with class 'alert-checkbox'
    document.querySelectorAll('.alert-checkbox:checked').forEach(function (checkbox) {
        selectedAlerts.push(checkbox.getAttribute('data-alert-id'));
    });
    return selectedAlerts;
}

// Function to update the visibility of bulk action buttons
function updateBulkButtonsVisibility() {
    var selectedAlerts = getSelectedAlerts();
    var bulkButtons = document.getElementById('bulkActionButtons');

    if (selectedAlerts.length > 0) {
        bulkButtons.classList.remove('d-none');
        bulkButtons.classList.add('d-flex');
    } else {
        bulkButtons.classList.add('d-none');
        bulkButtons.classList.remove('d-flex');
    }
}
//Search Function
document.addEventListener("DOMContentLoaded", function() {
    var searchInput = document.getElementById("searchInput");
    var alertRows = document.getElementsByClassName("alert-row");

    searchInput.addEventListener("input", function() {
        var filter = searchInput.value.toLowerCase();

        for (var i = 0; i < alertRows.length; i++) {
            var alertRow = alertRows[i];
            var alertText = alertRow.textContent || alertRow.innerText;

            if (alertText.toLowerCase().indexOf(filter) > -1) {
                alertRow.style.display = "";
            } else {
                alertRow.style.display = "none";
            }
        }
    });
});

// Event listener for the 'Select All' checkbox
document.getElementById('selectAllCheckbox').addEventListener('change', function () {
    // Get the state of the 'Select All' checkbox
    var selectAllChecked = this.checked;
    // Set the state of all checkboxes with class 'alert-checkbox'
    document.querySelectorAll('.alert-checkbox').forEach(function (checkbox) {
        checkbox.checked = selectAllChecked;
    });
});

// Event listener for checkbox change
document.addEventListener('change', function (event) {
    // Check if the changed element is a checkbox with class 'alert-checkbox' or the 'Select All' checkbox
    if (event.target.classList.contains('alert-checkbox') || event.target.id === 'selectAllCheckbox') {
        updateBulkButtonsVisibility();
    }
});

document.addEventListener('DOMContentLoaded', function () {
    // Get the dropdown element
    var refreshDropdown = document.getElementById('refreshIntervalDropdown');

    // Set the default value to 'Never'
    var defaultRefreshInterval = localStorage.getItem('refreshInterval') || 0;
    refreshDropdown.value = defaultRefreshInterval;

    // Function to handle dropdown change
    function handleRefreshChange() {
        // Get the selected value
        var selectedValue = refreshDropdown.value;

        // Save the selected value to local storage
        localStorage.setItem('refreshInterval', selectedValue);

        // Clear any existing interval
        if (window.refreshInterval) {
            clearInterval(window.refreshInterval);
        }

        // Set up a new interval if the selected value is not 'Never'
        if (selectedValue !== '0') {
            window.refreshInterval = setInterval(function () {
                // Reload the page
                location.reload();
            }, selectedValue * 60 * 1000); // Convert minutes to milliseconds
        }
    }

    // Add event listener for dropdown change
    refreshDropdown.addEventListener('change', handleRefreshChange);

    // Initial setup based on the default value
    handleRefreshChange();
});