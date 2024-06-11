# Copyright 2018 Sergi Oliva <sergi.oliva@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, exceptions, api, _
from odoo.addons.queue_job.job import job

import base64
import csv
from io import StringIO

import logging
_logger = logging.getLogger(__name__)


class ImportAccountMoveLine(models.TransientModel):
    _name = 'import.account.move.line'

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
        if ((len(values) == 2) and
                ('unique_code' in values and
                 'invoice_id' in values)):
            values['company_id'] = self.company_id.id
        elif (len(values) == 4):
            values['company_id'] = self.company_id.id
        else:
            for k, v in values.items():
                if v == 'True':
                    values[k] = True
                elif v == 'False':
                    values[k] = False
            values['journal_id'] = self.env['account.journal'].search([
                ('code', '=', 'HIST')
            ]).id
            values['company_id'] = self.company_id.id
            if values['credit']:
                values['credit'] = float(values['credit'])
            if values['debit']:
                values['debit'] = float(values['debit'])
        return values

    '''
        Function to assign not direct mapping data.

        :param values: Dict with the values to import.

        :return Dict with the correct mapping.
    '''
    def _assign_account_data(self, values, move_obj):
        account_data = {}

        if values['partner_id']:
            partner_obj = self.env['res.partner'].search([
                ('unique_code', '=', values['partner_id']),
                ('company_id', '=', values['company_id'])
            ])
            if partner_obj:
                account_data['partner_id'] = partner_obj[0].id
            else:
                partner_obj = self.env['res.partner'].search([
                    ('unique_code', '=', values['partner_id']),
                    ('company_id', '=', False),
                ])
                if partner_obj:
                    account_data['partner_id'] = partner_obj[0].id
        del values['partner_id']

        if not values['date_maturity']:
            values['date_maturity'] = move_obj.date

        if values['product_name']:
            product_obj = self.env['product.product'].search([
                ('name', '=', values['product_name']),
                ('company_id', '=', values['company_id'])
            ])
            if product_obj:
                account_data['product_id'] = product_obj[0].id
        del values['product_name']

        if values['account_name']:
            account_obj = self.env['account.account'].search([
                ('name', '=', values['account_name']),
                ('company_id', '=', values['company_id'])
            ])
            if account_obj:
                values['account_id'] = account_obj[0].id
        del values['account_name']

        return account_data

    '''
        Function to map taxes from v8 to v9+
    '''
    def _create_tax_fields(self, values):
        if values['tax_code_id']:
            tax_line = self.env['account.tax'].search([
                ('name', '=', values['name']),
                ('company_id', '=', values['company_id'])
            ])
            mline_obj = self.env['account.move.line'].search([
                ('unique_code', '=', values['unique_code'])
            ])
            if not tax_line:
                chart_ids = self.env['account.account'].search([
                    ('code', '=like', '47%'),
                    ('company_id', '=', values['company_id'])
                ]).ids
                line_objs = self.env['account.move.line'].search([
                    ('move_id', '=', mline_obj.move_id.id),
                    ('account_id', 'in', chart_ids)
                ])
                tax_ids = []
                for line in line_objs:
                    tax_id = self.env['account.tax'].search([
                        ('name', '=', line.name),
                        ('company_id', '=', values['company_id']),
                    ]).id
                    if tax_id:
                        tax_ids.append(tax_id)
                if tax_ids:
                    mline_obj.write({
                        'tax_ids': [(6, 0, tax_ids)]
                    })
            else:
                mline_obj.write({
                    'tax_line_id': tax_line.id
                })

    '''
        Function to create or write the partner / supplier.

        :param values: Dict with the values to import.
    '''

    @api.multi
    def _create_new_move_line(self, values, i):
        if ((len(values) == 3) and
                ('unique_code' in values and
                 'invoice_id' in values and
                 'company_id' in values)):
            self.with_delay()._create_new_move_line_delayed(
                    values)
        elif ((len(values) == 5) and
                ('unique_code' in values and
                 'tax_code_id' in values and
                 'product_id' in values and
                 'name' in values)):
            self._create_tax_fields(
                values)
        else:
            # Update existing move_lines
            move_obj = self.env['account.move'].search([
                ('unique_code', '=', values['move_id']),
                ('company_id', '=', values['company_id'])
            ])
            if move_obj.state == 'draft':
                self.with_delay()._create_new_move_line_delayed(
                    values, move_obj.id)

    @job
    @api.multi
    def _create_new_move_line_delayed(self, values, m_obj_id=False):
        fields = {}
        m_line_obj = self.env['account.move.line'].search([
            ('unique_code', '=', values['unique_code']),
            ('company_id', '=', values['company_id']),
        ])

        if ((len(values) == 3) and
                ('unique_code' in values and
                 'invoice_id' in values and
                 'company_id' in values)):

            invoice_obj = self.env['account.invoice'].search([
                ('unique_code', '=', values['invoice_id']),
                ('company_id', '=', values['company_id'])
            ])
            if invoice_obj:
                values.update({
                    'invoice_id': invoice_obj.id,
                })
                if m_line_obj:
                    m_line_obj.write(values)
                    _logger.info("Updating account move line")
        else:
            move_obj = self.env['account.move'].browse(m_obj_id)
            if move_obj:
                fields = self._assign_account_data(values, move_obj)
                values['move_id'] = move_obj.id
                if m_line_obj:
                    m_line_obj.write(values)
                    _logger.info("Updating account move line")
                else:
                    m_line_obj = m_line_obj.create(values)
                    _logger.info("Creating account move line")

        m_line_obj.write(fields)

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
                self._create_new_move_line(new_values, i+2)

        return {'type': 'ir.actions.act_window_close'}
