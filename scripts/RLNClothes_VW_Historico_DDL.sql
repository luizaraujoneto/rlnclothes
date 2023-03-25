-- View: public.vw_historicocliente

-- DROP VIEW public.vw_historicocliente;

CREATE OR REPLACE VIEW public.vw_historicocliente
 AS
 SELECT (v.codcliente || 'V'::text) || v.codvenda AS id,
    v.codcliente,
    'V'::text AS tipooperacao,
    v.codvenda AS codoperacao,
    v.datavenda AS data,
    p.codproduto,
    p.descricao,
    p.valorcusto,
    v.valorvenda,
    v.observacao,
    1 AS ordem
   FROM vendas v,
    produtos p
  WHERE v.codproduto = p.codproduto
UNION
 SELECT (p.codcliente || 'P'::text) || p.codpagamento AS id,
    p.codcliente,
    'P'::text AS tipooperacao,
    p.codpagamento AS codoperacao,
    p.datapagamento AS data,
    NULL::integer AS codproduto,
    p.formapagamento AS descricao,
    0 AS valorcusto,
    p.valorpagamento AS valorvenda,
    p.observacao,
    2 AS ordem
   FROM pagamentos p
  WHERE p.tipopagamento = 'C'::text
  ORDER BY 1, 5, 11, 7;

ALTER TABLE public.vw_historicocliente
    OWNER TO rlnclothesuser;

