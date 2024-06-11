# Copyright 2018 Sergi Oliva <sergi.oliva@qubiq.es>
# Copyright 2018 Xavier Jiménez <xavier.jimenez@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, exceptions, api, _
from odoo.addons.queue_job.job import job

import base64
import csv
from io import StringIO

import logging
_logger = logging.getLogger(__name__)


class ImportInvoice(models.TransientModel):
    _name = 'import.invoice'

    data = fields.Binary('File', required=True)
    name = fields.Char('file_inputame')
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
            if v == 'True' or v == 'TRUE':
                values[k] = True
            elif v == 'False' or v == 'FALSE':
                values[k] = False
        values['company_id'] = self.company_id.id

        return values

    '''
        Function to assign not direct mapping data.

        :param values: Dict with the values to import.

        :return Dict with the correct mapping.
    '''
    def _assign_invoice_data(self, values):
        invoice_data = {}

        if values['partner_id']:
            partner_obj = self.env['res.partner'].search([
                ('unique_code', '=', values['partner_id']),
                ('company_id', '=', values['company_id'])
            ])
            if partner_obj:
                invoice_data.update({
                    'partner_id': partner_obj.id,
                })
            else:
                partner_obj = self.env['res.partner'].search([
                    ('unique_code', '=', values['partner_id']),
                    ('company_id', '=', False)
                ])
                if partner_obj:
                    invoice_data.update({
                        'partner_id': partner_obj.id,
                    })
        del values['partner_id']

        if values['partner_shipping_id']:
            partner_ship_obj = self.env['res.partner'].search([
                ('unique_code', '=', values['partner_shipping_id']),
                ('company_id', '=', values['company_id'])
            ])
            if partner_ship_obj:
                invoice_data.update({
                    'partner_shipping_id': partner_ship_obj.id,
                })
        del values['partner_shipping_id']

        if values['payment_term_id']:
            payment_term_obj = self.env['account.payment.term'].search([
                ('name', '=', values['payment_term_id']),
                ('company_id', '=', values['company_id'])
            ])
            if payment_term_obj:
                invoice_data.update({
                    'payment_term_id': payment_term_obj.id,
                })
        del values['payment_term_id']

        if values['payment_mode_id']:
            payment_mode_obj = self.env['account.payment.term'].search([
                ('name', '=', values['payment_mode_id']),
                ('company_id', '=', values['company_id'])
            ])
            if payment_mode_obj:
                invoice_data.update({
                    'payment_mode_id': payment_mode_obj.id,
                })
        del values['payment_mode_id']

        if values['fiscal_position_id']:
            fiscal_position_obj = self.env['account.fiscal.position'].search([
                ('name', '=', values['fiscal_position_id']),
                ('company_id', '=', values['company_id'])
            ])
            if fiscal_position_obj:
                invoice_data.update({
                    'fiscal_position_id': fiscal_position_obj.id,
                })
        del values['fiscal_position_id']

        if values['currency_id']:
            currency_obj = self.env['res.currency'].search([
                ('name', '=', values['currency_id'])
            ])
            if currency_obj:
                invoice_data.update({
                    'currency_id': currency_obj.id,
                })
        del values['currency_id']

        if values['partner_bank_id']:
            partner_bank_obj = self.env['res.partner.bank'].search([
                ('acc_number', '=', values['partner_bank_id']),
                ('company_id', '=', values['company_id'])
            ])
            if partner_bank_obj:
                invoice_data.update({
                    'partner_bank_id': partner_bank_obj.id,
                })
        del values['partner_bank_id']

        if values['journal_id']:
            journal_obj = self.env['account.journal'].search([
                ('code', '=', values['journal_id']),
                ('company_id', '=', values['company_id'])
            ])
            if journal_obj:
                invoice_data.update({
                    'journal_id': journal_obj.id,
                })
        del values['journal_id']

        if values['move_id']:
            move_obj = self.env['account.move'].search([
                ('unique_code', '=', values['move_id']),
                ('company_id', '=', values['company_id'])
            ])
            if move_obj:
                invoice_data.update({
                    'move_id': move_obj.id,
                })
        del values['move_id']

        if values['account_id']:
            account_obj = self.env['account.account'].search([
                ('name', '=', values['account_id']),
                ('company_id', '=', values['company_id'])
            ])
            if account_obj:
                invoice_data.update({
                    'account_id': account_obj.id,
                })
        del values['account_id']

        if values['commercial_partner_id']:
            commercial_obj = self.env['res.partner'].search([
                ('unique_code', '=', values['commercial_partner_id']),
                ('company_id', '=', values['company_id'])
            ])
            if commercial_obj:
                invoice_data.update({
                    'commercial_partner_id': commercial_obj.id,
                })
        del values['commercial_partner_id']

        if values['company_id']:
            company_obj = self.env['res.company'].search([
                ('id', '=', values['company_id'])
            ])
            if company_obj:
                invoice_data.update({
                    'company_id': company_obj.id,
                })
        del values['company_id']

        return invoice_data

    '''
        Function to create or write the partner / supplier.

        :param values: Dict with the values to import.
    '''
    @job
    @api.multi
    def _create_new_invoice(self, values):
        # Update existing customers
        current_invoice = self.env['account.invoice'].search([
            ('unique_code', '=', values['unique_code']),
            ('company_id', '=', values['company_id'])
        ])
        fields = {}
        if not ((len(values) == 3) and
                ('unique_code' in values) and
                ('state' in values) and
                ('company_id' in values)):
            fields = self._assign_invoice_data(values)

        if current_invoice:
            current_invoice.write(values)
            _logger.info("Updating invoice: %s", current_invoice.number)
        else:
            current_invoice = current_invoice.create(values)
            _logger.info("Creating invoice: %s", current_invoice.number)
        current_invoice.write(fields)

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
            if not (reader_info[i][0] is '' or reader_info[i][0][0] == '('
                    or reader_info[i][0][0] == ' '):
                field = reader_info[i]
                values = dict(zip(keys, field))
                new_values = self._update_values(values)
                self.with_delay()._create_new_invoice(new_values)

        return {'type': 'ir.actions.act_window_close'}
