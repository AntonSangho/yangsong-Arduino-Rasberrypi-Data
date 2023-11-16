from dash import Dash, html, dcc
import pandas as pd
import pymysql
import datetime
from dash.dependencies import Output, Input

conn = pymysql.connect(
    host="127.0.0.1",
    user="song1",
    password="1q2w3e4r",
    db="yangsong2",
    charset="utf8",
    autocommit=True,
    cursorclass=pymysql.cursors.DictCursor,
)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?" "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "양송이 데이터"


def serve_layout():
    cur = conn.cursor()
    cur.execute("select stamp from yangsong2.yang1 limit 1")
    result = cur.fetchone()
    min_date = result["stamp"].date()
    cur.execute("select stamp from yangsong2.yang1 order by id desc limit 1")
    result = cur.fetchone()
    max_date = result["stamp"].date()
    return html.Div(
        children=[
            html.Div(
                children=[
                    html.P(
                        children="📈",
                        className="header_emoji",
                    ),
                    html.H1(
                        children="양송이 데이터",
                        className="header_title",
                    ),
                    html.P(
                        children="이산화탄소, 온도, 습도",
                        className="header_description",
                    ),
                ],
                className="header",
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children="데이터", className="menu-title"),
                            dcc.Dropdown(
                                id="type-filter",
                                options=[
                                    {"label": "이산화탄소", "value": "co2"},
                                    {"label": "온도", "value": "temperature"},
                                    {"label": "습도", "value": "humidity"},
                                ],
                                value="co2",
                                clearable=False,
                                searchable=False,
                                className="dropdown",
                            ),
                        ],
                    ),
                    html.Div(
                        children=[
                            html.Div(children="날짜", className="menu-title"),
                            dcc.DatePickerSingle(
                                id="date-single",
                                min_date_allowed=min_date,
                                max_date_allowed=max_date,
                                initial_visible_month=max_date,
                                date=max_date,
                            ),
                        ]
                    ),
                    dcc.Interval(id="interval-component", interval=60000, n_intervals=0),
                ],
                className="menu",
            ),
            html.Div(
                children=[
                    html.Div(
                        dcc.Graph(
                            id="data-chart",
                            config={"displayModeBar": False},
                        ),
                        className="card",
                    ),
                ],
                className="wrapper",
            ),
        ]
    )


app.layout = serve_layout


@app.callback(
    [Output("data-chart", "figure")],
    [
        Input("type-filter", "value"),
        Input("date-single", "date"),
        Input("interval-component", "n_intervals"),
    ],
)
def update_chart(data_type, date, n_intervals):
    cur = conn.cursor()
    if data_type == "co2":
        sql = f"select date_format(stamp,'%Y-%m-%d %H:%i') as stamp, ROUND(AVG(CO2), 2) as CO2 from yangsong2.yang1 WHERE DATE_FORMAT(stamp, '%Y-%m-%d')='{date}' GROUP BY 1"
        cur.execute(sql)
        dfdf = pd.DataFrame(cur.fetchall())
        if dfdf.empty:
            x = []
            y = []
        else:
            x = pd.to_datetime(dfdf.stamp)
            y = dfdf.CO2
        data_chart_figure = {
            "data": [
                {
                    "x": x,
                    "y": y,
                    "line": {"shape": "spline"},
                    "type": "lines",
                    "hovertemplate": "%{x} 이산화탄소 : %{y}" "<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "이산화탄소 데이터(ppm)",
                    "x": 0.5,
                    "xanchor": "center",
                },
                "xaxis": {"tickformat": "%H시 %M분"},
                "yaxis": {
                    "ticksuffix": "ppm",
                },
                "colorway": ["#119dff"],
            },
        }
    elif data_type == "temperature":
        sql = f"select date_format(stamp,'%Y-%m-%d %H:%i') as stamp, ROUND(AVG(temperature), 1) as temperature from yangsong2.yang1 WHERE DATE_FORMAT(stamp, '%Y-%m-%d')='{date}' GROUP BY 1"
        cur.execute(sql)
        res = cur.fetchall()
        dfdf = pd.DataFrame(res)
        if dfdf.empty:
            x = []
            y = []
        else:
            x = pd.to_datetime(dfdf.stamp)
            y = dfdf.temperature
        data_chart_figure = {
            "data": [
                {
                    "x": x,
                    "y": y,
                    "line": {"shape": "spline"},
                    "type": "lines",
                    "hovertemplate": "%{x} 온도 : %{y}" "<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "온도 데이터(℃)",
                    "x": 0.5,
                    "xanchor": "center",
                },
                "xaxis": {"tickformat": "%H시 %M분"},
                "yaxis": {"ticksuffix": "℃", "range": [-10, 50]},
                "colorway": ["#17B897"],
            },
        }
    elif data_type == "humidity":
        sql = f"select date_format(stamp,'%Y-%m-%d %H:%i') as stamp, ROUND(AVG(humidity), 1) as humidity from yangsong2.yang1 WHERE DATE_FORMAT(stamp, '%Y-%m-%d')='{date}' GROUP BY 1"
        cur.execute(sql)
        dfdf = pd.DataFrame(cur.fetchall())
        if dfdf.empty:
            x = []
            y = []
        else:
            x = pd.to_datetime(dfdf.stamp)
            y = dfdf.humidity
        data_chart_figure = {
            "data": [
                {
                    "x": x,
                    "y": y,
                    "line": {"shape": "spline"},
                    "type": "lines",
                    "hovertemplate": "%{x} 습도 : %{y}" "<extra></extra>",
                },
            ],
            "layout": {
                "title": {
                    "text": "습도 데이터(%)",
                    "x": 0.5,
                    "xanchor": "center",
                },
                "xaxis": {"tickformat": "%H시 %M분"},
                "yaxis": {"range": [0, 100], "ticksuffix": "%"},
                "colorway": ["#E12D39"],
            },
        }

    return [data_chart_figure]


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="80", debug=True)