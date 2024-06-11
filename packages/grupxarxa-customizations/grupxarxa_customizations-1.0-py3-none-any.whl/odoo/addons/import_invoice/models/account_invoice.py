# Copyright 2019 Sergi Oliva <sergi.oliva@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # Create a unique code to detect if an account invoice has been imported
    unique_code = fields.Char(string="Código Interno", index=True)


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # Create a unique code to detect the same for an account invoice line
    unique_code = fields.Char(string="Código Interno", index=True)
