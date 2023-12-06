const fs = require('fs');
const express = require('express'); // Import the ExpressJS framework
const pool = require('./database.js');
const papa = require('papaparse');
var table = 'Fablab'; //MySQL table name

//Express.js connection:
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
      res.status(500).send('SQL Server Query Error.'); 
      return;
    }

    res.render('index', { results });
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


// Handle Drill button click on the server side
// app.post('/drill', (req, res) => {
//   console.log('Drill button clicked on the server!');
//   // Your custom logic for the Drill button click on the server side

//   res.status(200).send('Drill button clicked on the server!');
// });

app.use(express.static(__dirname + '/public'));

app.listen(port, () => {
    console.log(`Server is listening at http://localhost:${port}`);
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
