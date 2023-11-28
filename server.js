const fs = require('fs');
const db = require('./Database/db'); // Import the SQLite database module
const express = require('express'); // Import the ExpressJS framework
let sql;

const app = express();
const port = 3000;

app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/public'));

// Read from file
const jsonUserData = fs.readFileSync('userdata.json', 'utf8');
const userData = JSON.parse(jsonUserData);

// Insert data into the database
const insertData = () => {
    // Begin a transaction
    //db.run('BEGIN TRANSACTION');

    for (const { userID, adminStatus } of userData) {
        sql = 'INSERT INTO USERS (userID, AdminStatus, MachineType, Date, StartTime) VALUES (?, ?, ?, ?, ?)';
        db.run(
        sql, 
        [userID, adminStatus, 'SampleMachine', '2023-01-01', '12:00:00'],
        (err) => {
          if (err) {
            console.error(err.message);
          } else {
            console.log(`Data inserted for userID: ${userID}`);
          }
        }
        );
    }
    // Commit the transaction
    //db.run('COMMIT');
};

const readData = () => {
// Read the data from the database
app.get('/', (req, res) => {
    sql = 'SELECT * FROM USERS';
    db.all(sql, [], (err, users) => {
        if (err) {
            console.error(err.message);
            res.status(500).send('Internal Server Error');
        }
        // rows.forEach((row) => {
        //     console.log(row);
        else {
            res.render('index', { users });
        }
    });
});
};

//insertData();
readData();

app.listen(port, () => {
    console.log(`Server is listening at http://localhost:${port}`);
  });