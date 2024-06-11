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


class ImportInvoiceLine(models.TransientModel):
    _name = 'import.invoice.line'

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

        # if values['price_subtotal']:
        #     values['price_subtotal'] = values['price_subtotal'].replace(
        #         '.', '')
        #     values['price_subtotal'] = values['price_subtotal'].replace(
        #         ',', '.')

        # if values['price_unit']:
        #     values['price_unit'] = values['price_unit'].replace('.', '')
        #     values['price_unit'] = values['price_unit'].replace(',', '.')

        # values.update({
        #     'quantity': float(values['quantity'])
        #     if values['quantity'] else 0.00,
        #     'price_subtotal': float(values['price_subtotal'])
        #     if values['price_subtotal'] else 0.00,
        #     'price_unit': float(values['price_unit'])
        #     if values['price_unit'] else 0.00,
        # })
        return values

    '''
        Function to assign not direct mapping data.

        :param values: Dict with the values to import.

        :return Dict with the correct mapping.
    '''
    def _assign_invoice_line_data(self, values):
        invoice_line_data = {}

        # if values['partner_id']:
        #     partner_obj = self.env['res.partner'].search([
        #         ('unique_code', '=', values['partner_id']),
        #         ('company_id', '=', values['company_id'])
        #     ])
        #     if partner_obj:
        #         invoice_line_data.update({
        #             'partner_id': partner_obj.id,
        #         })
        # del values['partner_id']

        # if values['currency_id']:
        #     currency_obj = self.env['res.currency'].search([
        #         ('name', '=', values['currency_id'])
        #     ])
        #     if currency_obj:
        #         invoice_line_data.update({
        #             'currency_id': currency_obj.id,
        #         })
        # del values['currency_id']

        # if values['product_id']:
        #     product_obj = self.env['product.product'].search([
        #         ('name', '=', values['product_id']),
        #         ('company_id', '=', values['company_id'])
        #     ])
        #     if product_obj:
        #         invoice_line_data.update({
        #             'product_id': product_obj.id,
        #         })
        # del values['product_id']

        # if values['invoice_id']:
        #     self.invoice_obj = self.env['account.invoice'].search([(
        #         'unique_code', '=', values['invoice_id']),
        #         ('company_id', '=', values['company_id'])])
        #     if self.invoice_obj:
        #         invoice_line_data.update({
        #             'invoice_id': self.invoice_obj.id,
        #         })
        # del values['invoice_id']

        # if values['uom_id']:
        #     uom_obj = self.env['uom.uom'].search([
        #         ('id', '=', values['uom_id'])
        #     ])
        #     if uom_obj:
        #         invoice_line_data.update({
        #             'uom_id': uom_obj.id,
        #         })
        # del values['uom_id']

        if values['tax_code']:
            tax_obj = self.env['account.tax'].search([
                ('description', '=', values['tax_code']),
                ('company_id', '=', values['company_id'])
            ])
            if tax_obj:
                if values['tax_code2']:
                    tax_obj2 = self.env['account.tax'].search([
                        ('description', '=', values['tax_code2']),
                        ('company_id', '=', values['company_id'])
                    ])
                    invoice_line_data.update({
                        'invoice_line_tax_ids': [(6, 0, [
                            tax_obj.id, tax_obj2.id])]
                    })
                else:
                    invoice_line_data.update({
                        'invoice_line_tax_ids': [(6, 0, [tax_obj.id])]
                    })
        del values['tax_code']
        del values['tax_code2']

        return invoice_line_data

    '''
        Function to create or write the partner / supplier.

        :param values: Dict with the values to import.
    '''
    @job
    @api.multi
    def _create_new_invoice_line(self, values):
        # Update existing customers
        current_invoice_line = self.env['account.invoice.line'].search([
            ('unique_code', '=', values['unique_code']),
            ('company_id', '=', values['company_id'])
        ])
        current_invoice = current_invoice_line.invoice_id
        if current_invoice:
            company_id = values['company_id']
            fields = {}
            fields = self._assign_invoice_line_data(values)
            # if values['account_id']:
            #     account_obj = self.env['account.account'].search([
            #         ('name', '=', values['account_id']),
            #         ('company_id', '=', company_id)
            #     ])
            #     if account_obj:
            #         values.update({
            #             'account_id': account_obj.id,
            #         })
            if not current_invoice_line:
                current_invoice_line = current_invoice_line.create(values)
                _logger.info("Creating invoice \
                    line: %s", current_invoice_line.name)
            current_invoice_line.write(fields)
            if current_invoice:
                current_invoice._onchange_invoice_line_ids()

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
                self.with_delay()._create_new_invoice_line(new_values)

        return {'type': 'ir.actions.act_window_close'}
