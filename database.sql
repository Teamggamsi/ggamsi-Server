create table likes
(
    id      int auto_increment
        primary key,
    article int null,
    author  int null
);

create table products
(
    id       int auto_increment
        primary key,
    title    varchar(50) null,
    content  longtext    null,
    delivery int         null,
    price    int         null,
    tag      varchar(50) null,
    image    mediumtext  null,
    author   varchar(50) null
);

create table users
(
    id       int auto_increment
        primary key,
    email    text        null,
    password text        null,
    nickname varchar(50) null
);

