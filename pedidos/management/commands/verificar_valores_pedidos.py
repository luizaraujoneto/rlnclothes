"""
Comando de gerenciamento Django para verificar pedidos com valores incorretos.

Este comando analisa todos os pedidos e identifica aqueles cujo valor gravado
(valorpedido) não corresponde à soma dos produtos ou devoluções associados,
dependendo do tipo do pedido.

Uso:
    python manage.py verificar_valores_pedidos [--apenas-significativos]
"""

from django.core.management.base import BaseCommand
from django.db.models import Sum
from pedidos.models import Pedidos, Produtos, Devolucoes
from decimal import Decimal


class Command(BaseCommand):
    help = 'Identifica pedidos com valor divergente entre valorpedido e soma dos produtos/devoluções'

    def add_arguments(self, parser):
        parser.add_argument(
            '--apenas-significativos',
            action='store_true',
            help='Mostra apenas divergências maiores que R$ 0.01 (ignora diferenças de arredondamento)',
        )

    def handle(self, *args, **options):
        """Executa a verificação de valores dos pedidos."""
        apenas_significativos = options.get('apenas_significativos', False)
        
        self.stdout.write(self.style.WARNING('Iniciando verificacao de valores dos pedidos...'))
        self.stdout.write('')
        
        # Busca todos os pedidos
        pedidos = Pedidos.objects.all().select_related('fornecedor')
        
        divergencias = []
        total_pedidos = pedidos.count()
        pedidos_verificados = 0
        
        for pedido in pedidos:
            pedidos_verificados += 1
            
            # Calcula o valor esperado baseado no tipo do pedido
            if pedido.tipopedido == 'C':
                # Pedido de Compra: soma dos produtos
                valor_calculado = Produtos.objects.filter(
                    pedido__codpedido=pedido.codpedido
                ).aggregate(
                    total=Sum('valorcusto')
                )['total'] or Decimal('0.00')
                
            elif pedido.tipopedido == 'D':
                # Pedido de Devolução: soma das devoluções
                valor_calculado = Devolucoes.objects.filter(
                    pedido__codpedido=pedido.codpedido
                ).aggregate(
                    total=Sum('produto__valorcusto')
                )['total'] or Decimal('0.00')
                
            else:
                # Tipo desconhecido
                self.stdout.write(
                    self.style.ERROR(
                        f'[!] Pedido {pedido.numeropedido} tem tipo desconhecido: {pedido.tipopedido}'
                    )
                )
                continue
            
            # Converte para Decimal para comparação precisa
            valor_gravado = Decimal(str(pedido.valorpedido))
            valor_calculado = Decimal(str(valor_calculado))
            
            # Verifica se há divergência
            diferenca = valor_gravado - valor_calculado
            
            # Se apenas_significativos, ignora diferenças menores que 0.01
            if apenas_significativos and abs(diferenca) <= Decimal('0.01'):
                continue
            
            if valor_gravado != valor_calculado:
                divergencias.append({
                    'numero': pedido.numeropedido or f'Pedido #{pedido.codpedido}',
                    'data': pedido.datapedido,
                    'tipo': 'Compra' if pedido.tipopedido == 'C' else 'Devolucao',
                    'valorpedido': valor_gravado,
                    'valorprodutos': valor_calculado,
                    'diferenca': diferenca
                })
        
        # Exibe os resultados
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'[OK] Verificacao concluida: {pedidos_verificados} pedidos analisados'))
        self.stdout.write('')
        
        if divergencias:
            titulo = 'divergencia(s) significativa(s)' if apenas_significativos else 'divergencia(s)'
            self.stdout.write(
                self.style.ERROR(f'[ERRO] Encontradas {len(divergencias)} {titulo}:')
            )
            self.stdout.write('')
            self.stdout.write('-' * 120)
            self.stdout.write(
                f'{"Numero do Pedido":<25} {"Data":<12} {"Tipo":<12} '
                f'{"Valor Gravado":>15} {"Valor Calculado":>15} {"Diferenca":>15}'
            )
            self.stdout.write('-' * 120)
            
            for div in divergencias:
                data_str = div['data'].strftime('%d/%m/%Y') if div['data'] else 'Sem data'
                diferenca_str = f"{div['diferenca']:+.2f}"
                
                self.stdout.write(
                    f"{div['numero']:<25} {data_str:<12} {div['tipo']:<12} "
                    f"R$ {div['valorpedido']:>12.2f} R$ {div['valorprodutos']:>12.2f} "
                    f"R$ {diferenca_str:>12}"
                )
            
            self.stdout.write('-' * 120)
            self.stdout.write('')
            
            # Estatísticas
            total_diferenca = sum(abs(d['diferenca']) for d in divergencias)
            self.stdout.write(f'Total de diferencas (absoluto): R$ {total_diferenca:.2f}')
            
        else:
            mensagem = 'Nenhuma divergencia significativa encontrada!' if apenas_significativos else 'Nenhuma divergencia encontrada!'
            self.stdout.write(
                self.style.SUCCESS(f'[OK] {mensagem} Todos os pedidos estao corretos.')
            )
        
        self.stdout.write('')
