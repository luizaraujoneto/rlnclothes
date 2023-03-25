-- Table: public.contaspagar

-- DROP TABLE IF EXISTS public.contaspagar;

CREATE TABLE IF NOT EXISTS public.contaspagar
(
    codcontapagar integer NOT NULL,
    codnotafiscal integer NOT NULL,
    parcela character varying(10) COLLATE pg_catalog."default",
    datavencimento timestamp with time zone NOT NULL,
    valor double precision NOT NULL,
    datapagamento timestamp with time zone,
    formapagamento character varying(255) COLLATE pg_catalog."default",
    observacao character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT contaspagar_pkey PRIMARY KEY (codcontapagar),
    CONSTRAINT fk_contaspagar_notafiscal FOREIGN KEY (codnotafiscal)
        REFERENCES public.notasfiscais (codnotafiscal) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.contaspagar
    OWNER to rlnclothesuser;