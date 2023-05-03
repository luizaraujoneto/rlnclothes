-- Table: public.devolucoes

-- DROP TABLE IF EXISTS public.devolucoes;

CREATE TABLE IF NOT EXISTS public.devolucoes
(
    coddevolucao integer NOT NULL,
    codpedido integer NOT NULL,
    codproduto integer NOT NULL,
    CONSTRAINT pk_devolucoes PRIMARY KEY (coddevolucao),
    CONSTRAINT uk_codproduto UNIQUE (codproduto),
    CONSTRAINT fk_devolucoes_pedido FOREIGN KEY (codpedido)
        REFERENCES public.pedidos (codpedido) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_devolucoes_produto FOREIGN KEY (codproduto)
        REFERENCES public.produtos (codproduto) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.devolucoes
    OWNER to rlnclothesuser;