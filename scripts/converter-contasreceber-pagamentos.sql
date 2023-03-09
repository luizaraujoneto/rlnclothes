drop table pagamentos cascade;

create table pagamentos as 
select max(cr.codcontareceber) codpagamento, v.codcliente, 'C' as tipopagamento, cr.datapagamento data, sum( cr.valorpago ) as valor, cr.formapagamento, cr.observacao
from contasreceber cr, 
     vendas v,
	 clientes c
where cr.codvenda = v.codvenda
and v.codcliente = c.codcliente
and not cr.datapagamento is null 
group by cr.codcontareceber, v.codcliente, cr.datapagamento, cr.formapagamento, cr.observacao
union 
select max(cr.codcontareceber) codpagamento, v.codcliente, 'P' as tipopagamento, cr.datapagamento as data, sum( cr.valorparcela ) as valor, cr.formapagamento, cr.observacao
from contasreceber cr, 
     vendas v,
	 clientes c
where cr.codvenda = v.codvenda
and v.codcliente = c.codcliente
and cr.datapagamento is null 
group by v.codcliente, cr.datapagamento, cr.formapagamento, cr.observacao;

