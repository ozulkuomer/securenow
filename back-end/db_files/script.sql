create table auths
(
    email           varchar(50) charset utf8  not null,
    password_hashed varchar(200) charset utf8 not null,
    user_id         int                       not null,
    constraint auths_email_uindex
        unique (email),
    constraint auths_user_id_uindex
        unique (user_id)
);

create table users
(
    _id      int auto_increment,
    username varchar(50) charset utf8 not null,
    email    varchar(50) charset utf8 not null,
    constraint users__id_uindex
        unique (_id),
    constraint users_email_uindex
        unique (email),
    constraint users_username_uindex
        unique (username)
);

alter table users
    add primary key (_id);

create table statuses
(
    _id     int auto_increment,
    text    varchar(140) charset utf8 not null,
    user_id int                       not null,
    constraint table_name__id_uindex
        unique (_id),
    constraint user_id
        foreign key (user_id) references users (_id)
);

create table likes
(
    _id         int auto_increment,
    user_id     int                  not null,
    status_id   int                  not null,
    is_archived tinyint(1) default 0 not null,
    constraint likes__id_uindex
        unique (_id),
    constraint likes_pk
        unique (user_id, status_id),
    constraint likes_statuses__id_fk
        foreign key (status_id) references statuses (_id),
    constraint likes_users__id_fk
        foreign key (user_id) references users (_id)
);

alter table likes
    add primary key (_id);


