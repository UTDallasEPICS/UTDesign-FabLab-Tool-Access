var mysql = require('mysql')
//var mysql = require('mysql2/promise');
var util = require('util')

var pool = mysql.createPool({
    connectionLimit: 10,
    host: 'sql3.freesqldatabase.com',    
    user: 'sql3667697', 
    password: '1dmeYAZjPr', 
    database: 'sql3667697',
    timezone: '-06:00' //set CST 
})

pool.getConnection((err, connection) => {
    if (err) {
        if (err.code === 'PROTOCOL_CONNECTION_LOST') {
            console.error('Database connection was closed.')
        }
        if (err.code === 'ER_CON_COUNT_ERROR') {
            console.error('Database has too many connections.')
        }
        if (err.code === 'ECONNREFUSED') {
            console.error('Database connection was refused.')
        }
        console.error('Database connection FAIL. \n', err)
    }

    //console.log(`Connected to MySQL server: ${database}`);
    if (connection) {
        connection.release() 
        console.log('Database connection SUCCESS.');
        return;
    }
})

// Promisify for Node.js async/await.
pool.query = util.promisify(pool.query)

// Function to clear records older than 5 years
const clearOldRecords = async () => {
    try {
        const deleteQuery = 'DELETE FROM Fablab WHERE Date < DATE_SUB(NOW(), INTERVAL 5 YEAR)';
        const result = await pool.query(deleteQuery);
        if (result.affectedRows > 0)
            console.log('Old records deleted successfully.');
    } catch (error) {
        console.error('Error deleting old records:', error.message);
    }
};

  // Call the function to clear old records
  clearOldRecords();

module.exports = pool