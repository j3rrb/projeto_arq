import plotly.express as px


def line_chart():
    df = px.data.gapminder().query("country=='Canada'")

    fig = px.line(df, x="year", y="lifeExp", title="Life expectancy in Canada")
    fig.show()


def bar_chart():
    pass


def scatter_chart():
    pass


def pie_chart():
    pass


def bars_and_lines_chart():
    pass


def table_chart():
    pass
