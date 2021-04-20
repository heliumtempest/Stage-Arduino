CREATE TABLE IF NOT EXISTS public.tsl2561
(
    "DateMesure" time without time zone,
    "Lux" integer,
    "LuminositeIR" integer,
    "Luminosite" integer,
	PRIMARY KEY ("DateMesure")
);

ALTER TABLE public.tsl2561
    OWNER to postgres;