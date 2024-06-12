import json
import logging
from http import HTTPStatus
from uuid import UUID

import pytest
import responses

from fiddler.constants.alert_rule import AlertCondition, BinSize, CompareTo, Priority
from fiddler.entities.alert_rule import AlertRule
from fiddler.exceptions import NotFound
from fiddler.schemas.alert_rule import NotificationConfig
from fiddler.tests.apis.test_baseline import (
    API_RESPONSE_200 as BASELINE_API_RESPONSE_200,
)
from fiddler.tests.apis.test_model import API_RESPONSE_200 as MODEL_API_RESPONSE_200
from fiddler.tests.constants import (
    ALERT_RULE_ID,
    BASELINE_ID,
    BASELINE_NAME,
    MODEL_ID,
    MODEL_NAME,
    PROJECT_ID,
    PROJECT_NAME,
    URL,
)
from fiddler.utils.logger import set_logging

API_RESPONSE_200 = {
    'data': {
        'id': ALERT_RULE_ID,
        'model': {'id': MODEL_ID, 'name': MODEL_NAME, 'version': 'v1'},
        'project': {'id': PROJECT_ID, 'name': PROJECT_NAME},
        'organization': {
            'id': 'e03d6f02-6efa-4eb1-b828-7ea9d2a083d0',
            'name': 'scale154',
        },
        'baseline': None,
        'segment': None,
        'version': 'rule_v3',
        'name': 'skdfvbj',
        'priority': 'HIGH',
        'feature_names': ['gender'],
        'bin_size': 'Hour',
        'compare_to': 'raw_value',
        'condition': 'greater',
        'warning_threshold': 1.0,
        'evaluation_delay': 10,
        'critical_threshold': 2.0,
        'updated_at': '2024-04-17T12:42:15.672909+00:00',
        'enable_notification': True,
        'compare_bin_delta': 0,
        'created_at': '2024-04-17T12:42:15.672909+00:00',
        'created_by': {
            'id': '287949c2-13f8-49fc-a559-55b2e6f36e9b',
            'full_name': 'Fiddler Administrator',
            'email': 'admin@fiddler.ai',
        },
        'updated_by': {
            'id': '287949c2-13f8-49fc-a559-55b2e6f36e9b',
            'full_name': 'Fiddler Administrator',
            'email': 'admin@fiddler.ai',
        },
        'metric': {
            'id': 'null_violation_percentage',
            'display_name': '% Missing Value Violation',
            'type': 'data_integrity',
            'type_display_name': 'Data Integrity',
        },
    },
    'api_version': '3.0',
    'kind': 'NORMAL',
}

API_RESPONSE_200_V2 = {
    'data': {
        'id': 794,
        'organization_name': 'mainbuild',
        'project_name': PROJECT_NAME,
        'model_id': 285,
        'name': 'test_rule',
        'metric': 'jsd',
        'metric_id': 'jsd',
        'metric_display_name': 'Jensen-Shannon Distance',
        'alert_type': 'drift',
        'alert_type_display_name': 'Data Drift',
        'priority': 'MEDIUM',
        'baseline_name': BASELINE_NAME,
        'feature_names': ['creditscore'],
        'time_bucket': 3600000,
        'category': None,
        'bin_size': 'Hour',
        'compare_to': 'raw_value',
        'condition': 'greater',
        'compare_period': None,
        'warning_threshold': 1.0,
        'critical_threshold': 2.3,
        'is_active': True,
        'created_by': 'admin@fiddler.ai',
        'created_at': '2024-04-23T10:34:14.321895+00:00',
        'last_updated': '2024-04-23T10:34:14.323554+00:00',
        'model_name': 'bank_churn',
        'enable_notification': True,
        'segment': {
            'id': '1c9b551a-808b-4ef0-b67b-e788eaf1e6de',
            'organization_name': 'mainbuild',
            'project_name': 'nick_test_project_11',
            'model_name': 'bank_churn',
            'name': 'xyzab',
            'definition': 'Age > 10',
            'description': 'meh',
            'created_at': '2024-04-23T10:31:52.181550+00:00',
            'created_by': {
                'id': 1,
                'full_name': 'Fiddler Administrator',
                'email': 'admin@fiddler.ai',
            },
        },
        'project': {'id': PROJECT_ID, 'name': PROJECT_NAME},
        'model': {'id': MODEL_ID, 'name': MODEL_NAME, 'version': 'v1'},
        'baseline': {'id': BASELINE_ID, 'name': BASELINE_NAME},
        'compare_bin_delta': None,
        'uuid': ALERT_RULE_ID,
        'notifications': {
            'pagerduty': {
                'alert_config_uuid': ALERT_RULE_ID,
                'service': '',
                'severity': '',
            },
            'emails': {'email': ''},
            'webhooks': [],
        },
    },
    'api_version': '2.0',
    'kind': 'NORMAL',
}


