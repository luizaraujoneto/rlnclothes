-- Table: public.vendas

DROP TABLE IF EXISTS public.vendas CASCADE;

--codvenda, codcliente, datavenda, codproduto, valorvenda, observacao

CREATE TABLE IF NOT EXISTS public.vendas
(
    codvenda integer NOT NULL,
    codcliente integer NOT NULL,
    datavenda date NOT NULL,
	codproduto integer NOT NULL, 
    valorvenda double precision NOT NULL,
    observacao character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT vendas_pkey PRIMARY KEY (codvenda),
    CONSTRAINT fk_vendas_clientes FOREIGN KEY (codcliente)
        REFERENCES public.clientes (codcliente) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT fk_vendas_produtos FOREIGN KEY (codproduto)
        REFERENCES public.produtos (codproduto) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.vendas
    OWNER to rlnclothesuser;