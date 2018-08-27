DROP USER IF EXISTS 'TuVid'@'localhost';
CREATE USER IF NOT EXISTS 'TuVid'@'localhost' IDENTIFIED BY 'TuVid';

DROP DATABASE IF EXISTS TuVid;
CREATE DATABASE IF NOT EXISTS TuVid DEFAULT CHARACTER SET utf8 ;

GRANT ALL PRIVILEGES ON TuVid.* TO 'TuVid'@'localhost';
FLUSH PRIVILEGES;

USE TuVid;

DROP TABLE IF EXISTS Cuenta;
CREATE TABLE IF NOT EXISTS Cuenta (
    idCuenta INT NOT NULL UNIQUE AUTO_INCREMENT,
    usuario VARCHAR (255) NOT NULL UNIQUE,
    contrasenia VARCHAR (255) NOT NULL,
    PRIMARY KEY (idCuenta)
);

USE TuVid;

DROP TABLE IF EXISTS Video;
CREATE TABLE IF NOT EXISTS Video (
    idVideo INT NOT NULL UNIQUE AUTO_INCREMENT,
    titulo VARCHAR (255) NOT NULL,
    ubicacionVideo VARCHAR (255) NOT NULL,
    ubicacionThumbnail VARCHAR (255) NOT NULL,
    descripcion BLOB NULL DEFAULT NULL,
    fechaSubida DATETIME NOT NULL,
    idCuenta INT NOT NULL,
    PRIMARY KEY (idVideo),
    FOREIGN KEY (idCuenta) REFERENCES Cuenta (idCuenta)
);

USE TuVid;

DROP TABLE IF EXISTS TipoInteraccion;
CREATE TABLE IF NOT EXISTS TipoInteraccion (
    idTipoInteraccion INT NOT NULL UNIQUE AUTO_INCREMENT,
    nombreInteraccion VARCHAR (255) NOT NULL UNIQUE,
    PRIMARY KEY  (idTipoInteraccion)
);

USE TuVid;

INSERT INTO TipoInteraccion (nombreInteraccion) VALUES ('visita');
INSERT INTO TipoInteraccion (nombreInteraccion) VALUES ('buscado');

USE TuVid;

DROP TABLE IF EXISTS Interaccion;
CREATE TABLE IF NOT EXISTS Interaccion (
    idInteraccion INT NOT NULL UNIQUE AUTO_INCREMENT,
    idCuenta INT NULL,
    idVideo INT NOT NULL,
    idTipoInteraccion INT NOT NULL,
    PRIMARY KEY (idInteraccion),
    FOREIGN KEY (idCuenta) REFERENCES Cuenta (idCuenta),
    FOREIGN KEY (idVideo) REFERENCES Video (idVideo),
    FOREIGN KEY (idTipoInteraccion) REFERENCES TipoInteraccion (idTipoInteraccion)
);

USE TuVid;

DROP TABLE IF EXISTS Comentario;
CREATE TABLE IF NOT EXISTS Comentario (
    idComentario INT NOT NULL UNIQUE AUTO_INCREMENT,
    contenido BLOB NOT NULL,
    fechaComentario DATETIME NOT NULL,
    idCuenta INT NOT NULL,
    idVideo INT NOT NULL,
    PRIMARY KEY (idComentario),
    FOREIGN KEY (idCuenta) REFERENCES Cuenta (idCuenta),
    FOREIGN KEY (idVideo) REFERENCES Video (idVideo)
);

USE TuVid;

DROP TABLE IF EXISTS Notificacion;
CREATE TABLE IF NOT EXISTS Notificacion(
    idNotificacion INT NOT NULL UNIQUE AUTO_INCREMENT,
    contenido VARCHAR (255) NOT NULL,
    fechaNotificacion DATETIME NOT NULL,
    visto TINYINT NOT NULL,
    idCuenta INT NOT NULL,
    PRIMARY KEY (idNotificacion),
    FOREIGN KEY (idCuenta) REFERENCES Cuenta (idCuenta)
);

USE TuVid;

CREATE OR REPLACE VIEW NumeroVisitas AS
    SELECT
		i.idVideo,
		count(*) as visitas
	FROM 
		Interaccion i 
    WHERE 
		i.idTipoInteraccion = 1 
	GROUP BY 
		i.idVideo;


USE TuVid;

CREATE OR REPLACE VIEW Thumbnail AS
	SELECT
		v.idVideo as id,
		v.idVideo as idVideo,
        v.titulo as titulo,
        v.ubicacionThumbnail as ubicacionThumbnail,
        v.ubicacionVideo as ubicacionVideo,
        c.usuario as usuario,
        nv.visitas as visitas,
        v.fechaSubida as fecha
	FROM
		Video v
	JOIN
		Cuenta c ON v.idCuenta = c.idCuenta
    LEFT JOIN
		NumeroVisitas nv ON v.idVideo = nv.idVideo;

USE TuVid;

CREATE OR REPLACE VIEW VideoDetalle AS
    SELECT
		v.idVideo as id,
        v.idVideo as idVideo,
        v.titulo as titulo,
        v.ubicacionThumbnail as ubicacionThumbnail,
        v.ubicacionVideo as ubicacionVideo,
        c.usuario as usuario,
        nv.visitas as visitas,
        v.fechaSubida as fecha,
        v.descripcion as descripcion
    FROM
        Video v
	JOIN
		Cuenta c ON v.idCuenta = c.idCuenta
	LEFT JOIN
		NumeroVisitas nv ON v.idVideo = nv.idVideo;

USE TuVid;

CREATE OR REPLACE VIEW MasVistos AS
	SELECT
		t.*
	FROM
		Thumbnail t
	ORDER BY
		visitas
	DESC;

USE TuVid;

CREATE OR REPLACE VIEW Recientes AS
	SELECT
		t.*
	FROM
		Thumbnail t
	ORDER BY
		fecha
	DESC;

USE TuVid;

CREATE OR REPLACE VIEW NumeroBusquedas AS
    SELECT
		i.idVideo,
		count(*) as busquedas
	FROM 
		Interaccion i 
    WHERE 
		i.idTipoInteraccion = 2 
	GROUP BY 
		i.idVideo;

USE TuVid;

CREATE OR REPLACE VIEW MasBuscados AS
	SELECT
		t.*
	FROM
		Thumbnail t
	LEFT JOIN
		NumeroBusquedas nb ON t.idVideo = nb.idVideo
    ORDER BY
        t.visitas
    DESC;
    
USE TuVid;
    
CREATE OR REPLACE VIEW NotificacionesOrdenadas AS
	SELECT
		n.idnotificacion as id,
		n.*
	FROM
		Notificacion n
	ORDER BY
		n.fechaNotificacion
	DESC;
