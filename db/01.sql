CREATE DATABASE IF NOT EXISTS test_db;
use test_db;
create table if not exists users(id int not null auto_increment primary key, username varchar(100),password varchar(100),unique(username));
create table if not exists tasks(id int not null auto_increment primary key,title varchar(100),stack varchar(100),mentors varchar(100),user_id int ,foreign key(user_id) references users(id) on delete cascade);
