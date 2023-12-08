var mysql = require('mysql')
var util = require('util')

var pool = mysql.createPool({
    connectionLimit: 10,
    host: 'sql3.freesqldatabase.com',    
    user: 'sql3667697', 
    password: '1dmeYAZjPr', 
    database: 'sql3667697',
    timezone: 'utc-6' //set CST 
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
    else {
        console.log('Database connection SUCCESS.');
    }

    //console.log(`Connected to MySQL server: ${database}`);
    if (connection) connection.release()
        return
})

// Promisify for Node.js async/await.
pool.query = util.promisify(pool.query)

module.exports = pool