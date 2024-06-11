# Copyright 2018 Sergi Oliva <sergi.oliva@qubiq.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Import Account Moves",
    "summary": "Import account moves",
    "version": "12.0.1.0.0",
    "category": "Account",
    "website": "https://www.qubiq.es",
    "author": "QubiQ",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
        "account",
        "queue_job",
    ],
    "data": [
        "wizard/import_account_move.xml",
        "wizard/import_account_move_line.xml",
        "wizard/import_concilation.xml",
        "security/ir.model.access.csv",
    ],
}
