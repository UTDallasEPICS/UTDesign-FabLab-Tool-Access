const fs = require('fs');
//const db = require('./Database/db'); // Import the SQLite database module
const express = require('express'); // Import the ExpressJS framework
const mysql = require('mysql'); // Import the MySQL database module

//Express.js connection:
const app = express();
const port = 3000;

app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/public'));

//Connection to local mysql server:
// const connection = mysql.createConnection({
//   host: 'localhost',    
//   user: 'pi', 
//   password: 'pi', 
//   database: 'testdb' //MySQL database name
// });

const connection = mysql.createConnection({
  host: 'sql3.freesqldatabase.com',    
  user: 'sql3667697', 
  password: '1dmeYAZjPr', 
  database: 'sql3667697' //MySQL database name
});

// Connect to the MySQL server
connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL server:', err);
    return;
  }
  console.log('Connected to MySQL server');

  const database = connection.config.database;

  // Select the MySQL database
  connection.query(`USE ${database}`, (err) => {
    if (err) {
      console.error('Error selecting database:', err);
      return;
    }
    console.log(`Database selected: ${database}`);
  });
});

const createTable = () => {
  // Create the USERS table if it doesn't exist
  const createTableQuery = `
    CREATE TABLE IF NOT EXISTS USERS (
      userID INT NOT NULL PRIMARY KEY,
      AdminStatus INT NOT NULL,
      MachineType TEXT NOT NULL,
      Date DATE NOT NULL,
      StartTime TIME NOT NULL,
      EndTime TIME NOT NULL ); `;

  connection.query(createTableQuery, (err, result) => {
    if (err) {
      console.error('ERROR creating table:', err);
      return;
    }

    if (result.warningStatus === 0) {
      console.log('Table successfully created!');
    } else {
    console.log('Existing table found.');
    }
  });
};

const readData = () => {
  // Read the data from the database
  app.get('/', (req, res) => {
      const selectQuery = 'SELECT * FROM Fablab';

      //db.all(sql, [], (err, users) => {
      connection.query(selectQuery, (err, users) => {
        if (err) {
            console.error(err.message);
            res.status(500).send('Internal Server Error');
            return;
        }
        // rows.forEach((row) => {
        //     console.log(row);
        else {
            res.render('index', { users });
        }
      });
  });
};

//createTable();
readData();

app.listen(port, () => {
    console.log(`Server is listening at http://localhost:${port}`);
  });

  // Close the MySQL connection when the application is shutting down
process.on('SIGINT', () => {
  connection.end((err) => {
    if (err) {
      console.error('Error closing MySQL connection:', err);
      process.exit(1);
    }
    console.log('MySQL connection closed');
    process.exit(0);
  });
});
