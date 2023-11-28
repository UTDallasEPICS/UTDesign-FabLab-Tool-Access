const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');

const db = new sqlite3.Database('./database.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.error(err.message);
        console.error('Failed to connect to database!');
    } else {
        console.log('Connected to database successfully!');
    }
    });

const sqlFile = './Database/SQLite.sql';

// let sql = 'CREATE TABLE IF NOT EXISTS USERS (userID TEXT PRIMARY KEY, AdminStatus INTEGER, MachineType TEXT, Date TEXT, StartTime TEXT)';
// db.run(sql, [], (err) => {
//     if (err) {
//         console.error(err.message);
//         console.error('Failed to create table USERS!');
//     } else {
//         console.log('Table USERS created successfully!');
//     }
//     });

// Read the SQL commands from the file
const sql = fs.readFileSync(sqlFile, 'utf8');

//Execute the SQL commands to create tables
db.exec(sql, (execErr) => {
  if (execErr) {
    console.error(execErr.message);
    console.error('Failed to create database!');
    db.close();
  } else {
    console.log('Database created successfully!');
    // Export the database instance only after creating the tables
  }
});

module.exports = db;
