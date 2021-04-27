CREATE TABLE IF NOT EXISTS public.tsl2561
(
    "id" serial NOT NULL,
    "Session" character varying,
    "DateMesure" timestamp without time zone,
    "Lux" integer,
    "LuminositeIR" integer,
    "Luminosite" integer,
	PRIMARY KEY ("id")
);

ALTER TABLE public.tsl2561
    OWNER to postgres;