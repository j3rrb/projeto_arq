import plotly.graph_objs as go
from .models import Product, Sale
from django.db.models import Sum
from datetime import datetime

current_year = datetime.now().year

sales_query = Sale.objects.filter(timestamp__year=current_year)\
    .values('timestamp__month', 'id')\
    .annotate(total_sold=Sum('sold_price'), total_qty=Sum('sold_qty'))

products_query = Product.objects.filter(sold_qty__gt=0, bought_qty__gt=0, sale__timestamp__year=current_year)\
    .values('sale__timestamp__month')\
    .annotate(total_bought=Sum('bought_qty'), total_sold=Sum('sold_qty'))

profit_query = Product.objects.filter(sold_qty__gt=0, bought_qty__gt=0, sale__timestamp__year=current_year)\
    .values('sale__timestamp__month')\
    .annotate(profit_percent=(Sum('sale_price') - Sum('cost_price')) / Sum('cost_price') * 100)

top_products_query = Product.objects.filter(sold_qty__gt=0, sale__timestamp__year=current_year)\
    .values('name')\
    .annotate(total_sold=Sum('sold_qty'))\
    .order_by('-total_sold')[:3]

top_groups_query = Product.objects.filter(sold_qty__gt=0, sale__timestamp__year=current_year)\
    .values('group__name')\
    .annotate(total_sold=Sum('sold_qty'))\
    .filter(total_sold__gte=1000)\
    .order_by('-total_sold')[:4]

low_stock_products_query = Product.objects.filter(sold_qty__lte=10)\
    .order_by('-sold_qty')

def line_chart():
    months = list(range(1, 13))
    total_sales = [0] * 12
    total_costs = [0] * 12

    for sale_data in sales_query:
        month_index = sale_data['timestamp__month'] - 1
        total_sales[month_index] = sale_data['total_sold']
        total_costs[month_index] += sale_data['total_qty'] * Product.objects.get(id=sale_data['id']).cost_price

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=total_sales, mode='lines+markers', name='Vendas Totais'))
    fig.add_trace(go.Scatter(x=months, y=total_costs, mode='lines+markers', name='Custo Total'))

    fig.update_layout(title='Vendas e Custo Total Mensal',
                    xaxis_title='Mês',
                    yaxis_title='Valor',
                    legend_title='Tipo',
                    )
    
    return fig.to_html(full_html=False)
    
def bar_chart():
    months = list(range(1, 13))
    bought_qty = [0] * 12
    sold_qty = [0] * 12

    for product_data in products_query:
        month_index = product_data['sale__timestamp__month'] - 1
        bought_qty[month_index] += product_data['total_bought']
        sold_qty[month_index] += product_data['total_sold']

    fig = go.Figure()
    fig.add_trace(go.Bar(x=months, y=bought_qty, name='Quantidade Comprada'))
    fig.add_trace(go.Bar(x=months, y=sold_qty, name='Quantidade Vendida'))

    fig.update_layout(title='Quantidade Comprada e Vendida Mensal',
                    xaxis_title='Mês',
                    yaxis_title='Quantidade',
                    barmode='group',
                    )

    return fig.to_html(full_html=False)

def scatter_chart():
    months = list(range(1, 13))
    profit_percent = [0] * 12

    for product_data in profit_query:
        month_index = product_data['sale__timestamp__month'] - 1
        profit_percent[month_index] = product_data['profit_percent']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=profit_percent, mode='markers', name='Percentual de Lucro'))

    fig.update_layout(title='Percentual de Lucro Mensal',
                    xaxis_title='Mês',
                    yaxis_title='Percentual (%)',
                    )

    return fig.to_html(full_html=False)

def pie_chart():
    labels = [product['name'] for product in top_products_query]
    values = [product['total_sold'] for product in top_products_query]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    fig.update_layout(title='Top 3 Produtos Mais Vendidos Mensalmente')

    return fig.to_html(full_html=False)

def bar_line_chart():
    labels = [product['name'] for product in top_products_query]
    values = [product['total_sold'] for product in top_products_query]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

    fig.update_layout(title='Top 3 Produtos Mais Vendidos Mensalmente')

    return fig.to_html(full_html=False)

def table_chart():
    low_stock_products = low_stock_products_query.values('name', 'bought_qty', 'sold_qty')

    return list(low_stock_products)