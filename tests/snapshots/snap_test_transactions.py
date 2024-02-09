# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_add_transactions Test add Expense'] = {
    'data': {
        'addExpense': {
            'amount': '2000',
            'currency': 'ARS',
            'description': None,
            'id': '2024-01-01T00:03:00.000#EXPENSE',
            'name': 'Pringles'
        }
    },
    'errors': None,
    'extensions': {
    }
}

snapshots['test_add_transactions Test add Income'] = {
    'data': {
        'addIncome': {
            'amount': '4000',
            'currency': 'USD',
            'description': 'Monthly Salary',
            'id': '2024-01-01T00:02:00.000#INCOME',
            'name': 'Salary'
        }
    },
    'errors': None,
    'extensions': {
    }
}

snapshots['test_add_transactions Test transactions'] = {
    'data': {
        'transactions': [
            {
                '__typename': 'Expense',
                'amount': '4000',
                'createdAt': '2024-01-01T00:02:00.000',
                'currency': 'USD',
                'id': '2024-01-01T00:02:00.000#INCOME'
            },
            {
                '__typename': 'Expense',
                'amount': '2000',
                'createdAt': '2024-01-01T00:03:00.000',
                'currency': 'ARS',
                'id': '2024-01-01T00:03:00.000#EXPENSE'
            }
        ]
    },
    'errors': None,
    'extensions': {
    }
}
