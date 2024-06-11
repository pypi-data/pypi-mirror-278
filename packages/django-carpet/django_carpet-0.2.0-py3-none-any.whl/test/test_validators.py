# Python
from datetime import datetime, timedelta

# Django
from django.test import TestCase

from django_carpet.validators import date_time_validation, string_validation, choice_validation, boolean_validation, integer_validation
from django_carpet.exceptions import InputError


class ValidaotrsTest(TestCase):

    def test_date_time_validators(self):
        now = datetime.now()
        valid_iso = now.isoformat()
        min_iso = (datetime.now() + timedelta(days=10)).isoformat()

        # Testing the date time validation when the value is None
        try:
            date_time_validation(None, "dateTime")
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'dateTime')
        except Exception as e:
            self.fail(e)


        # Testing the date time validation when the value is not an ISO format date time
        try:
            date_time_validation('abc', "dateTime")
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'dateTime')
        except Exception as e:
            self.fail(e)

        # Testing the date time validation when the value is a valid but before min date
        try:
            date_time_validation(valid_iso, "dateTime", False, min_iso)
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'dateTime')
        except Exception as e:
            self.fail(e)

        # Testing the date time validation when the value is None and empty is allowed
        self.assertIsNone(date_time_validation(None, 'dateTime', True))

        # Testing the date time validation when the value is an empty string and empty is allowed
        self.assertIsNone(date_time_validation("", 'dateTime', True))
        
        # Testing the date time validation when the value is valid without min date
        self.assertEqual(
            date_time_validation(valid_iso, 'dateTime'),
            now
        )

        # Testing the date time validation when the value is valid with a min date
        self.assertEqual(
            date_time_validation(valid_iso, 'dateTime', False, (datetime.now() - timedelta(days=10))),
            now
        )
        

    def test_string_validators(self):

        # Testing the string validation when the value is None
        try:
            string_validation(None, 10, 'string')
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'string')
        except Exception as e:
            self.fail(e)


        # Testing the string validation when the value is empty string
        try:
            string_validation("", 10, 'string')
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'string')
        except Exception as e:
            self.fail(e)


        # Testing the string validation when the text is too long
        try:
            string_validation('1234567891011', 10, "string")
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'string')
        except Exception as e:
            self.fail(e)

        self.assertEqual(type(string_validation("abc", 10, 'string')), str)
        self.assertEqual(type(string_validation("abc", 10, 'string', empty=True)), str)
        self.assertIsNone(string_validation(None, 10, 'string', empty=True))
        self.assertIsNone(string_validation("", 10, 'string', empty=True))
    

    def test_choice_validators(self):

        # Testing the choice validation when the value is None
        try:
            choice_validation(None, ["one", "two"], "choice")
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'choice')
        except Exception as e:
            self.fail(e)


        # Testing the choice validation when the value is empty string
        try:
            choice_validation("", ["one", "two"], 'choice')
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'choice')
        except Exception as e:
            self.fail(e)


        # Testing the choice validation when the value is not among the options
        try:
            choice_validation('three', ["one", "two"], "choice")
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'choice')
        except Exception as e:
            self.fail(e)

        self.assertEqual(type(choice_validation("one", ["one", "two"], 'choice')), str)
        self.assertEqual(type(choice_validation("one", ["one", "two"], 'choice', True)), str)
        self.assertIsNone(choice_validation(None, ["one", "two"], 'choice', null=True))
        self.assertIsNone(choice_validation("", ["one", "two"], 'choice', null=True))


    def test_boolean_validators(self):

        # Testing the boolean validation if the value is None
        try:
            boolean_validation(None, 'bool')
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'bool')
        except Exception as e:
            self.fail(e)

        # Testing the boolean validation if the value is an invalid string
        try:
            boolean_validation('other', 'bool')
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'bool')
        except Exception as e:
            self.fail(e)
            
        self.assertTrue(boolean_validation(True, 'bool'))
        self.assertTrue(boolean_validation('true', 'bool'))
        self.assertFalse(boolean_validation(False, 'bool'))
        self.assertFalse(boolean_validation('false', 'bool'))

    def test_integer_validators(self):

        # Testing the integer validation when the value is None and empty is false
        try:
            integer_validation(None, 0, 100, 'number', empty=False)
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'number')
        except Exception as e:
            self.fail(e)

        try:
            integer_validation('', 0, 100, 'number', empty=False)
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'number')
        except Exception as e:
            self.fail(e)
            
        # Testing the integer validation when the value is None and empty is True
        self.assertIsNone(integer_validation(None, 0, 100, 'number', empty=True))
        self.assertIsNone(integer_validation("", 0, 100, 'number', empty=True))
        
        # Passing an invalid text as number
        try:
            integer_validation('ss', 0, 100, 'number', empty=False)
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'number')
        except Exception as e:
            self.fail(e)

        # Passing a number smaller than the minimum
        try:
            integer_validation('0', 1, 100, 'number', empty=False)
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'number')
        except Exception as e:
            self.fail(e)

        try:
            integer_validation(0, 1, 100, 'number', empty=False)
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'number')
        except Exception as e:
            self.fail(e)

        # Passing a number bigger than the minimum
        try:
            integer_validation('200', 0, 100, 'number', empty=False)
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'number')
        except Exception as e:
            self.fail(e)

        try:
            integer_validation(200, 0, 100, 'number', empty=False)
            self.fail("exception was not raised")
        except InputError as e:
            self.assertEqual(e.obj, 'number')
        except Exception as e:
            self.fail(e)

        # Passing valid values 
        self.assertEqual(integer_validation(200, 0, 300, 'number', empty=False), 200)
        self.assertEqual(integer_validation('200', 0, 300, 'number', empty=False), 200)