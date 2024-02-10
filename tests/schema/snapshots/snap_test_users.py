# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_add_user Test addUser'] = {
    'data': {
        'addUser': {
            'createdAt': '2024-01-01T00:02:00.000',
            'email': 'tester@email.com',
            'id': 'deterministic-id-2',
            'modifiedAt': '2024-01-01T00:02:00.000',
            'name': 'Tester User',
            'username': 'tester'
        }
    },
    'errors': None,
    'extensions': {
    }
}

snapshots['test_add_user Test another addUser'] = {
    'data': {
        'addUser': {
            'createdAt': '2024-01-01T00:03:00.000',
            'email': 'tester_another@email.com',
            'id': 'deterministic-id-3',
            'modifiedAt': '2024-01-01T00:03:00.000',
            'name': 'Tester Userr',
            'username': 'testerr'
        }
    },
    'errors': None,
    'extensions': {
    }
}

snapshots['test_add_user Test user query'] = {
    'data': {
        'user': {
            'createdAt': '2024-01-01T00:02:00.000',
            'email': 'tester@email.com',
            'id': 'deterministic-id-2',
            'name': 'Tester User',
            'username': 'tester'
        }
    },
    'errors': None,
    'extensions': {
    }
}
