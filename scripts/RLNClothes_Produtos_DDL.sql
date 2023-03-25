-- Table: public.produtos

-- DROP TABLE IF EXISTS public.produtos;

CREATE TABLE IF NOT EXISTS public.produtos
(
    codproduto integer NOT NULL,
    codpedido integer NOT NULL,
    codprodutofornecedor character varying(255) COLLATE pg_catalog."default",
    referencia character varying(255) COLLATE pg_catalog."default",
    descricao character varying(255) COLLATE pg_catalog."default" NOT NULL,
    valorcusto double precision NOT NULL,
    CONSTRAINT produtos_pkey PRIMARY KEY (codproduto),
    CONSTRAINT fk_produtos_pedidos FOREIGN KEY (codpedido)
        REFERENCES public.pedidos (codpedido) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.produtos
    OWNER to rlnclothesuser;