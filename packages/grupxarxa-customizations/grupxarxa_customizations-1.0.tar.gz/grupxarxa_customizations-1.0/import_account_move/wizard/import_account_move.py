# Copyright 2018 Sergi Oliva <sergi.oliva@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, exceptions, _

import base64
import csv
from io import StringIO

import logging
_logger = logging.getLogger(__name__)


class ImportAccountMove(models.TransientModel):
    _name = 'import.account.move'

    data = fields.Binary('File', required=True)
    name = fields.Char('File name')
    delimeter = fields.Char('Delimiter', default=',',
                            help='Default delimiter ","')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True
    )

    '''
        Function to update and correct some values.

        :param values: Dict with the values to import.

        :return Dict with the modified values modifieds.
    '''
    def _update_values(self, values):
        for k, v in values.items():
            if v == 'True':
                values[k] = True
            elif v == 'False':
                values[k] = False
        values['journal_id'] = self.env['account.journal'].search([
            ('code', '=', 'HIST')
        ]).id
        values['company_id'] = self.company_id.id

        return values

    '''
        Function to assign not direct mapping data.

        :param values: Dict with the values to import.

        :return Dict with the correct mapping.
    '''
    def _assign_account_data(self, values):
        account_data = {}

        if values['partner_id']:
            partner_obj = self.env['res.partner'].search([
                ('unique_code', '=', values['unique_code']),
                ('company_id', '=', values['company_id'])
            ])
            if partner_obj:
                account_data['partner_id'] = partner_obj[0].id
        del values['partner_id']

        return account_data

    '''
        Function to create or write the partner / supplier.

        :param values: Dict with the values to import.
    '''
    def _create_new_move(self, values):
        # Update existing customers
        current_move = self.env['account.move'].search([
            ('unique_code', '=', values['unique_code']),
            ('company_id', '=', values['company_id'])
        ])
        fields = {}
        if not ((len(values) == 4) and
                ('unique_code' in values) and
                ('state' in values) and
                ('company_id' in values)):
            fields = self._assign_account_data(values)

        if current_move:
            current_move.write(values)
            _logger.info("Updating account move: %s", current_move.unique_code)
        else:
            current_move = current_move.create(values)
            _logger.info("Creating account move: %s", current_move.unique_code)

        current_move.write(fields)

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
                self._create_new_move(new_values)

        return {'type': 'ir.actions.act_window_close'}
