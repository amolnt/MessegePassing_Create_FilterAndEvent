drop table if exists requestsWatcher;
drop table if exists requestsValidator;

CREATE  TABLE IF NOT EXISTS  requestsWatcher(filename varchar(30),
    data json,
    updateFlag int default 0);

CREATE TABLE IF NOT EXISTS requestsValidator(filename varchar(30),
    data json,
    updateFlag int default 0);
