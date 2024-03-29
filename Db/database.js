var mysql = require('mysql');
var util = require('util');

var host = process.env.DOCKER === 'true' ? 'db' : 'localhost';

var pool = mysql.createPool({
    connectionLimit: 10,
    host,    
    user: 'root', 
    password: 'root', 
    database: 'fablab', 
    timezone: '-06:00', //set CST 
});

pool.getConnection((err, connection) => {
    if (err) {
        if (err.code === 'PROTOCOL_CONNECTION_LOST') {
            console.error('Database connection was closed.');
        }
        if (err.code === 'ER_CON_COUNT_ERROR') {
            console.error('Database has too many connections.');
        }
        if (err.code === 'ECONNREFUSED') {
            console.error('Database connection was refused.');
        }
        console.error('Database connection FAIL. \n', err);
    }

    if (connection) {
        connection.release();
        console.log('Database connection SUCCESS.');
        return;
    }
})

// Promisify for Node.js async/await.
pool.query = util.promisify(pool.query);

module.exports = pool;
