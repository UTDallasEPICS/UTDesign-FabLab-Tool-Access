const fs = require('fs');
const express = require('express'); // Import the ExpressJS framework
const pool = require('./database.js');
const papa = require('papaparse');

var table = 'Fablab'; //MySQL table name
var limit = 100; //Number of records to display in main page

//Express.js connection:
const hostname = "127.0.0.1";
const app = express();
const port = 3000;

app.set('view engine', 'ejs');

// Function to clear records older than 5 years
const clearOldRecords = async () => {
  try {
      const deleteQuery = `DELETE FROM ${table} WHERE date < DATE_SUB(NOW(), INTERVAL 5 YEAR)`;
      const result = await pool.query(deleteQuery);
      if (result.affectedRows > 0)
          console.log('Old records deleted successfully.');
  } catch (error) {
      console.error('Error deleting old records:', error.message);
  }
};

// Call the function to clear old records
clearOldRecords();

//Display the log table in main page
app.get('/', (req, res) => {
  const selectQuery = 
  `SELECT *
  FROM ${table}
  ORDER BY date DESC, logID DESC 
  LIMIT ${limit}`;
  const queryMachineList = `SELECT DISTINCT MachineType FROM ${table}`;

  pool.query(selectQuery, (err, results, fields) => {
    if (err) {
      console.error(err.message);
      res.status(500).send(`Internal Server Error! Cannot query Database ${table}.`); 
      return;
    }

    pool.query(queryMachineList, (err, machines, fields) => {
      if (err) {
        console.error(err.message);
        res.status(500).send(`Internal Server Error! Cannot query Database ${table}.`); 
        return;
      }

      // Combine the data into a single object
      const templateData = {
        results,
        machines,
        limit
      };

      // Render the template with the combined data
      res.render('index', templateData);
    });
  });
});


//Go to home page
app.get('/api/home', (req, res) => {
  const selectQuery = `SELECT * FROM ${table} ORDER BY date DESC, logID DESC LIMIT ${limit}`;

  pool.query(selectQuery, (err, results, fields) => {
    if (err) {
      console.error(err.message);
      res.status(500).send('SQL Server Query Error.'); 
      return;
    }
    
    res.json(results);
  });
});

//Sort by machine type
app.get('/api/filterByMachineType', (req, res) => {
  const machineType = req.query.machineType;
  if (!machineType) {
      res.status(400).send('Missing required query parameter: machineType');
      return;
  }
  // console.log(`Machine ${machineType} clicked on the server!`);
  const selectQuery = `SELECT * FROM ${table} WHERE MachineType='${machineType}' ORDER BY date DESC, logID DESC LIMIT ${limit}`;

  pool.query(selectQuery, (err, results, fields) => {
    if (err) {
      console.error(err.message);
      res.status(500).send('SQL Server Query Error.'); 
      return;
    }
    //Send the filtered data to client (as JSON)
    res.send(results);
  });
});

//Sort by month and day
app.get('/api/filterByDate', (req, res) => {
  const month = req.query.month;
  const day = req.query.day;
  if (!month || !day) {
      res.status(400).send('Missing required query parameter: month or day');
      return;
  }
  //console.log(`Month ${month} and Day ${day} clicked on the server!`);

  const selectQuery = `SELECT * FROM ${table} WHERE 
  DATE = '${new Date().getFullYear()}-${month}-${day}' ORDER BY logID DESC`;

  pool.query(selectQuery, (err, results, fields) => {
    if (err) {
      console.error(err.message);
      res.status(500).send('SQL Server Query Error.'); 
      return;
    }
    //Send the filtered data to client (as JSON)
    res.send(results);
  });
});

//Delete machine type
app.get('/api/deleteMachine', (req, res) => {
  const machineType = req.query.machineType;
  if (!machineType) {
      res.status(400).send('Missing required query parameter: machineType');
      return;
  }
  const deleteQuery = `DELETE FROM ${table} WHERE MachineType='${machineType}'`;
  pool.query(deleteQuery, (err, results, fields) => {
    if (err) {
      console.error(err.message);
      res.status(500).send('SQL Server Query Error.'); 
      return;
    }
    if (results.affectedRows === 0) {
      //send bad response to client (popup alert that delete failed)
      res.json({ success: false });
    }
    else {
      const queryMachineList = `SELECT DISTINCT MachineType FROM ${table}`;
      pool.query(queryMachineList, (err, results, fields) => {
        // Send a response with the updated machine list
        if (err) {
          console.error(err.message);
          res.json({ success: false });
          return;
        }
        res.json({ success: true, machines: results});
      });
    }
  });
});

//Download CSV
app.get('/api/downloadCSV', (req, res) => {
  console.log('Download CSV clicked on the server!');
  const machineType = req.query.machineType;
  const date = req.query.date;

  let selectQuery;

  if (machineType) {
    selectQuery = `SELECT * FROM ${table} WHERE MachineType='${machineType}' ORDER BY Date DESC, logID DESC`;
  } else if (date) {
    const month = date.split('-')[1];
    const day = date.split('-')[2];
    selectQuery = `SELECT * FROM ${table} WHERE DATE = '${new Date().getFullYear()}-${month}-${day}' ORDER BY logID DESC`;
  } else {
    selectQuery = `SELECT * FROM ${table} ORDER BY Date DESC, logID DESC`;
  }

  pool.query(selectQuery, (err, results, fields) => {
    if (err) {
      console.error(err.message);
      res.status(500).send('SQL Server Query Error.');
      return;
    }
    console.log(results);

    //Using papaparse to convert query result to csv file
    const csv = papa.unparse(results);

    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', 'attachment; filename=\"Fablab_Log.csv\"');

    //Send CSV to client
    res.status(200).send(csv);
  });
});

app.use(express.static(__dirname + '/public'));

app.listen(port, () => {
    console.log(`Server is listening at http://${hostname}:${port}`);
  });

// Close the MySQL connection when the application is shutting down (Ctrl + C on terminal)
process.on('SIGINT', () => {
  pool.end((err) => {
    if (err) {
      console.error('Error closing MySQL connection:', err);
      process.exit(1);
    }
    console.log('MySQL connection closed');
    process.exit(0);
  });
});
