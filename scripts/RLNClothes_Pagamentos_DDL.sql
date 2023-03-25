-- Table: public.pagamentos

-- DROP TABLE IF EXISTS public.pagamentos;

CREATE TABLE IF NOT EXISTS public.pagamentos
(
    codpagamento integer NOT NULL,
    codcliente integer,
    tipopagamento text COLLATE pg_catalog."default",
    datapagamento date,
    valorpagamento double precision,
    formapagamento character varying(255) COLLATE pg_catalog."default",
    observacao character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT pk_pagamentos PRIMARY KEY (codpagamento),
    CONSTRAINT fk_pagamentos_cliente FOREIGN KEY (codcliente)
        REFERENCES public.clientes (codcliente) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT ck_tipopagamento CHECK (tipopagamento = ANY (ARRAY['C'::text, 'P'::text])) NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.pagamentos
    OWNER to rlnclothesuser;