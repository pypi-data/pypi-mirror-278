# Copyright 2019 Sergi Oliva <sergi.oliva@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields
import logging


class ImportReconcileTransientModel(models.Model):
    _name = 'import.reconcile.transient.model'

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True
    )
    mline_id = fields.Many2one(
        'account.move.line',
        string='Company',
        required=True
    )
    reconcile_code = fields.Char(string='Reconcile_code')

    check = fields.Boolean(string='Check', default=False)

    def reconcile_moves(self, company_obj):
        reconcile_moves = self.env['import.reconcile.transient.model'].search([
            ('company_id', '=', int(company_obj))
        ])
        for move in reconcile_moves:
            moves_rec = reconcile_moves.search([
                ('reconcile_code', '=', move.reconcile_code),
                ('check', '=', False)
            ])
            if moves_rec:
                m_lines = []
                m_account = moves_rec[0].mline_id.account_id
                diff_acc = False
                for move_rec in moves_rec:
                    if m_account != move_rec.mline_id.account_id:
                        diff_acc = True
                    m_lines.append(move_rec.mline_id.id)
                if diff_acc:
                    logging.info(m_lines)
                # if m_lines and len(m_lines) > 1 and not diff_acc:
                #     data = [{
                #         'type': 'account',
                #         'id': moves_rec[0].mline_id.account_id.id,
                #         'mv_line_ids': m_lines,
                #         'new_mv_line_dicts': [],
                #     }]
                #     self.env['account.reconciliation.widget'].\
                #         process_move_lines(data)
                #     moves_rec.write({
                #         'check': True,
                #     })
