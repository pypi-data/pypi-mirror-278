from odoo import fields, models, exceptions, _

import base64
import csv
from io import StringIO

import logging
_logger = logging.getLogger(__name__)


class ImportReconcile(models.TransientModel):
    _name = 'import.reconcile'

    data = fields.Binary('File', required=True)
    name = fields.Char('File name')
    delimeter = fields.Char('Delimiter', default=',',
                            help='Default delimiter ","')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True
    )

    def _update_values(self, values):
        for k, v in values.items():
            if v == 'True':
                values[k] = True
            elif v == 'False':
                values[k] = False
        values['company_id'] = self.company_id.id
        mline_obj = self.env['account.move.line'].search([
            ('unique_code', '=', int(values['mline_id'])),
            ('company_id', '=', values['company_id'])
        ])
        if mline_obj and len(mline_obj) > 1:
            mline_obj[1].move_id.state = 'draft'
            mline_obj[1].unlink()
            mline_obj = mline_obj[0]
            mline_obj[0].move_id.state = 'posted'

        values['mline_id'] = mline_obj.id
        return values

    '''
        Function to create or write the partner / supplier.

        :param values: Dict with the values to import.
    '''
    def _create_new_reconcile(self, values, i):
        reconcile_obj = self.env['import.reconcile.transient.model']

        _logger.info("Creating new reconcile: %d", i)
        reconcile_obj.create(values)

    '''
        Function to read the csv file and convert it to a dict.

        :return Dict with the columns and its value.
    '''
    def action_import(self):
        """Load Inventory data from the CSV file."""
        if not self.data:
            raise exceptions.Warning(_("You need to select a file!"))
        # Decode the file data
        data = base64.b64decode(self.data).decode('utf-8')
        file_input = StringIO(data)
        file_input.seek(0)
        reader_info = []
        if self.delimeter:
            delimeter = str(self.delimeter)
        else:
            delimeter = ','
        reader = csv.reader(file_input, delimiter=delimeter,
                            lineterminator='\r\n')
        try:
            reader_info.extend(reader)
        except Exception:
            raise exceptions.Warning(_("Not a valid file!"))
        keys = reader_info[0]

        # Get column names
        keys_init = reader_info[0]
        keys = []
        for k in keys_init:
            temp = k.replace(' ', '_')
            keys.append(temp)
        del reader_info[0]
        values = {}

        for i in range(len(reader_info)):
            # Don't read rows that start with ( or are empty
            if not (reader_info[i][0] == '' or reader_info[i][0][0] == '('
                    or reader_info[i][0][0] == ' '):
                field = reader_info[i]
                values = dict(zip(keys, field))
                new_values = self._update_values(values)
                self._create_new_reconcile(new_values, i+2)

        return {'type': 'ir.actions.act_window_close'}
