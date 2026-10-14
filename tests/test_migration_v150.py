import sqlite3
import tempfile
import unittest
from pathlib import Path

from app import create_app, get_db, build_qr_labels_pdf
from pypdf import PdfReader


class MigrationTest(unittest.TestCase):
    def test_actual_v140_schema_upgrade_and_repeated_start_preserve_data(self):
        with tempfile.TemporaryDirectory() as folder:
            database = str(Path(folder) / 'legacy.db')
            old = sqlite3.connect(database)
            old.executescript((Path(__file__).parent / 'fixtures/v140_schema.sql').read_text())
            old.execute("INSERT INTO users(id,username,full_name,password_hash,role) VALUES (1,'admin','Admin','hash','admin')")
            old.execute("INSERT INTO components(id,code,description,quantity) VALUES (1,'TPS0001','Resistore',7)")
            old.execute("INSERT INTO movement_batches(id,operation_id,movement_type,recipient,user_id,operator_snapshot) VALUES (1,'batch-legacy','prelievo','Docente',1,'Admin')")
            old.execute("INSERT INTO movements(component_id,movement_type,quantity,delta,balance_after,user_id,batch_id,operation_id,operator_snapshot) VALUES (1,'prelievo',3,-3,7,1,1,'legacy-op','Admin')")
            old.execute('INSERT INTO reorder_lines(component_id,desired_quantity,set_by) VALUES (1,20,1)')
            old.execute("INSERT INTO app_settings VALUES ('public_base_url','https://magazzino.example')")
            before = {table: old.execute('SELECT * FROM ' + table).fetchall() for table in ('users','movements','movement_batches','reorder_lines')}
            old.commit(); old.close()
            for _ in range(2):
                app = create_app({'TESTING': True, 'DATABASE': database, 'EXCEL_SOURCE': folder + '/missing.xlsx', 'SECRET_KEY': 'test'})
                with app.app_context():
                    db = get_db()
                    self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0], 150)
                    component = db.execute('SELECT * FROM components').fetchone()
                    self.assertEqual((component['quantity'],component['active']), (7,1))
                    for table, rows in before.items():
                        self.assertEqual([tuple(row) for row in db.execute('SELECT * FROM ' + table)], rows)
                    self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
                    self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(), [])
                    with app.test_request_context():
                        pdf = PdfReader(build_qr_labels_pdf([component] * 3, 'https://magazzino.example', 200, 280))
                        self.assertEqual(len(pdf.pages), 3)
                        for page in pdf.pages:
                            self.assertIn('TPS0001',page.extract_text())

    def test_bundled_excel_import_and_restart(self):
        with tempfile.TemporaryDirectory() as folder:
            config = {'TESTING': True, 'DATABASE': folder + '/fresh.db', 'SECRET_KEY': 'test'}
            for _ in range(2):
                app = create_app(config)
                with app.app_context():
                    db = get_db()
                    self.assertEqual(db.execute('SELECT COUNT(*) FROM components').fetchone()[0], 725)
                    self.assertEqual(db.execute('SELECT COUNT(*) FROM component_codes').fetchone()[0], 725)
                    self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
