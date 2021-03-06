drop table if exists users;
drop table if exists messages;
drop table if exists outbox;
drop table if exists requestsWatcher;
drop table if exists requestsCompression;
drop table if exists requestsValidator;

CREATE  TABLE IF NOT EXISTS  requestsWatcher(filename varchar(30),
    data json,
    updateFlag int default 0);

CREATE TABLE IF NOT EXISTS requestsCompression(filename varchar(30),
    compressdata bytea,
    updateFlag int default 0);

CREATE TABLE IF NOT EXISTS requestsValidator(filename varchar(30),
    data json,
    updateFlag int default 0);

create table users(userId serial,
fname varchar(20) NOT NULL,
lname varchar(20) NOT NULL,
username varchar(20) NOT NULL,
email varchar(200) NOT NULL,
password varchar(13) NOT NULL,
birthDate date NOT NULL,
gender varchar(8) NOT NULL,
mobileNo varchar(20) NOT NULL,
constraint pkc_primarykey primary key(userId,username));


CREATE TABLE IF NOT EXISTS messages (
  id serial primary key,
  user_from varchar(11) NOT NULL,
  user_to varchar(11) NOT NULL,
  subject varchar(20),
  message text NOT NULL,
  status int DEFAULT 0 NOT NULL,
  label varchar(20) DEFAULT 'INBOX' NOT NULL,
  sending_time timestamp NOT NULL,
  receive_time TIMESTAMP DEFAULT (now()::timestamp) NOT NULL 
);

CREATE TABLE IF NOT EXISTS outbox (
  id serial primary key,
  user_from varchar(30) NOT NULL,
  user_to varchar(30) NOT NULL,
  subject varchar(20),
  message text NOT NULL,
  status int DEFAULT 0 NOT NULL,
  label varchar(20) DEFAULT 'DRAFT' NOT NULL,
  sending_time timestamp NOT NULL,
  receive_time TIMESTAMP DEFAULT (now()::timestamp) NOT NULL
);

CREATE SEQUENCE slnextValue;

SELECT setval('slnextValue', 100);

CREATE TABLE IF NOT EXISTS label(
  labelid text PRIMARY KEY CHECK (labelid ~ '^sl[0-9]+$' ) DEFAULT 'sl'  || nextval('slnextValue'),
  labelName varchar(20) NOT NULL,
  subject varchar(20) NOT NULL,
  username varchar(20) REFERENCES users,
  users text NOT NULL
);

CREATE SEQUENCE hlnextValue;

SELECT setval('hlnextValue', 100);

CREATE TABLE IF NOT EXISTS labelHirarchy(
  labelHid text PRIMARY KEY CHECK (labelHid ~ '^hl[0-9]+$' ) DEFAULT 'hl'  || nextval('hlnextValue'),
  parent_id text NOT NULL,		
  labelName varchar(20) NOT NULL,
  subject varchar(20) NOT NULL,
  username varchar(20) REFERENCES users,
  users text NOT NULL
);

CREATE SEQUENCE value1;

SELECT setval('value1', 100);


create table if not exists event(
eventId text PRIMARY KEY CHECK (eventId ~ '^[0-9]+$' ) || nextval('value1'),
username varchar(20) REFERENCES users,
eventName varchar(70) not null,
location varchar(50) not null,
datetime timestamp not null,
discription text not null,
invitedUser text);