API_RESPONSE_404 = {
    'error': {
        'code': 404,
        'message': "AlertConfig({'uuid': 'ff9a897b-be5b-48e6-909f-13073a6d0fe8'}) not found",
        'errors': [
            {
                'reason': 'ObjectNotFound',
                'message': "AlertConfig({'uuid': 'ff9a897b-be5b-48e6-909f-13073a6d0fe8'}) not found",
                'help': '',
            }
        ],
    },
    'api_version': '2.0',
    'kind': 'ERROR',
}

LIST_API_RESPONSE = {
    'data': {
        'page_size': 100,
        'total': 2,
        'item_count': 2,
        'page_count': 1,
        'page_index': 1,
        'offset': 0,
        'items': [
            API_RESPONSE_200['data'],
            {
                'id': '3431b746-d18f-4aed-99ea-2da8d5b46fb6',
                'model': {'id': MODEL_ID, 'name': MODEL_NAME, 'version': 'v1'},
                'project': {'id': PROJECT_ID, 'name': PROJECT_NAME},
                'organization': {
                    'id': 'e03d6f02-6efa-4eb1-b828-7ea9d2a083d0',
                    'name': 'scale154',
                },
                'baseline': {'id': BASELINE_ID, 'name': BASELINE_NAME},
                'segment': None,
                'version': 'rule_v3',
                'name': 'sfdvsefv',
                'priority': 'HIGH',
                'feature_names': ['numofproducts'],
                'bin_size': 'Hour',
                'compare_to': 'raw_value',
                'condition': 'greater',
                'warning_threshold': 1e-05,
                'critical_threshold': 0.001,
                'updated_at': '2024-04-17T12:43:23.871997+00:00',
                'enable_notification': True,
                'compare_bin_delta': 0,
                'evaluation_delay': 0,
                'created_at': '2024-04-17T12:43:23.871997+00:00',
                'created_by': {
                    'id': '287949c2-13f8-49fc-a559-55b2e6f36e9b',
                    'full_name': 'Fiddler Administrator',
                    'email': 'admin@fiddler.ai',
                },
                'updated_by': {
                    'id': '287949c2-13f8-49fc-a559-55b2e6f36e9b',
                    'full_name': 'Fiddler Administrator',
                    'email': 'admin@fiddler.ai',
                },
                'metric': {
                    'id': 'jsd',
                    'display_name': 'Jensen-Shannon Distance',
                    'type': 'drift',
                    'type_display_name': 'Data Drift',
                },
            },
        ],
    }
}

LIST_API_RESPONSE_EMPTY = {
    'data': {
        'page_size': 100,
        'total': 2,
        'item_count': 2,
        'page_count': 1,
        'page_index': 1,
        'offset': 0,
        'items': [],
    }
}


@responses.activate
def test_get_alert_rule_success() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)

    assert isinstance(alert_rule, AlertRule)


@responses.activate
def test_get_alert_rule_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        AlertRule.get(id_=ALERT_RULE_ID)


@responses.activate
def test_alert_rule_list_success() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules',
        json=LIST_API_RESPONSE,
    )
    for rule in AlertRule.list(model_id=MODEL_ID):
        assert isinstance(rule, AlertRule)


@responses.activate
def test_alert_rule_list_empty() -> None:

    responses.get(
        url=f'{URL}/v3/alert-rules',
        json=LIST_API_RESPONSE_EMPTY,
    )

    assert len(list(AlertRule.list(model_id=MODEL_ID))) == 0


@responses.activate
def test_delete_alert_rule() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )
    rule = AlertRule.get(id_=ALERT_RULE_ID)

    responses.delete(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
    )

    rule.delete()


@responses.activate
def test_delete_alert_rule_not_found() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )
    rule = AlertRule.get(id_=ALERT_RULE_ID)

    responses.delete(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_404,
        status=HTTPStatus.NOT_FOUND,
    )

    with pytest.raises(NotFound):
        rule.delete()


