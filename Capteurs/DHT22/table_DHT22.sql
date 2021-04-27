CREATE TABLE IF NOT EXISTS dht22
(
    id serial NOT NULL,
    Session character varying,
    Date timestamp without time zone,
    Humidite double precision,
    Temperature double precision,
    Indice double precision,
    PRIMARY KEY (id)
);

ALTER TABLE public.dht22
    OWNER to postgres;