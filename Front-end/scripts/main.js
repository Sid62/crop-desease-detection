let predictionHistory = [];

// Function to preview uploaded image
function previewImage(event) {
    const imagePreviewDiv = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImg.src = e.target.result;
            imagePreviewDiv.classList.remove('hidden'); // Show the image preview section
        };
        reader.readAsDataURL(file);
    }
}

// Function to predict disease
async function predictDisease() {
    const imageUpload = document.getElementById('imageUpload');
    if (!imageUpload.files.length) {
        alert("Please upload an image first.");
        return;
    }

    // Get the crop type from the select dropdown
    const cropSelect = document.getElementById("cropSelect");
    const crop = cropSelect.value;
    
    // Create FormData and append both image and crop type
    const formData = new FormData();
    formData.append('image', imageUpload.files[0]);
    formData.append('crop', crop); // Append crop parameter

    try {
        // Send the image and crop type to the server for prediction
        const response = await fetch('http://127.0.0.1:8000/disease_detection/predict/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }

        const result = await response.json();
        
        if (result.error) {
            alert("Error: " + result.error);
            return;
        }
        
        if (result.predicted_class) {
            displayResult(result);
            addToHistory(imageUpload.files[0], result);
        } else {
            alert("Unexpected error occurred. Please try again.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Network error: Unable to reach the server. Please check your connection and try again.");
    }
}

// Function to display prediction result
function displayResult(result) {
    document.getElementById('disease-name').textContent = "Predicted Disease: " + result.predicted_class;
    document.getElementById('confidence').textContent = "Confidence: " + (result.confidence * 100).toFixed(2) + "%";
    
    // Fetch solution
    fetchSolution(result.predicted_class);

    // Show result section
    document.getElementById('result-section').classList.remove('hidden');
}

// Function to fetch solution
async function fetchSolution(diseaseName) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/disease_detection/solution/${diseaseName.replace(/ /g, '%20')}/`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch solution: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.solution) {
            document.getElementById('solution').textContent = result.solution;
        } else {
            document.getElementById('solution').textContent = "Solution not available.";
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Error while fetching solution. Please try again later.");
    }
}

// Function to add prediction to history
function addToHistory(image, result) {
    const reader = new FileReader();
    reader.onload = function (e) {
        const historyList = document.getElementById('history-list');
        const listItem = document.createElement('li');
        listItem.classList.add('history-item');
        listItem.innerHTML = `
            <img src="${e.target.result}" alt="History Image">
            <span>${result.predicted_class} (${(result.confidence * 100).toFixed(2)}%)</span>
            <button class="repredict-btn" onclick="rePredict('${e.target.result}')">Re-Predict</button>
        `;
        historyList.appendChild(listItem);
    };
    reader.readAsDataURL(image);
}

// Function to re-predict history images
function rePredict(imageSrc) {
    document.getElementById('preview-img').src = imageSrc;
    document.getElementById('image-preview').classList.remove('hidden');
}

async function fetchSolution(diseaseName) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/disease_detection/solution/${diseaseName.replace(/ /g, '%20')}/`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch solution: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.solution) {
            document.getElementById('solution').textContent = result.solution;
        } else {
            document.getElementById('solution').textContent = "Solution not available.";
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Error while fetching solution. Please try again later.");
    }
}


function fetchBrowserLocation() {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
  
          try {
            const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${latitude}&lon=${longitude}`;
            const response = await fetch(url);
            const data = await response.json();
  
            const city = data.address.city || data.address.town || data.address.village || "Unknown City";
            const state = data.address.state || "Unknown State";
            const postcode = data.address.postcode || "Unknown PIN";
  
            document.getElementById('location').textContent =
              `City: ${city}, State: ${state}, PIN: ${postcode}`;
          } catch (error) {
            console.error("Reverse geocoding failed:", error);
            document.getElementById('location').textContent =
              `Lat: ${latitude.toFixed(4)}, Lng: ${longitude.toFixed(4)} (City info unavailable)`;
          }
        },
        (error) => {
          console.error("Geolocation error:", error);
          document.getElementById('location').textContent =
            "Location access denied or unavailable.";
        }
      );
    } else {
      document.getElementById('location').textContent =
        "Geolocation not supported by your browser.";
    }
  }
  
  window.onload = () => {
    fetchBrowserLocation();
  };
  
