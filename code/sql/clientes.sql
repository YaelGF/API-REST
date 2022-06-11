Drop table if exists clientes;

Create table clientes(
    id_cliente integer primary key autoincrement,
    nombre varchar(50) not null,
    email varchar(50) not null
);

insert into clientes(nombre,email) values ("Nombre","nombre@email.com");

insert into clientes(nombre,email) values ("Yael","yael@email.com");
insert into clientes(nombre,email) values ("Erick","erick@email.com");
insert into clientes(nombre,email) values ("Mauricio","mau@email.com");

.headers ON

Select * From clientes;