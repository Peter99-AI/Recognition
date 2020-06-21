create database Recognition

use Recognition

create table People(
	id int primary key NOT NULL AUTO_INCREMENT,
    name varchar(255),
    age int,
    gender varchar(255))
