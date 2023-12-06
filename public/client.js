
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
});