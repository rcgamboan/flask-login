drop table if exists usuarios;
    create table usuarios (
    id integer primary key autoincrement,
    username VARCHAR(20) unique not null,
    password CHAR(102) not null,
    isAdmin INT DEFAULT 0
);