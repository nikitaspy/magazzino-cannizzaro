import sqlite3
import unittest
from io import BytesIO
from pathlib import Path

import test_app
from app import create_app, get_db, label_dimensions, set_setting, new_operation_id
from pypdf import PdfReader


class ComponentAdministrationTest(unittest.TestCase):
    setUp = test_app.WarehouseTest.setUp
    tearDown = test_app.WarehouseTest.tearDown
    create_operator = test_app.WarehouseTest.create_operator
    use_account = test_app.WarehouseTest.use_account
    def test_create_auto_code_stable_qr_and_edit(self):
        with self.app.app_context():
            set_setting('public_base_url', 'https://magazzino.example')
            get_db().commit()
        response = self.client.post('/componenti/nuovo', data={
            'description': 'Nuovo resistore', 'reorder_threshold': '2', 'target_quantity': '10'
        })
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            component = get_db().execute('SELECT * FROM components WHERE id = 2').fetchone()
            self.assertEqual(component['code'], 'TPS0002')
            self.assertEqual(component['quantity'], 0)
        self.assertEqual(self.client.get('/qr/TPS0002.svg').status_code, 200)
        self.assertEqual(self.client.get('/q/TPS0002').status_code, 200)
        self.client.post('/componenti/2/modifica', data={'description': 'Modificato', 'reorder_threshold': '1', 'target_quantity': '10'})
        with self.app.app_context():
            row = get_db().execute('SELECT * FROM components WHERE id = 2').fetchone()
            self.assertEqual(row['description'], 'Modificato')
            self.assertEqual(row['code'], 'TPS0002')

    def test_invalid_and_reserved_codes(self):
        for code in ('TPS0001', 'tps0001', 'A/B', '<script>'):
            self.client.post('/componenti/nuovo', data={'code': code, 'description': 'Test', 'reorder_threshold': '0', 'target_quantity': '0'})
        with self.app.app_context():
            self.assertEqual(get_db().execute('SELECT COUNT(*) FROM components').fetchone()[0], 1)

    def test_archive_blocks_all_movements_and_reactivation_restores(self):
        self.client.post('/componenti/1/stato', data={'action': 'archivia'})
        for path in ('/movimenti/nuovo', '/q/TPS0001'):
            response = self.client.post(path, data={'component_id': '1', 'movement_type': 'prelievo', 'quantity': '1', 'recipient': 'Test'}, follow_redirects=True)
            self.assertIn(b'archiviato', response.data)
        self.assertNotIn(b'TPS0001', self.client.get('/componenti').data)
        self.assertIn(b'TPS0001', self.client.get('/componenti?archivio=archiviati').data)
        self.assertEqual(self.client.get('/q/TPS0001').status_code, 200)
        with self.app.app_context():
            self.assertEqual(get_db().execute('SELECT quantity FROM components').fetchone()[0], 10)
            self.assertEqual(get_db().execute('SELECT COUNT(*) FROM movements').fetchone()[0], 0)
        self.client.post('/componenti/1/stato', data={'action': 'riattiva'})
        self.client.post('/movimenti/nuovo', data={'component_id': '1', 'movement_type': 'prelievo', 'quantity': '1', 'recipient': 'Test'})
        with self.app.app_context():
            self.assertEqual(get_db().execute('SELECT quantity FROM components').fetchone()[0], 9)

    def test_archived_line_rolls_back_entire_batch(self):
        with self.app.app_context():
            db = get_db()
            db.execute("INSERT INTO components(code,description,quantity,active) VALUES ('TPS0002','Archiviato',10,0)")
            db.commit()
        response = self.client.post('/movimenti/multipli', data={
            'component_id': ['1', '2'], 'quantity': ['2', '2'], 'movement_type': 'prelievo',
            'operation_id': new_operation_id()
        })
        self.assertIn(b'archiviato', response.data)
        with self.app.app_context():
            db = get_db()
            self.assertEqual([row[0] for row in db.execute('SELECT quantity FROM components')], [10, 10])
            self.assertEqual(db.execute('SELECT COUNT(*) FROM movements').fetchone()[0], 0)
            self.assertEqual(db.execute('SELECT COUNT(*) FROM movement_batches').fetchone()[0], 0)

    def test_archive_hides_reorder_but_preserves_confirmation(self):
        with self.app.app_context():
            db = get_db()
            db.execute('INSERT INTO reorder_lines(component_id, desired_quantity) VALUES (1, 5)')
            db.commit()
        self.client.post('/componenti/1/stato', data={'action': 'archivia'})
        self.assertNotIn(b'TPS0001', self.client.get('/modulo-riordino').data)
        self.assertNotIn(b'TPS0001', self.client.get('/riordino').data)
        self.assertEqual(self.client.get('/').status_code, 200)
        self.client.post('/componenti/1/stato', data={'action': 'riattiva'})
        self.assertIn(b'TPS0001', self.client.get('/modulo-riordino').data)

    def test_safe_delete_and_code_never_reused(self):
        self.client.post('/componenti/1/elimina', data={'confirm_code': 'TPS0001'})
        with self.app.app_context():
            db = get_db()
            self.assertEqual(db.execute('SELECT COUNT(*) FROM components').fetchone()[0], 1)
            db.execute('UPDATE components SET quantity = 0, active = 0 WHERE id = 1')
            db.execute('INSERT INTO reorder_lines(component_id, desired_quantity) VALUES (1, 5)')
            db.commit()
        self.client.post('/componenti/1/elimina', data={'confirm_code': 'TPS0001'})
        with self.app.app_context():
            db = get_db()
            self.assertEqual(db.execute('SELECT COUNT(*) FROM components').fetchone()[0], 1)
            db.execute('DELETE FROM reorder_lines'); db.commit()
        self.client.post('/componenti/1/elimina', data={'confirm_code': 'wrong'})
        self.client.post('/componenti/1/elimina', data={'confirm_code': 'TPS0001'})
        self.assertEqual(self.client.get('/q/TPS0001').status_code, 404)
        self.client.post('/componenti/nuovo', data={'code': 'TPS0001', 'description': 'Test', 'reorder_threshold': '0', 'target_quantity': '0'})
        with self.app.app_context():
            self.assertEqual(get_db().execute('SELECT COUNT(*) FROM components').fetchone()[0], 0)
        # Empty inventory must not reimport the bundled Excel on restart.
        reopened = create_app({**self.app.config, 'EXCEL_SOURCE': str(Path(__file__).resolve().parents[1] / 'DATABASE GLOBALE TPS ELETTRONICA.xlsx')})
        with reopened.app_context():
            self.assertEqual(get_db().execute('SELECT COUNT(*) FROM components').fetchone()[0], 0)

    def test_database_preserves_history_and_qr_identity(self):
        self.client.post('/movimenti/nuovo', data={'component_id': '1', 'movement_type': 'prelievo', 'quantity': '10', 'recipient': 'Test'})
        self.client.post('/componenti/1/stato', data={'action': 'archivia'})
        self.client.post('/componenti/1/elimina', data={'confirm_code': 'TPS0001'})
        with self.app.app_context():
            db = get_db()
            self.assertEqual(db.execute('SELECT COUNT(*) FROM components').fetchone()[0], 1)
            for sql in ('DELETE FROM components WHERE id = 1', "UPDATE components SET code = 'NEW' WHERE id = 1", 'DELETE FROM movements'):
                with self.assertRaises(sqlite3.IntegrityError):
                    db.execute(sql)
                db.rollback()

    def test_operator_forbidden_and_csrf_required(self):
        self.app.config['CSRF_ENABLED'] = True
        self.assertEqual(self.client.post('/componenti/1/stato', data={'action': 'archivia'}).status_code, 400)
        self.app.config['CSRF_ENABLED'] = False
        self.use_account(self.create_operator())
        for path in ('/componenti/nuovo', '/componenti/1/stato', '/componenti/1/elimina'):
            self.assertEqual(self.client.post(path).status_code, 403)
        self.assertEqual(self.client.get('/componenti?archivio=tutti').status_code, 403)

    def test_label_presets_custom_multipage_and_validation(self):
        with self.app.app_context():
            set_setting('public_base_url', 'https://magazzino.example'); get_db().commit()
        for form in ({'format': '25x25'}, {'format': '35x25'}, {'format': '50x30'}, {'format': 'custom', 'width_mm': '200', 'height_mm': '280'}):
            response = self.client.post('/etichette-qr.pdf', data={**form, 'selected_ids': '1'})
            self.assertEqual(response.status_code, 200)
            pdf = PdfReader(BytesIO(response.data))
            self.assertIn('TPS0001', pdf.pages[0].extract_text())
            self.assertAlmostEqual(float(pdf.pages[0].mediabox.width), 595.2756, places=3)
            from pypdf.generic import ContentStream
            rectangle = next(args for args, op in ContentStream(pdf.pages[0].get_contents(), pdf).operations if op == b're')
            dimensions = label_dimensions(form)
            self.assertAlmostEqual(float(rectangle[2]), dimensions[0] * 72/25.4, places=3)
            self.assertAlmostEqual(float(rectangle[3]), dimensions[1] * 72/25.4, places=3)
        for width in ('nan', 'inf', '-5', '201', 'hello'):
            with self.assertRaises(ValueError):
                label_dimensions({'format': 'custom', 'width_mm': width, 'height_mm': '25'})
        response = self.client.post('/etichette-qr.pdf', data={'selected_ids': '1', 'format': 'bad'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get('/componenti/1/etichetta.pdf?format=bad').status_code, 400)

    def test_public_credits_and_legal_documents(self):
        anonymous = self.app.test_client()
        self.assertIn(b'Nikita Spiridigliozzi', anonymous.get('/informazioni').data)
        for name in ('LICENSE', 'NOTICE.md', 'ADDITIONAL_TERMS.md'):
            self.assertEqual(anonymous.get('/documenti/' + name).status_code, 200)
        self.assertEqual(anonymous.get('/documenti/app.py').status_code, 404)
