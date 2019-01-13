# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

from dash.dependencies import Input, Output  #, State
import dash_core_components as dcc
import dash_html_components as html
from . import app

import tempfile
import os
import sys
import traceback
import base64

layout = html.Div(
    [
        dcc.Upload(
            id='ga_upload',
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
            multiple=False),
        #html.Div(id='ga_parsed_data', style=HIDE),
        html.Div(id='ga_parsed_data'),
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


@app.callback(
    Output('ga_parsed_data', 'children'), [
        Input('ga_upload', 'contents'),
        Input('ga_upload', 'filename'),
        Input('ga_upload', 'last_modified')
    ])
def parse_data(content, name, date):  # pylint: disable=unused-argument
    if content is None:
        return ''

    if sys.getsizeof(content) < 10000000:
        return 'File too large - size limit 10 MB.'

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
            msg = 'imported archive {}'.format(name)

    finally:
        os.remove(path)

    print(msg)
    return msg


#@app.callback(
#    Output('div_compute', 'style'), [Input('ga_parsed_data', 'children')])
#def show_button(json):
#    if json is None:
#        return HIDE
#    return SHOW

#@app.callback(
#    Output('ga_compute_info',
#           'children'), [Input('ga_btn_compute', 'n_clicks')],
#    [State('ga_parsed_data', 'children')])
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
