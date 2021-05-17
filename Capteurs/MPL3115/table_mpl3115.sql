CREATE TABLE IF NOT EXISTS mpl3115
(
    "id" serial NOT NULL,
    "Session" character varying,
    "DateMesure" timestamp without time zone,
    "Pression" double precision,
    "Altitude" double precision,
    "Temperature" double precision,
	PRIMARY KEY ("id")
);

ALTER TABLE mpl3115
    OWNER to postgres;