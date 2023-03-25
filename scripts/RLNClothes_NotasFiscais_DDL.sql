-- Table: public.notasfiscais

-- DROP TABLE IF EXISTS public.notasfiscais;

CREATE TABLE IF NOT EXISTS public.notasfiscais
(
    codnotafiscal integer NOT NULL,
    numeronotafiscal character varying(255) COLLATE pg_catalog."default" NOT NULL,
    codfornecedor integer NOT NULL,
    datanotafiscal timestamp with time zone NOT NULL,
    valornotafiscal double precision NOT NULL,
    observacao character varying(255) COLLATE pg_catalog."default",
    formapagamento character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT notasfiscais_pkey PRIMARY KEY (codnotafiscal),
    CONSTRAINT fk_notasfiscais_fornecedores FOREIGN KEY (codfornecedor)
        REFERENCES public.fornecedores (codfornecedor) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.notasfiscais
    OWNER to rlnclothesuser;