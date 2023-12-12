create database if not exists fablab;
use fablab;

create table timelog (
  logID int AUTO_INCREMENT PRIMARY KEY NOT NULL,
  userID varchar(20) not null,
  adminStatus int NOT NULL,
  machineType varchar(255) not null,
  date date not null,
  startTime time not null,
  endTime time not null
);

GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY 'root' WITH GRANT OPTION;
