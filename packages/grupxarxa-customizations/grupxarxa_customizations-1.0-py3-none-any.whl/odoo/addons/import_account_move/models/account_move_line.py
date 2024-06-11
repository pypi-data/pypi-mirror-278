# Copyright 2018 Sergi Oliva <sergi.oliva@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # Create a unique code to detect if a account_move_line has been imported
    unique_code = fields.Char(string="Old Code", index=True)
