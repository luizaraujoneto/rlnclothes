-- Table: public.fornecedores

-- DROP TABLE IF EXISTS public.fornecedores;

CREATE TABLE IF NOT EXISTS public.fornecedores
(
    codfornecedor integer NOT NULL,
    nomefornecedor character varying(255) COLLATE pg_catalog."default" NOT NULL,
    telefone character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT fornecedores_pkey PRIMARY KEY (codfornecedor)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.fornecedores
    OWNER to rlnclothesuser;