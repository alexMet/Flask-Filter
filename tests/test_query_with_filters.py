import unittest
from datetime import date

from flask_filter.query_filter import query_with_filters

from tests.minipet_app import create_app, Dog, DogSchema, db


class QueryWithFiltersTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.db = db
        with self.app.app_context():
            self.db.create_all()
            self.make_dogs()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()
        self.app = None
        self.db = None

    def make_dogs(self):
        doggos = [
            Dog(name="Xocomil", dob=date(1990, 12, 16), weight=100),
            Dog(name="Jasmine", dob=date(1997, 4, 20), weight=40),
            Dog(name="Quick", dob=date(2000, 5, 24), weight=90),
            Dog(name="Jinx", dob=date(2005, 12, 31), weight=55),
            Dog(name="Kaya", dob=None, weight=50)
        ]
        self.db.session.add_all(doggos)
        self.db.session.commit()

    def test_name_equalsfilter(self):
        xfilters = [{"field": "name", "op": "=", "value": "Xocomil"}]
        with self.app.app_context():
            xoco = query_with_filters(Dog, xfilters, DogSchema)
        self.assertEqual(len(xoco), 1)
        self.assertEqual(xoco[0].name, "Xocomil")

    def test_name_likefilter(self):
        filters = [{"field": "name", "op": "like", "value": "J%"}]
        with self.app.app_context():
            j_dogs = query_with_filters(Dog, filters, DogSchema)
        self.assertEqual(len(j_dogs), 2)
        self.assertEqual(j_dogs[0].name, "Jasmine")
        self.assertEqual(j_dogs[1].name, "Jinx")

    def test_name_notequalsfilter(self):
        xfilters = [{"field": "name", "op": "!=", "value": "Xocomil"}]
        with self.app.app_context():
            not_xoco = query_with_filters(Dog, xfilters, DogSchema)
        self.assertEqual(len(not_xoco), 4)

    def test_name_infilter(self):
        f = [{"field": "name", "op": "in", "value": ["Jinx", "Kaya"]}]
        with self.app.app_context():
            jinx_and_kaya = query_with_filters(Dog, f, DogSchema)
        self.assertEqual(len(jinx_and_kaya), 2)

    def test_dob_filter(self):
        min_date = date(2002, 1, 1).isoformat()
        f = [{"field": "dateOfBirth", "op": "<", "value": min_date}]
        with self.app.app_context():
            old_dogs = query_with_filters(Dog, f, DogSchema)
        self.assertEqual(len(old_dogs), 3)

    def test_dob_null_equalsfilter(self):
        f = [{"field": "dateOfBirth", "op": "=", "value": None}]
        with self.app.app_context():
            kaya = query_with_filters(Dog, f, DogSchema)
            self.assertEqual(len(kaya), 1)
            self.assertEqual(kaya[0].name, "Kaya")

    def test_dob_null_notequalsfilter(self):
        f = [{"field": "dateOfBirth", "op": "!=", "value": None}]
        with self.app.app_context():
            not_kaya = query_with_filters(Dog, f, DogSchema)
            self.assertEqual(len(not_kaya), 4)

    def test_weight_ltfilter(self):
        f = [{"field": "weight", "op": "<", "value": 50}]
        with self.app.app_context():
            skinny_dogs = query_with_filters(Dog, f, DogSchema)
        self.assertEqual(len(skinny_dogs), 1)

    def test_weight_ltefilter(self):
        f = [{"field": "weight", "op": "<=", "value": 50}]
        with self.app.app_context():
            skinnyish_dogs = query_with_filters(Dog, f, DogSchema)
        self.assertEqual(len(skinnyish_dogs), 2)

    def test_weight_gtfilter(self):
        f = [{"field": "weight", "op": ">", "value": 90}]
        with self.app.app_context():
            fat_dogs = query_with_filters(Dog, f, DogSchema)
        self.assertEqual(len(fat_dogs), 1)

    def test_weight_gtefilter(self):
        f = [{"field": "weight", "op": ">=", "value": 90}]
        with self.app.app_context():
            fatish_dogs = query_with_filters(Dog, f, DogSchema)
        self.assertEqual(len(fatish_dogs), 2)

    def test_registered_schema_against_dob(self):
        min_date = date(2002, 1, 1).isoformat()
        f = [{"field": "dateOfBirth", "op": "<", "value": min_date}]
        with self.app.app_context():
            old_dogs = query_with_filters(Dog, f, DogSchema)
        self.assertEqual(len(old_dogs), 3)
