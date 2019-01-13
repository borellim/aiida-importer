# -*- coding: utf-8 -*-
from aiida_importer import app, app_home, app_upload
import dash.dependencies as dep


@app.callback(
    dep.Output('page-content', 'children'), [dep.Input('url', 'pathname')])
def display_page(pathname):
    if pathname is None:
        return app_home.layout

    if pathname.endswith('/upload/'):
        return app_upload.layout
    #elif pathname.endswith('/ga/'):
    #    return app_ga.layout
    #elif pathname.endswith('/ml/'):
    #    return app_ml.layout
    return app_home.layout


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
