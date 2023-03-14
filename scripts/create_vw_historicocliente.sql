-- View: public.vw_historicocliente

-- DROP VIEW public.vw_historicocliente;
/*
CREATE OR REPLACE VIEW public.vw_historicocliente
 AS
 SELECT (v.codcliente || 'V'::text) || iv.coditemvenda AS id,
    v.codcliente,
    'V'::text AS tipooperacao,
    iv.coditemvenda AS codoperacao,
    v.datavenda AS data,
    p.descricao,
    iv.valorvenda AS valor,
    iv.observacao
   FROM itemvenda iv,
    vendas v,
    produtos p
  WHERE iv.codvenda = v.codvenda AND iv.codproduto = p.codproduto
UNION
 SELECT (p.codcliente || 'P'::text) || p.codpagamento AS id,
    p.codcliente,
    'P'::text AS tipooperacao,
    p.codpagamento AS codoperacao,
    p.data,
    formapagamento AS descricao,
    p.valor,
    observacao AS observacao
   FROM pagamentos p
  WHERE p.tipopagamento = 'C'::text
  ORDER BY 4;

ALTER TABLE public.vw_historicocliente
    OWNER TO rlnclothesuser;

*/