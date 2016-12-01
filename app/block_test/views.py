# coding: utf-8
'''
app.block_test.views
------------------

'''

import time
import jinja2
from flask import (
    render_template_string,
)

from . import block_test
# from .. import csrf


@block_test.route('/index')
def test_render():
    return render_template_string(
'''
<html>
<head>
    <meta content="{{ csrf_token() }}" name="csrf-token">
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery.js') }}"></script>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/jquery.cxcalendar.css') }}">
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery.cxcalendar.min.js') }}"></script>
</head>
<body>
    <div id="div_lvl_1">
        <div id="div_lvl_2">
            div 2 1
        </div>
        <link rel="stylesheet" type="text/css" href="{{ url_for('block_test.sleeping_css') }}">
        {# <script type="text/javascript" src="{{ url_for('block_test.sleeping_js') }}"></script> #}
        <div id="div_lvl_2_2">
            div 2 2
        </div>
        {# <link rel="stylesheet" type="text/css" href="{{ url_for('block_test.sleeping_css2') }}"> #}
        <script type="text/javascript" src="{{ url_for('block_test.sleeping_js2') }}"></script>
        <div id="div_lvl_2_2">
            div 2 3
        </div>
        <link rel="stylesheet" type="text/css" href="{{ url_for('block_test.sleeping_css2') }}">
    </div>
    <script type="text/javascript">
    </script>
</body>
</html>
'''
            )

@block_test.route('/sleeping_css')
def sleeping_css():
    time.sleep(5)
    return '''
    body
    {
            background-color:#d0e4fe;
    }
    '''

@block_test.route('/sleeping_js')
def sleeping_js():
    time.sleep(5)
    return 'alert("sleeping_js");'

@block_test.route('/sleeping_css2')
def sleeping_css2():
    time.sleep(5)
    return '''
    div 
    {
            background-color:#d1e4fe;
    }
    '''

@block_test.route('/sleeping_js2')
def sleeping_js2():
    time.sleep(5)

@block_test.route('/t')
def t():
    return 't'




@block_test.route('/dw')
def document_write():
    return render_template_string(
'''
<html>
<head>
</head>
<body>
    some content
</body>
    <script type="text/javascript">
        window.onload = function() {
            console.log("window.onload ---");
        }
        document.write("new content");
    </script>
</html>
'''
        )
