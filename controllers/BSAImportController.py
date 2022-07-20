# -*- coding: utf-8 -*-


import json

from odoo import http
from odoo.http import request
from odoo.tools import misc




class CustomImportController(http.Controller):

    @http.route('/base_import/set_file', methods=['POST'])
    def custom_set_file(self, file, import_id, jsonp='callback'):

        print("Calling set_file")
        import_id = int(import_id)

        written = request.env['base_import.import'].browse(import_id).write({
            'file': file.read(),
            'file_name': file.filename,
            'file_type': file.content_type,
        })



        return 'window.top.%s(%s)' % (misc.html_escape(jsonp), json.dumps({'result': written}))