@responses.activate
def test_add_alert_rule_success() -> None:
    responses.get(
        url=f'{URL}/v3/models/{MODEL_ID}',
        json=MODEL_API_RESPONSE_200,
    )
    responses.get(
        url=f'{URL}/v3/baselines/{BASELINE_ID}',
        json=BASELINE_API_RESPONSE_200,
    )
    responses.post(
        url=f'{URL}/v3/alert-rules',
        json=API_RESPONSE_200,
    )
    alert_rule = AlertRule(
        name='alert_name',
        model_id=MODEL_ID,
        metric_id='drift',
        priority=Priority.HIGH,
        compare_to=CompareTo.RAW_VALUE,
        condition=AlertCondition.GREATER,
        bin_size=BinSize.HOUR,
        critical_threshold=0.5,
        warning_threshold=0.1,
        columns=['gender', 'creditscore'],
        evaluation_delay=10,
    ).create()

    assert isinstance(alert_rule, AlertRule)
    assert alert_rule.id == UUID(ALERT_RULE_ID)
    assert alert_rule.model.id == UUID(MODEL_ID)
    assert alert_rule.project_id == UUID(PROJECT_ID)
    assert alert_rule.evaluation_delay == 10


@responses.activate
def test_enable_notifications(caplog) -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)

    resp = responses.patch(
        url=f'{URL}/v2/alert-configs/{ALERT_RULE_ID}',
        json=API_RESPONSE_200_V2,
    )
    set_logging(logging.INFO)

    alert_rule.enable_notifications()
    assert json.loads(resp.calls[0].request.body) == {'enable_notification': True}
    assert (
        f'Notifications have been enabled for alert rule with id: {ALERT_RULE_ID}'
        == caplog.messages[0]
    )


@responses.activate
def test_disable_notifications(caplog) -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)

    API_RESPONSE_200['enable_notification'] = False

    resp = responses.patch(
        url=f'{URL}/v2/alert-configs/{ALERT_RULE_ID}',
        json=API_RESPONSE_200_V2,
    )

    set_logging(logging.INFO)
    alert_rule.disable_notifications()
    assert json.loads(resp.calls[0].request.body) == {'enable_notification': False}
    assert (
        f'Notifications have been disabled for alert rule with id: {ALERT_RULE_ID}'
        == caplog.messages[0]
    )


@responses.activate
def test_set_notifications() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)
    API_RESPONSE_200_V2['data']['notifications'] = {
        'webhooks': [
            {'uuid': 'e20bf4cc-d2cf-4540-baef-d96913b14f1b'},
            {'uuid': '6e796fda-0111-4a72-82cd-f0f219e903e1'},
        ],
        'emails': {
            'alert_config_uuid': ALERT_RULE_ID,
            'email': 'nikhil@fiddler.ai, admin@fiddler.ai',
        },
        'pagerduty': {
            'service': '',
            'alert_config_uuid': ALERT_RULE_ID,
            'severity': '',
        },
    }
    responses.patch(
        url=f'{URL}/v2/alert-configs/{ALERT_RULE_ID}',
        json=API_RESPONSE_200_V2,
    )
    notifications = alert_rule.set_notification_config(
        emails=['nikhil@fiddler.ai', 'admin@fiddler.ai'],
        webhooks=[
            'e20bf4cc-d2cf-4540-baef-d96913b14f1b',
            '6e796fda-0111-4a72-82cd-f0f219e903e1',
        ],
    )
    assert notifications == NotificationConfig(
        **{
            'emails': ['nikhil@fiddler.ai', 'admin@fiddler.ai'],
            'webhooks': [
                'e20bf4cc-d2cf-4540-baef-d96913b14f1b',
                '6e796fda-0111-4a72-82cd-f0f219e903e1',
            ],
        }
    )


@responses.activate
def test_get_notifications() -> None:
    responses.get(
        url=f'{URL}/v3/alert-rules/{ALERT_RULE_ID}',
        json=API_RESPONSE_200,
    )

    alert_rule = AlertRule.get(id_=ALERT_RULE_ID)
    responses.get(
        url=f'{URL}/v2/alert-configs/{ALERT_RULE_ID}',
        json=API_RESPONSE_200_V2,
    )
    notifications = alert_rule.get_notification_config()
    assert notifications == NotificationConfig(
        **{
            'emails': ['nikhil@fiddler.ai', 'admin@fiddler.ai'],
            'webhooks': [
                'e20bf4cc-d2cf-4540-baef-d96913b14f1b',
                '6e796fda-0111-4a72-82cd-f0f219e903e1',
            ],
        }
    )
