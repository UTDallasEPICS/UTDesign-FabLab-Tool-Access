const mysql = require('mysql');

const pool = mysql.createPool({
  connectionLimit: 10,
  host: 'db', // MySQL service name in Docker Compose or use the IP/hostname of your MySQL server
  user: 'root',
  password: 'root',
  database: 'fablab',
  timezone: '-06:00', // set CST
});

const healthcheck = () => {
  return new Promise((resolve, reject) => {
    pool.getConnection((err, connection) => {
      if (err) {
        return reject(err);
      }
      connection.release();
      resolve();
    });
  });
};

const tryConnect = async () => {
  let i;
  for (i = 0; i < 5; i++) {
    try {
      await healthcheck();
      console.log('Database is up, starting the application...');
      pool.end();
      process.exit(0);
    } catch (err) {
      if (i === 0) {
        console.error('Waiting for the database...');
      }
      else {
          console.error('Cannot connect to the database, retrying...');
      }
      await sleep(2000);
    }
  }
  console.error('Unable to connect to the database, exiting...');
  process.exit(1);
};

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

tryConnect();
