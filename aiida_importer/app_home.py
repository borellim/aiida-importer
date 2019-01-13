import dash_html_components as html
from . import app

about = """
Upload your AiiDA database.
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
                    html.Li(html.A('Upload AiiDA datbase', href='upload/')),
                    html.Li(html.A('Look at plot', href='ml/')),
                ]),
                className="sycolinks"),
        ],
        id="container",
        # tag for iframe resizer
        #**{'data-iframe-height': ''},
    )
]
