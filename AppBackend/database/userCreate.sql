drop table if exists users;
drop table if exists messages;
drop table if exists outbox;

create table users(userId int auto increment,
fname varchar(20) NOT NULL,
lname varchar(20) NOT NULL,
username varchar(20) NOT NULL,
email varchar(200) NOT NULL,
password varchar(13) NOT NULL,
birthDate date NOT NULL,
gender varchar(8) NOT NULL,
mobileNo varchar(17) NOT NULL,
constraint pkc_primarykey primary key(userId,username));


CREATE TABLE IF NOT EXISTS messages (
  id INTEGER primary key AUTOINCREMENT,
  user_from int(11) NOT NULL,
  user_to int(11) NOT NULL,
  message text NOT NULL,
  status int DEFAULT false NOT NULL,
  sending_time datetime NOT NULL,
  label varchar(10) DEFAULT INBOX NOT NULL,
  label1 varchar(10) DEFAULT null NOT NULL,
  receive_time TIMESTAMP DEFAULT (datetime('now','localtime')) NOT NULL
);

CREATE TABLE IF NOT EXISTS outbox (
  id int auto increment primary key,
  user_from int(11) NOT NULL,
  user_to int(11) NOT NULL,
  message text NOT NULL,
  sending_time datetime NOT NULL,
  receive_time TIMESTAMP DEFAULT (datetime('now','localtime')) NOT NULL
);

