select 
	to_char( p.data, 'YYYYMM' ) as anomes,
	to_char( p.data, 'MM/YYYY') as mesano,
	tipolancamento, 
	tipopagamento,
	sum(valor) as valorpago
from (
select 'Crédito' as tipolancamento, 
    p.codpagamento,
	c.nomecliente as nomepagador,
	case 
	   when p.tipopagamento = 'P' then 'Previsto'
	   else 'Confirmado' 
	end AS tipopagamento,
	p.datapagamento as data,
	p.valorpagamento as valor,
	p.formapagamento,
	p.observacao
from pagamentos p, 
	clientes c
where p.codcliente = c.codcliente
union
select 'Débito' as tipolancamento,
	c.codcontapagar, 
	f.nomefornecedor as nomepagador,
	case 
	   when c.datapagamento is null 
	   then 'Previsto'
	   else 'Confirmado' 
	end AS tipopagamento,
	case 
	   when c.datapagamento is null 
	   then datavencimento
	   else datapagamento 
	end AS data,
	c.valorparcela as valor,
	c.formapagamento,
	c.observacao
from contaspagar c,
     notasfiscais n,
	 fornecedores f
where c.codnotafiscal = n.codnotafiscal
  and n.codfornecedor = f.codfornecedor
 ) as p
group by 
	to_char( p.data, 'YYYYMM' ),
	to_char( p.data, 'MM/YYYY'),
	tipolancamento, 
	tipopagamento
order by 1
