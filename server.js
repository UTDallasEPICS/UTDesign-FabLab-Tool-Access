const fs = require('fs');
const express = require('express'); // Import the ExpressJS framework
const pool = require('./database.js');
const papa = require('papaparse');
var table = 'Fablab'; //MySQL table name

//Express.js connection:
const hostname = "127.0.0.1";
const app = express();
const port = 3000;

app.set('view engine', 'ejs');

//Connection to local mysql server:
// const connection = mysql.createConnection({
//   host: 'localhost',    
//   user: 'pi', 
//   password: 'pi', 
//   database: 'testdb' //MySQL database name
// });

//Display the log table in main page
app.get('/', (req, res) => {
  const selectQuery = `SELECT * FROM ${table}`;

  pool.query(selectQuery, (err, results, fields) => {
    if (err) {
      console.error(err.message);
      res.status(500).send(`Internal Server Error! Cannot query Database ${table}.`); 
      return;
    }
      res.render('index', { results });
   
  });
});

//Go to home page
app.get('/api/home', (req, res) => {
  const selectQuery = `SELECT * FROM ${table}`;

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
  console.log(`Machine ${machineType} clicked on the server!`);
  const selectQuery = `SELECT * FROM ${table} WHERE MachineType='${machineType}'`;

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

  console.log(`Month ${month} and Day ${day} clicked on the server!`);

  const selectQuery = `SELECT * FROM ${table} WHERE DATE = '${new Date().getFullYear()}-${month}-${day}'`;
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

//Download CSV
app.get('/api/downloadCSV', (req, res) => {
  const selectQuery = `SELECT * FROM ${table}`;

  pool.query(selectQuery, (err, results, fields) => {
    if (err) {
      console.error(err.message);
      res.status(500).send('SQL Server Query Error.'); 
      return;
    }

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