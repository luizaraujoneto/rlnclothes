-- Table: public.pedidos

-- DROP TABLE IF EXISTS public.pedidos;

CREATE TABLE IF NOT EXISTS public.pedidos
(
    codpedido integer NOT NULL,
    numeropedido character varying(255) COLLATE pg_catalog."default" NOT NULL,
    codfornecedor integer NOT NULL,
    codnotafiscal integer,
    datapedido timestamp with time zone NOT NULL,
    valorpedido double precision NOT NULL,
    observacao character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT pedidos_pkey PRIMARY KEY (codpedido),
    CONSTRAINT fk_pedidos_fornecedores FOREIGN KEY (codfornecedor)
        REFERENCES public.fornecedores (codfornecedor) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT fk_pedidos_notasfiscais FOREIGN KEY (codnotafiscal)
        REFERENCES public.notasfiscais (codnotafiscal) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.pedidos
    OWNER to rlnclothesuser;