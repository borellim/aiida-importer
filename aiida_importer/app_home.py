import dash_html_components as html
from . import app
from .common import bokeh_url

about = """
Upload your AiiDA database and compare it to existing data using automated plots.
"""
about_html = [html.P(i) for i in about.split("\n\n")]

layout = [
    html.Div(
        [
            html.Div(html.H1(app.title), id="maintitle"),
            html.H2("About"),
            html.Div(about_html, className="info-container"),
            html.H2("Steps"),
            html.Div(
                html.Ol([
                    html.Li(html.A('Upload AiiDA database', href='upload/')),
                    html.Li(
                        html.A(
                            'Plot performance of all MOFs',
                            href=bokeh_url + '/figure',
                            target="_blank")),
                ]),
                className="sycolinks"),
        ],
        id="container",
        # tag for iframe resizer
        #**{'data-iframe-height': ''},
    )
]
