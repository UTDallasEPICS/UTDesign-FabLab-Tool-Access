
const padWithZero = (number) => {
  return number < 10 ? '0' + number : number;
};

// Function to update the machine list
const updateMachineList = (machines) => {
  const machineListContainer = document.getElementById('machine-list');
  machineListContainer.innerHTML = ''; // Clear the existing list

  // Add the 'Machines' link
  const machinesLink = document.createElement('li');
  machinesLink.innerHTML = '<a class="link_name" href="#">Machines </a>';
  machineListContainer.appendChild(machinesLink);

  // Add each machine to the list
  machines.forEach(machine => {
    const machineLink = document.createElement('li');
    machineLink.innerHTML = `<a href="#">${machine}</a>`;
    machineListContainer.appendChild(machineLink);
  });

  // Reload the current page
  location.reload();
};

const updateDisplayText = () => {
  const optionsDisplay = document.querySelector('.options-display');
  const machineType = sessionStorage.getItem('selectedMachineType');
  const storedDate = sessionStorage.getItem('selectedDate');
  //Now render it to index.ejs
  if (machineType) {
    optionsDisplay.innerHTML = `<h2> Sorting by Machine: ${machineType} </h2>`;
  } else if (storedDate) {
    const month = storedDate.split('-')[1];
    const day = storedDate.split('-')[2];
    optionsDisplay.innerHTML = `<h2> Sorting by Date: ${month}-${day}-${new Date().getFullYear()} </h2>`;
  } else {
    optionsDisplay.innerHTML = '<h2> Viewing All Log Data </h2>';
  }
}

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
          <td>${user.adminStatus == 1 ? '<p style="color:#32CD32;">Yes</p>' : 'No'}</td>
          <td>${user.machineType}</td>
          <td>${new Date(user.date).toLocaleDateString()}</td>
          <td>${user.startTime}</td>
          <td>${user.endTime}</td>
      `;
      tableBody.appendChild(newRow);
  });
  updateDisplayText();
  //<td>${user.Date.toLocaleDateString() == undefined ? 'N/A' : user.Date.toLocaleDateString()}</td>
};

//DOMContentLoaded Main event listener
document.addEventListener('DOMContentLoaded', () => {

  if (sessionStorage) {
    const storedMachineType = sessionStorage.getItem('selectedMachineType');
    const storedDate = sessionStorage.getItem('selectedDate');

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

  //Function that handles the search bar
  const searchBar = document.querySelector('.search-bar');
  const form = document.querySelector('form');
  
  //Event listner that sends a request to the server to search for the revelant data using await
  form.addEventListener('submit', event => {
    event.preventDefault(); //Prevent page reload
    searchBar.addEventListener('keyup', async (e) => {
      // Check if the key pressed was 'Enter'
      if (e.key === 'Enter' || e.keyCode === 13) {
        const searchString = e.target.value.toLowerCase();
        const response = await fetch(`/api/search?searchString=${encodeURIComponent(searchString)}`);
        if (response.ok) {
          const responseData = await response.json();
          updateTable(responseData);
        }
      }
    });
  });

  // Function to handle month and day click
  const handleDateClick = (month, day) => {

    sessionStorage.removeItem('selectedMachineType');
    sessionStorage.setItem('selectedDate', `${new Date().getFullYear()}-${month}-${day}`);

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
    });
  });

  // -------------------------

  // Function to handle machine type click
  const handleMachineTypeClick = (machineType) => {

    sessionStorage.removeItem('selectedDate');
    sessionStorage.setItem('selectedMachineType', machineType);

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
      });
  });

  // -------------------------

  //Get home button to display all data
  const homeButton = document.querySelector('#home_btn');
  homeButton.addEventListener('click', () => {

    // Clear local storage
    sessionStorage.removeItem('selectedMachineType');
    sessionStorage.removeItem('selectedDate');

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
          updateTable(data); // Update the table with the filtered data
      })
      .catch(err => {
          console.error('Error fetching all data:', err.message);
      });
  });

  //Detect if download button is clicked
  const downloadBtn = document.getElementById('download-btn');
  if (downloadBtn) {
    downloadBtn.addEventListener('click', () => {

    // Check if machine type is stored in sessionStorage
    const storedMachineType = sessionStorage.getItem('selectedMachineType');
    // Check if date is stored in sessionStorage
    const storedDate = sessionStorage.getItem('selectedDate');

    let downloadUrl = '/api/downloadCSV';

    // Decide which parameter to include based on stored values
    var index = 0;
    if (storedMachineType) {
      downloadUrl += `?machineType=${encodeURIComponent(storedMachineType)}`;
      index = 1;
    } else if (storedDate) {
      downloadUrl += `?date=${encodeURIComponent(storedDate)}`;
      index = 2;
    }
    // Make an HTTP request to the server to download the CSV
      fetch(downloadUrl)
        .then (res => res.blob()) 
        .then (blob => {
          //Create download link
          const link = document.createElement('a');
          link.href = URL.createObjectURL(blob);
          if (index === 1) {
            link.download = `Fablab_Log_${storedMachineType}.csv`
          } else if (index === 2) {
            link.download = `Fablab_Log_${storedDate}.csv`
          } else {
            link.download = `Fablab_Log_All.csv`
          }
          document.body.appendChild(link);

          //Trigger download
          link.click();

          //Remove link from DOM
          document.body.removeChild(link);
        })
        .catch(err => console.error('CSV Download Failed:', err.message));
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

  //Delete existing Machine
  const deleteButton = document.querySelector('#delete-machine-btn');
  deleteButton.addEventListener('click', async () => {

    const machineName = prompt('Enter the machine type to delete:');
    if (machineName) {
      const confirmDelete = confirm(`Are you sure you want to delete ${machineName}?`);
      if (confirmDelete) {
        const response = await fetch(`/api/deleteMachine?machineType=${encodeURIComponent(machineName)}`)
        if (response.ok) {
          const responseData = await response.json();
          if (responseData.success) {
            alert('Machine deleted successfully!');
            updateMachineList(responseData.machines);
          }
          else {
            alert('Invalid machine type! No machine deleted');
          }
        }
        else {
          console.error(`Error ${response.status}: ${response.statusText}`);
        }
      }
    }
  });

  //Add new machine //W.I.P
  const addButton = document.querySelector('#add-machine-btn');
  addButton.addEventListener('click', async () => {
    alert('⚠ This feature is not yet implemented')
  });

  //Make table visible
  function TableVisibility() {
    const userTable = document.querySelector('#userTable');
    userTable.style.visibility = 'visible';
  }
  
});

// DEPRECIATED FUNCTION! SessionStorage automatically clears session when window is closed.
// Clear the localStorage when the window is about to be unloaded
// window.addEventListener('beforeunload', () => {
//   // Check if the page is being closed, not refreshed
//   if (performance.navigation.type === PerformanceNavigation.TYPE_NAVIGATE) {
//     // Clear the localStorage
//     localStorage.clear();
//   }
// });


