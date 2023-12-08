
document.addEventListener('DOMContentLoaded', () => {
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

    // Function to handle machine type click
//     const handleMachineTypeClick = (machineType) => {
//       // Make an HTTP request to the server to get filtered data based on machine type
//       fetch(`/api/filterByMachineType?machineType=${machineType}`)
//           .then(res => res.json())
//           .then(data => {
//               // Update the table with the filtered data
//               updateTable(data);
//           })
//           .catch(err => console.error('Error fetching filtered data:', err));
//   };

//   // Get all machine type links
//   const machineTypeLinks = document.querySelectorAll('.sub-menu li a');

//   // Add click event listener to each machine type link
//   machineTypeLinks.forEach(link => {
//       link.addEventListener('click', (event) => {
//           event.preventDefault();
//           const machineType = link.textContent.trim(); // Extract machine type from link text
//           handleMachineTypeClick(machineType);
//       });
//   });

//   // Function to update the table with new data
//   const updateTable = (data) => {
//       const tableBody = document.querySelector('#userTable tbody');

//       // Clear existing table rows
//       while (tableBody.firstChild) {
//           tableBody.removeChild(tableBody.firstChild);
//       }

//       // Append new rows to the table
//       data.forEach(user => {
//           const newRow = document.createElement('tr');
//           newRow.innerHTML = `
//               <td>${user.userID}</td>
//               <td>${user.AdminStatus === 1 ? 'Yes' : 'No'}</td>
//               <td>${user.MachineType}</td>
//               <td>${user.Date.toLocaleDateString()}</td>
//               <td>${user.StartTime}</td>
//               <td>${user.EndTime}</td>
//           `;
//           tableBody.appendChild(newRow);
//       });
//   };
});