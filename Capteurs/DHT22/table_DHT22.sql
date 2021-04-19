CREATE TABLE IF NOT EXISTS DHT22
(
    Temperature double precision,
    Humidite double precision,
    DateMesure timestamp without time zone,
    Indice double precision,
    PRIMARY KEY (DateMesure)
);

ALTER TABLE DHT22
    OWNER to postgres;

-- Remarque : les noms de table/colonnes sont tous mis en 'lowercase'
