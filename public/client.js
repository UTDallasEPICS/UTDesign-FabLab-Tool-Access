
const padWithZero = (number) => {
  return number < 10 ? '0' + number : number;
};

// Function to update the table with new data
const updateTable = (data) => {
  const tableBody = document.querySelector('#userTable tbody');

  // Clear existing table rows
  while (tableBody.firstChild) {
      tableBody.removeChild(tableBody.firstChild);
  }

  // Append new rows to the table
  data.forEach(user => {
      const newRow = document.createElement('tr');
      newRow.innerHTML = `
          <td>${user.userID}</td>
          <td>${user.AdminStatus == 1 ? 'Yes' : 'No'}</td>
          <td>${user.MachineType}</td>
          <td>${new Date(user.Date).toLocaleDateString()}</td>
          <td>${user.StartTime}</td>
          <td>${user.EndTime}</td>
      `;
      tableBody.appendChild(newRow);
  });
  //<td>${user.Date.toLocaleDateString() == undefined ? 'N/A' : user.Date.toLocaleDateString()}</td>
};

document.addEventListener('DOMContentLoaded', () => {

  if (localStorage) {
    const storedMachineType = localStorage.getItem('selectedMachineType');
    const storedDate = localStorage.getItem('selectedDate');

    if (storedMachineType) {
      // Make an HTTP request to the server to get filtered data based on machine type
      fetch(`/api/filterByMachineType?machineType=${encodeURIComponent(storedMachineType)}`)
        .then(res => {
            if (!res.ok) {
                throw new Error(`Error ${res.status}: ${res.statusText}`);
            }
            return res.json();
        })
        .then(data => {
            // Process the data
            console.log('Filtered data:', data);
            updateTable(data); // Update the table with the filtered data
            TableVisibility();
        })
        .catch(err => {
            console.error('Error fetching filtered data:', err.message);
        });
    }
    else if (storedDate) {
      const month = storedDate.split('-')[1];
      const day = storedDate.split('-')[2];

      // Make an HTTP request to the server to get filtered data based on month and day
      fetch(`/api/filterByDate?month=${encodeURIComponent(month)}&day=${encodeURIComponent(day)}`)
        .then(res => {
            if (!res.ok) {
                throw new Error(`Error ${res.status}: ${res.statusText}`);
            }
            return res.json();
        })
        .then(data => {
            // Process the data
            console.log('Filtered data:', data);
            updateTable(data); // Update the table with the filtered data
            TableVisibility();
        })
        .catch(err => {
            console.error('Error fetching filtered data:', err.message);
        });
    }
    else {
      TableVisibility();
    }
  }

  // Function to handle month and day click
  const handleDateClick = (month, day) => {

    localStorage.setItem('selectedDate', `${new Date().getFullYear()}-${month}-${day}`);

    // Make an HTTP request to the server to get filtered data based on month and day
    fetch(`/api/filterByDate?month=${encodeURIComponent(month)}&day=${encodeURIComponent(day)}`)
      .then(res => {
          if (!res.ok) {
              throw new Error(`Error ${res.status}: ${res.statusText}`);
          }
          return res.json();
      })
      .then(data => {
          // Process the data
          console.log('Filtered data:', data);
          updateTable(data); // Update the table with the filtered data
      })
      .catch(err => {
          console.error('Error fetching filtered data:', err.message);
      });
  };

  const DateLinks = document.querySelectorAll('.dropdown a')

  //Add event listener for what month and day is clicked
  DateLinks.forEach(link => {
    link.addEventListener('click', event => {
      const month = event.target.closest('.dropdown-content').getAttribute('itemid'); // Get the month from the data-month attribute
      const day = padWithZero(event.target.innerText); // Get the day from the clicked link's text

      // Call the handleTimeClick function with the selected month and day
      handleDateClick(month, day);
      console.log(`Date: ${month} ${day} link clicked on the client!`);
    });
  });

  // -------------------------

  // Function to handle machine type click
  const handleMachineTypeClick = (machineType) => {

    localStorage.setItem('selectedMachineType', machineType);

  // Make an HTTP request to the server to get filtered data based on machine type
  fetch(`/api/filterByMachineType?machineType=${encodeURIComponent(machineType)}`)
    .then(res => {
        if (!res.ok) {
            throw new Error(`Error ${res.status}: ${res.statusText}`);
        }
        return res.json();
    })
    .then(data => {
        // Process the data
        console.log('Filtered data:', data);
        updateTable(data); // Update the table with the filtered data
    })
    .catch(err => {
        console.error('Error fetching filtered data:', err.message);
    });
};

// Get all machine type links
const machineTypeLinks = document.querySelectorAll('#machine-list li a');

// Add click event listener to each machine type link
machineTypeLinks.forEach(link => {
    link.addEventListener('click', (event) => {
      if (link.innerText === 'Machines' || link.innerText === 'Time') {
        return; // Exit the event listener early
    }
        event.preventDefault();
        const machineType = link.textContent.trim(); // Extract machine type from link text
        handleMachineTypeClick(machineType);
        console.log(`Machine ${machineType} link clicked on the client!`);
    });
});

// -------------------------

  //Get home button to display all data
  const homeButton = document.querySelector('#home_btn');
  homeButton.addEventListener('click', () => {

    // Clear local storage
    localStorage.removeItem('selectedMachineType');
    localStorage.removeItem('selectedDate');

    console.log('Home button clicked on the client!');
    // Make an HTTP request to the server to get all data
    fetch('/api/home')
    .then(res => {
        if (!res.ok) {
            throw new Error(`Error ${res.status}: ${res.statusText}`);
        }
        return res.json();
    })
    .then(data => {
        // Process the data
        console.log('All data:', data);
        updateTable(data); // Update the table with the filtered data
    })
    .catch(err => {
        console.error('Error fetching all data:', err.message);
    });
  });

  const downloadBtn = document.getElementById('download-btn');
  if (downloadBtn) {
    downloadBtn.addEventListener('click', () => {
      console.log('Download button clicked on the client!');
      // Make an HTTP request to the server to download the CSV
      fetch('/api/downloadCSV')
        .then (res => res.blob())
        .then (blob => {
          //Create download link
          const link = document.createElement('a');
          link.href = URL.createObjectURL(blob);
          link.download = 'Fablab_Log.csv'
          document.body.appendChild(link);

          //Trigger download
          link.click();

          //Remove link from DOM
          document.body.removeChild(link);
        })
        .catch(err => console.error('Line 31:', err.message));
    });
  }
  //Download button tooltip
  const downloadButton = document.getElementById('download-btn');
    const tooltip = downloadButton.querySelector('.tooltip');

    if (downloadButton) {
        downloadButton.addEventListener('mouseenter', () => {
            tooltip.style.visibility = 'visible';
            tooltip.style.opacity = '1';
        });

        downloadButton.addEventListener('mouseleave', () => {
            tooltip.style.visibility = 'hidden';
            tooltip.style.opacity = '0';
        });
    }

  //Make table visible
  function TableVisibility() {
    const userTable = document.querySelector('#userTable');
    userTable.style.visibility = 'visible';
  }
  
});

// Clear the localStorage when the window is about to be unloaded
window.addEventListener('beforeunload', () => {
  if (localStorage)
    localStorage.clear();
});

