document.addEventListener('DOMContentLoaded', function() {
    var summarizeButton = document.getElementById('summarize');
    var summaryField = document.getElementById('summary');

    summarizeButton.addEventListener('click', function() {
        // Change button text to "Summarizing..."
        summarizeButton.innerText = "Summarizing...";

        // Get YouTube video URL from input field
        var videoUrl = document.getElementById('videoUrl').value;

        // Make a request to your Flask backend to summarize the video transcript
        const apiUrl = 'http://127.0.0.1:5000/summarize'; // Update with your API URL

        const postData = {
            videoUrl: videoUrl
        };

        fetch(apiUrl, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            // Display the summary in the summary field
            summaryField.value = data.summary;

            // Reset button text to "SUMMARIZE"
            summarizeButton.innerText = "SUMMARIZE";
        })
        .catch(error => {
            console.error ('Error:', error);
            // Display an error message to the user
            summaryField.value = "An error occurred while summarizing the video.";
            summarizeButton.innerText = "SUMMARIZE";
        });
    });
})