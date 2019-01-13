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
    # note: using processes=3 for handling multiple callbacks in parallel
    # https://community.plot.ly/t/dash-callbacks-are-not-async-handling-multiple-requests-and-callbacks-in-parallel/5848
    #app.run_server(debug=True, host='0.0.0.0', processes=3)
    app.run_server(debug=True, host='0.0.0.0')
