const desktop1 = document.getElementById("desktop1");
const desktop2 = document.getElementById("desktop2");
const desktop3 = document.getElementById("desktop3");
const fileNameElem = document.getElementById("fileName");
let fileName = "";
let file;
let csvData = [];


function allowDrop(event) {
    event.preventDefault();
}

async function fetchThresholds() {
    
    try {
        const url = `http://127.0.0.1:5000/get_thresholds?filePath=${encodeURIComponent(fileName)}`;
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        
        const results = data.results
        
        return results;
        // Use these values as needed in your application
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}

function parseCSV(data) {
    const rows = data.split('\n').filter(row => row.trim() !== ''); // Split by new line and filter empty lines
    return rows.map(row => row.split(',').map(value => value.trim())); // Split each row by commas and trim spaces
}

async function loadFile() {
    const reader = new FileReader();
    reader.onload = function (event) {
        const c_csvData = event.target.result;
        csvData = parseCSV(c_csvData);
        csvData.shift();
        
    }
    reader.readAsText(file);
}

function handleDrop(event) {
    event.preventDefault();
    file = event.dataTransfer.files[0];
    if (file && file.name.endsWith(".csv")) {
        fileName = "Assets/" + file.name;
        fileNameElem.textContent = file.name;
        
        goToDesktop2();
    } else {
        alert("Please upload a CSV file.");
    }
}

function browseFile() {
    document.getElementById("fileInput").click();
}

function handleFileSelect(event) {
    file = event.target.files[0];
    if (file && file.name.endsWith(".csv")) {
        fileName = "Assets/" + file.name;
        fileNameElem.textContent = file.name;
        goToDesktop2();
    } else {
        alert("Please upload a CSV file.");
    }
}

function goBack() {
    fileName = "";
    document.getElementById("fileInput").value = "";
    goToDesktop1();
}

function goToDesktop1() {
    desktop1.style.display = "block";
    desktop2.style.display = "none";
    desktop3.style.display = "none";
}

function goToDesktop2() {
    desktop1.style.display = "none";
    desktop2.style.display = "block";
    desktop3.style.display = "none";
}


async function goToDesktop3() {
    desktop1.style.display = "none";
    desktop2.style.display = "none";
    desktop3.style.display = "block";
    await loadFile();
    const playerResults = fetchThresholds(); // Assuming this is properly awaited
    // Ensure you wait for fetchThresholds to complete and get the playerResults
    playerResults.then(results => {
        
        const tableBody = document.querySelector("#excelTable tbody");
        Object.entries(results).forEach(([index, value]) => {
            const isPlrSucess = value[3];
                let row = csvData[index];
                const tr = document.createElement("tr");

                // Populate the cells
                for (const key in row) {
                    if(key == 1) {
                        const td = document.createElement("td");
                        td.textContent = isPlrSucess.toString();
                        if(isPlrSucess) {
                            td.classList.add("accepted_recruit");
                        } else {
                            td.classList.add("rejected_recruit");
                        }
                        tr.appendChild(td);
                    }
                    const td = document.createElement("td");
                    td.textContent = row[key];
                    tr.appendChild(td);
                }

                // Add event listeners for hover and click
                tr.addEventListener("click", () => displayPlayerData(value));
                
                // Append the row to the table
                tableBody.appendChild(tr);
            
            
        })
        
        
    }).catch(error => console.error('Error fetching thresholds:', error));
}




function displayPlayerData(playerData) {
    const min_threshold = playerData[0];
    const significance = playerData[1];
    const a = playerData[2];
    let quant_accept;
    let message = '-----------------------------------------\n';

    if (a < min_threshold) {
        message += 'We reject the recruit since they are below the third quantile.\n';
        message += `3rd Quantile: ${min_threshold}\n`;
        message += `Recruit: ${a}\n`;
        quant_accept = false;
    } else {
        message += 'Recruit is in the 3rd quantile. (Good)\n';
        message += `3rd Quantile: ${min_threshold}\n`;
        message += `Recruit: ${a}\n`;
        quant_accept = true;
    }

    message += '-----------------------------------------\n';

    if (quant_accept && significance <= 0.3) { // Assuming significance should be > 0 to accept
        message += `We recommend this recruit with a significance value of ${significance} and a quantile significance of ${a / min_threshold}.\n`;
    } else {
        message += `We reject this recruit with a significance value of ${significance} and a quantile significance of ${a / min_threshold}.\n`;
    }

    // Display the message
    alert(message); // Or you can display it in a specific div instead of an alert
}
