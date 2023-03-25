-- Table: public.clientes

-- DROP TABLE IF EXISTS public.clientes;

CREATE TABLE IF NOT EXISTS public.clientes
(
    codcliente integer NOT NULL,
    nomecliente character varying(255) COLLATE pg_catalog."default" NOT NULL,
    telefone character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT clientes_pkey PRIMARY KEY (codcliente)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.clientes
    OWNER to rlnclothesuser;