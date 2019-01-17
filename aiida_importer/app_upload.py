# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

from dash.dependencies import Input, Output  #, State
import dash_core_components as dcc
import dash_html_components as html
from . import app
from .common import HIDE  # , SHOW

import tempfile
import os
import traceback
import base64

max_size_mb = 10
max_size = max_size_mb * 1000000

layout = html.Div(
    [
        html.Div("Upload your AiiDA export file (size limit: {} MB)".format(
            max_size_mb)),
        html.Div([
            "After uploading, ",
            html.B("please wait 10s"),
            " until you get the \'Sucess\' message. If the upload fails, contact a tutor."
        ]),
        dcc.Upload(
            id='upload_component',
            children=html.Div(['Drag and Drop or ',
                               html.A('Select Files')]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False,
            max_size=max_size),
        html.Div(html.B(id='upload_info')),
        html.Div(id='upload_success', style=HIDE),
        html.A('Back to overview', href='/')

        #html.Div(
        #    [
        #        html.Button('compute', id='ga_btn_compute'),
        #        html.Div('', id='ga_compute_info')
        #    ],
        #    id='div_compute'),
    ],
    id="container",
    # tag for iframe resizer
    #**{'data-iframe-height': ''},
)


# TODO: For some reason unkown to me, this callback is
# *not* fired upon file upload.
# I believe this is a bug, and should be reported to the
# plotly forum with a MWE (2 callbacks depending on file upload)
@app.callback(
    Output('upload_info', 'children'), [
        Input('upload_component', 'contents'),
        Input('upload_component', 'filename'),
        Input('upload_component', 'last_modified'),
        Input('upload_success', 'children'),
    ])
def monitor_upload(contents, filename, date, success):  # pylint: disable=unused-argument
    if not filename:
        return ""

    if not success:
        return "Uploading {}, please wait.".format(filename)
    return success


@app.callback(
    Output('upload_success', 'children'), [
        Input('upload_component', 'contents'),
        Input('upload_component', 'filename'),
        Input('upload_component', 'last_modified')
    ])
def parse_data(content, name, date):  # pylint: disable=unused-argument
    if content is None:
        return ''

    content_type, content_string = content.split(',')  # pylint: disable=unused-variable
    decoded = base64.b64decode(content_string)

    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'wb') as tmp:
            # do stuff with temp file
            tmp.write(decoded)

        try:
            from aiida import load_dbenv, is_dbenv_loaded
            if not is_dbenv_loaded():
                load_dbenv()
            from aiida.orm.importexport import import_data
            #from aiida.common import exceptions
            import_data(path)
        except Exception:
            msg = 'an exception occurred while importing the archive {}'.format(
                name)
            msg += traceback.format_exc()
        else:
            msg = 'Success: imported archive {}'.format(name)

    finally:
        os.remove(path)

    print(msg)
    return msg


#@app.callback(
#    Output('div_compute', 'style'), [Input('upload_info', 'children')])
#def show_button(json):
#    if json is None:
#        return HIDE
#    return SHOW

#@app.callback(
#    Output('ga_compute_info',
#           'children'), [Input('ga_btn_compute', 'n_clicks')],
#    [State('upload_info', 'children')])
## pylint: disable=unused-argument, unused-variable
#def on_compute(n_clicks, json):
#    if json is None:
#        return
#    df = pd.read_json(json, orient='split')
#
#    new_pop, variables = ga.main(input_data=df.values, var_names=list(df))
#    df_new = pd.DataFrame(new_pop, columns=variables)
#    df_new['Fitness'] = ""
#
#    return generate_table(df_new, download_link=True)
