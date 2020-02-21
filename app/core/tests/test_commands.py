from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_should_wait_for_db_when_db_is_available(self):
        with patch('django.db.utils.ConnectionHandler.__getitem__') as get_it:
            get_it.return_value = True
            call_command('wait_for_db')
            self.assertEqual(get_it.call_count, 1)

    # this patch is used for mock the waiting time, speeding up the tests
    @patch('time.sleep', return_value=True)
    def test_should_wait_for_database(self, ts):
        with patch('django.db.utils.ConnectionHandler.__getitem__') as get_it:
            # the get_item function raises 5 times the OperationalError
            # when called and at the sixth return True.
            get_it.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(get_it.call_count, 6)
