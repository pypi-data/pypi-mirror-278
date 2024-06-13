#!/usr/bin/env python
import json

from unittest import TestCase
from unittest.mock import ANY
from unittest.mock import Mock
from unittest.mock import patch

from event_utils.v2_event_utils import ExperimentLogger
from event_utils.v2_event_utils import V2EventLogger
from rust_decider import Decider
from rust_decider.events import ExperimentLoggerExposerAdapter
from rust_decider.events import Exposer
from utils import APP_NAME
from utils import BASE_URL
from utils import BUILD_NUMBER
from utils import CANONICAL_URL
from utils import COOKIE_CREATED_TIMESTAMP
from utils import COUNTRY_CODE
from utils import create_temp_config_file
from utils import ctx_dict
from utils import DEVICE_ID
from utils import event_json
from utils import GEN_EXP_ID
from utils import GEN_EXP_NAME
from utils import GEN_EXP_VERSION
from utils import IS_EMPLOYEE
from utils import IS_LOGGED_IN
from utils import REFERRER_URL
from utils import SUBREDDIT_ID
from utils import USER_AGENT
from utils import USER_ID


class TestDeciderExpose(TestCase):
    def setUp(self):
        def __init__(self, event_queue=None):
            return

        with patch.object(V2EventLogger, "__init__", __init__):
            self.exp_logger = ExperimentLogger()
            self.exp_logger._v2_logger = Mock(spec=V2EventLogger)

        self.valid_ctx_dict = ctx_dict

        self.genexp_0_cfg = {
            "genexp_0": {
                "id": GEN_EXP_ID,
                "name": GEN_EXP_NAME,
                "enabled": True,
                "owner": "test",
                "version": GEN_EXP_VERSION,
                "emit_event": True,
                "type": "range_variant",
                "start_ts": 0,
                "stop_ts": 2147483648,
                "experiment": {
                    "variants": [
                        {"range_start": 0.0, "range_end": 0.2, "name": "control_1"},
                        {"range_start": 0.2, "range_end": 0.4, "name": "variant_2"},
                        {"range_start": 0.4, "range_end": 0.6, "name": "variant_3"},
                        {"range_start": 0.6, "range_end": 0.8, "name": "variant_4"},
                        {"range_start": 0.8, "range_end": 1.0, "name": "variant_5"},
                    ],
                    "experiment_version": 5,
                    "shuffle_version": 91,
                    "bucket_val": "user_id",
                    "log_bucketing": False,
                },
            },
        }

        super().setUp()

    def test_choose_with_exposer(self):
        mock_expose_fn = Mock()
        exposer = Exposer(expose_fn=mock_expose_fn)

        with create_temp_config_file(self.genexp_0_cfg) as f:
            decider = Decider(f.name, exposer)

            choice = decider.choose(
                feature_name="genexp_0", context=self.valid_ctx_dict, expose=True
            )

            assert len(choice.full_events) == 1
            mock_expose_fn.assert_called_once()
            logger_arg = mock_expose_fn.call_args.args[0]

            self.assertDictEqual(
                json.loads(logger_arg),
                event_json(
                    ctx=self.valid_ctx_dict,
                    noun="user_id",
                    variant="variant_5",
                    experiment_name=GEN_EXP_NAME,
                    experiment_id=GEN_EXP_ID,
                    is_override=False,
                ),
            )

    def test_choose_with_exposer_without_expose(self):
        mock_expose_fn = Mock()
        exposer = Exposer(expose_fn=mock_expose_fn)

        with create_temp_config_file(self.genexp_0_cfg) as f:
            decider = Decider(f.name, exposer)

            choice = decider.choose(
                feature_name="genexp_0", context=self.valid_ctx_dict, expose=False
            )

            assert len(choice.full_events) == 1
            mock_expose_fn.assert_not_called()

    def test_choose_with_exposer_for_holdout(self):
        mock_expose_fn = Mock()
        exposer = Exposer(expose_fn=mock_expose_fn)

        cfg = {
            "holdout": {
                "id": 1,
                "name": "holdout",
                "version": "5",
                "type": "range_variant",
                "enabled": True,
                "emit_event": True,
                "owner": "test",
                "experiment": {
                    "variants": [
                        {"name": "holdout", "range_end": 0.0, "range_start": 0.0},
                        {"name": "control_1", "range_end": 1.0, "range_start": 0.0},
                    ],
                    "experiment_version": 5,
                    "shuffle_version": 0,
                    "bucket_val": "user_id",
                },
            },
            "child": {
                "id": 2,
                "name": "child",
                "version": "1",
                "type": "range_variant",
                "enabled": True,
                "emit_event": True,
                "owner": "asdf",
                "parent_hg_name": "holdout",
                "experiment": {
                    "variants": [
                        {"name": "control_1", "range_end": 1.0, "range_start": 0.0}
                    ],
                    "experiment_version": 0,
                    "shuffle_version": 0,
                    "bucket_val": "user_id",
                },
            },
        }

        with create_temp_config_file(cfg) as f:
            decider = Decider(f.name, exposer)

            # only expose holdout events
            choice = decider.choose(
                feature_name="child",
                context=self.valid_ctx_dict,
                expose=False,
                expose_holdout=True,
            )

            # 2 events present
            assert len(choice.full_events) == 2
            # only expose holdout event
            mock_expose_fn.assert_called_once()
            logger_arg = mock_expose_fn.call_args.args[0]

            self.assertDictEqual(
                json.loads(logger_arg),
                event_json(
                    ctx=self.valid_ctx_dict,
                    noun="user_id",
                    variant="control_1",
                    experiment_name="holdout",
                    experiment_id=1,
                    is_override=False,
                ),
            )

    def test_choose_with_exposer_adapter(self):
        logger_adapter = ExperimentLoggerExposerAdapter(self.exp_logger)

        with create_temp_config_file(self.genexp_0_cfg) as f:
            decider = Decider(f.name, logger_adapter)

            choice = decider.choose(
                feature_name="genexp_0", context=self.valid_ctx_dict, expose=True
            )

            self.assertEqual(
                dict(choice),
                {
                    "variant": "variant_5",
                    "value": None,
                    "feature_id": 6299,
                    "feature_name": "genexp_0",
                    "feature_version": 5,
                    "events": [
                        f"0::::6299::::genexp_0::::5::::variant_5::::{USER_ID}::::user_id::::0::::2147483648"
                    ],
                    "full_events": ANY,
                },
            )

            assert len(choice.full_events) == 1
            logger_kwargs = logger_adapter._logger._v2_logger.log.call_args.kwargs

            self.assertDictEqual(
                logger_kwargs,
                {
                    "device_id": DEVICE_ID,
                    "user_id": USER_ID,
                    "build_number": BUILD_NUMBER,
                    "source": "experiment",
                    "action": "expose",
                    "noun": "user_id",
                    "uuid": ANY,
                    "client_timestamp": ANY,
                    "experiment": {
                        "id": GEN_EXP_ID,
                        "name": GEN_EXP_NAME,
                        "variant": "variant_5",
                        "owner": ANY,
                        "version": str(5),
                        "bucketing_key": "user_id",
                        "bucketing_value": USER_ID,
                        "end_timestamp": ANY,
                        "start_timestamp": ANY,
                    },
                    "user": {
                        "id": USER_ID,
                        "logged_in": IS_LOGGED_IN,
                        "cookie_created_timestamp": COOKIE_CREATED_TIMESTAMP,
                        "is_employee": IS_EMPLOYEE,
                        "created_timestamp": ANY,
                    },
                    "app": {
                        "name": APP_NAME,
                        "build_number": BUILD_NUMBER,
                    },
                    "platform": {"device_id": DEVICE_ID},
                    "geo": {"country_code": COUNTRY_CODE},
                    "request": {
                        "canonical_url": CANONICAL_URL,
                        "base_url": BASE_URL,
                        "user_agent": USER_AGENT,
                    },
                    "referrer": {"url": REFERRER_URL},
                    "base_url": BASE_URL,
                    "user_agent": USER_AGENT,
                    "subreddit": {"id": SUBREDDIT_ID},
                    "app_name": APP_NAME,
                    "canonical_url": CANONICAL_URL,
                    "subreddit_id": SUBREDDIT_ID,
                    "cookie_created_timestamp": COOKIE_CREATED_TIMESTAMP,
                    "correlation_id": ANY,
                    "country_code": COUNTRY_CODE,
                    "logged_in": IS_LOGGED_IN,
                    "user_is_employee": IS_EMPLOYEE,
                    "zipkin": ANY,
                },
            )

    def test_choose_with_exposer_adapter_without_expose(self):
        logger_adapter = ExperimentLoggerExposerAdapter(self.exp_logger)

        with create_temp_config_file(self.genexp_0_cfg) as f:
            decider = Decider(f.name, logger_adapter)

            choice = decider.choose(
                feature_name="genexp_0", context=self.valid_ctx_dict, expose=False
            )

            self.assertEqual(
                dict(choice),
                {
                    "variant": "variant_5",
                    "value": None,
                    "feature_id": 6299,
                    "feature_name": "genexp_0",
                    "feature_version": 5,
                    "events": [
                        f"0::::6299::::genexp_0::::5::::variant_5::::{USER_ID}::::user_id::::0::::2147483648"
                    ],
                    "full_events": ANY,
                },
            )

            assert len(choice.full_events) == 1
            logger_adapter._logger._v2_logger.log.assert_not_called()
