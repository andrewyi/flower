# coding: utf-8
'''
app.upload.views
------------------

'''

# import jinja2
from flask import (
    current_app,
    request,
    # make_response,
    abort,
    url_for,
    # jsonify,
    render_template_string,
)

from . import upload
from .. import csrf


@upload.route('/upload_something', methods=['GET', 'POST'])
@csrf.exempt
def upload_something():

    if request.method == 'GET':
        return render_template_string(
        '''
        <!doctype html>
        <html>
            <head>
                <title>Upload new File</title>
            </head>
            <body>
                <h1>Upload new File</h1>

                <form method="post" enctype="multipart/form-data" action="{{ url_for('upload.upload_something') }}">
                    <p><input type="text" name="plain_value">
                    <p><input type="file" name="file_field" multiple="multiple">
                    <input type="submit" value="Upload">
                </form>
            </body>
        </html>
        '''
        )

    elif request.method == 'POST':
        current_app.logger.error(request.files)
        files = request.files.getlist('file_field')
        for f in files:
            # f.save('./upload_dir/' + f.filename)
            raise Exception()
            for l in f:
                current_app.logger.debug(l)

        return 'OK'

    abort(504)


@upload.route('/post', methods=['GET', 'POST'])
@csrf.exempt
def post():

    if request.method == 'GET':
        return render_template_string(
        '''
        <!doctype html>
        <html>
            <head>
                <title>Upload new File</title>
            </head>
            <body>
                <h1>Upload new File</h1>

                <form method="post" action="{{ url_for('upload.post') }}">
                    <p><input type="text" name="fff">
                    <p><input type="text" name="fff">
                    <p><input type="text" name="fff">
                    <input type="submit" value="suBmit">
                </form>
            </body>
        </html>
        '''
        )

    elif request.method == 'POST':
        current_app.logger.error(request.form.getlist('fff'))
        return ''

    abort(504)
