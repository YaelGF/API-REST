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

Drop table if exists usuarios;
CREATE TABLE usuarios(
    username TEXT,
    password varchar(32),
    level varchar(5)
);

CREATE UNIQUE INDEX index_usuario ON usuarios(username);

INSERT INTO usuarios(username, password, level) VALUES('admin','21232f297a57a5a743894a0e4a801fc3','Admin');
INSERT INTO usuarios(username, password, level) VALUES('user','ee11cbb19052e40b07aac0ca060c23ee','user');

SELECT * FROM usuarios;