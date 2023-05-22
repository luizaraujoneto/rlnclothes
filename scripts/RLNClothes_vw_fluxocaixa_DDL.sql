-- View: public.vw_fluxocaixa

-- DROP VIEW public.vw_fluxocaixa;

CREATE OR REPLACE VIEW public.vw_fluxocaixa
 AS
 SELECT to_char(p.data, 'YYYYMM'::text) AS anomes,
    to_char(p.data, 'MM/YYYY'::text) AS mesano,
    sum(p.creditoconfirmado) AS creditoconfirmado,
    sum(p.debitoconfirmado) AS debitoconfirmado,
    sum(p.creditoconfirmado - p.debitoconfirmado) AS saldoconfirmado,
    sum(p.creditoprevisto) AS creditoprevisto,
    sum(p.debitoprevisto) AS debitoprevisto,
    sum(p.creditoconfirmado - p.debitoconfirmado + p.creditoprevisto - p.debitoprevisto) AS saldoprevisto
   FROM ( SELECT 'Crédito'::text AS tipolancamento,
            p_1.codpagamento,
            c.nomecliente AS nomepagador,
            p_1.datapagamento AS data,
                CASE
                    WHEN p_1.tipopagamento = 'P'::text THEN p_1.valorpagamento
                    ELSE 0::double precision
                END AS creditoprevisto,
                CASE
                    WHEN p_1.tipopagamento = 'C'::text THEN p_1.valorpagamento
                    ELSE 0::double precision
                END AS creditoconfirmado,
            0 AS debitoprevisto,
            0 AS debitoconfirmado,
            p_1.formapagamento,
            p_1.observacao
           FROM pagamentos p_1,
            clientes c
          WHERE p_1.codcliente = c.codcliente
        UNION
         SELECT 'Débito'::text AS tipolancamento,
            c.codcontapagar,
            f.nomefornecedor AS nomepagador,
                CASE
                    WHEN c.datapagamento IS NULL THEN c.datavencimento
                    ELSE c.datapagamento
                END AS data,
            0 AS creditoprevisto,
            0 AS creditoconfirmado,
                CASE
                    WHEN c.datapagamento IS NULL THEN c.valorparcela
                    ELSE 0::double precision
                END AS debitoprevisto,
                CASE
                    WHEN c.datapagamento IS NULL THEN 0::double precision
                    ELSE c.valorparcela
                END AS debitoconfirmado,
            c.formapagamento,
            c.observacao
           FROM contaspagar c,
            notasfiscais n,
            fornecedores f
          WHERE c.codnotafiscal = n.codnotafiscal AND n.codfornecedor = f.codfornecedor) p
  GROUP BY (to_char(p.data, 'YYYYMM'::text)), (to_char(p.data, 'MM/YYYY'::text))
  ORDER BY (to_char(p.data, 'YYYYMM'::text));

ALTER TABLE public.vw_fluxocaixa
    OWNER TO rlnclothesuser;

