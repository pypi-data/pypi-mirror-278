import json
import random
import tempfile

from contextlib import contextmanager
from typing import Optional
from unittest.mock import ANY

USER_ID = "795244"
AD_ACCOUNT_ID = "t2_4321"
APP_NAME = "ios"
APP_VERSION = "0.0.0.0"
AUTH_CLIENT_ID = "token"
BUILD_NUMBER = 1234
BUSINESS_ID = "t_some"
CANONICAL_URL = "www.reddit.com"
BASE_URL = "https://www.reddit.com?test=true"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
REFERRER_URL = "https://www.google.com"
COOKIE_CREATED_TIMESTAMP = 1648859753
COUNTRY_CODE = "UA"
DEVICE_ID = "d42b90e7-aae3-4ac5-b137-042de165ecf6"
IS_EMPLOYEE = True
IS_LOGGED_IN = True
EVENT_FIELDS = {
    "user_id": USER_ID,
    "logged_in": IS_LOGGED_IN,
    "cookie_created_timestamp": COOKIE_CREATED_TIMESTAMP,
}
LOID_CREATED_TIMESTAMP = 123456
LOCALE_CODE = "us_en"
ORIGIN_SERVICE = "origin"
SUBREDDIT_ID = "t5_asdf"

EXPERIMENT_OWNER = "test"
GEN_EXP_ID = 6299
GEN_EXP_NAME = "genexp_0"
GEN_EXP_VERSION = "5"

ctx_dict = {
    "user_id": USER_ID,
    "device_id": DEVICE_ID,
    "canonical_url": CANONICAL_URL,
    "base_url": BASE_URL,
    "user_agent": USER_AGENT,
    "referrer_url": REFERRER_URL,
    "subreddit_id": SUBREDDIT_ID,
    "ad_account_id": AD_ACCOUNT_ID,
    "business_id": BUSINESS_ID,
    "locale": LOCALE_CODE,
    "user_is_employee": IS_EMPLOYEE,
    "logged_in": IS_LOGGED_IN,
    "app_name": APP_NAME,
    "build_number": BUILD_NUMBER,
    "country_code": COUNTRY_CODE,
    "origin_service": "oss",
    "oauth_client_id": "test",
    "cookie_created_timestamp": COOKIE_CREATED_TIMESTAMP,
}

# TODO: make these real country codes.  Not necessary, but nicer.
# eventually get from reddit-service-admin/admin/lib/geolocations.py
LOCALES = ["us", "gb", "es"]
APP_NAMES = [
    "app_1",
    "app_2",
    "app_3",
    "app_4",
    "app_5",
]  # TODO: figure out if this is enough.


@contextmanager
def create_temp_config_file(contents):
    with tempfile.NamedTemporaryFile() as f:
        f.write(json.dumps(contents).encode())
        f.seek(0)
        yield f


def make_request_context_map(h={}):
    return {
        "user_id": str(h.get("user_id", random.choice(range(1000)))),
        "locale": h.get("locale", random.choice(LOCALES + [None])),
        "device_id": str(h.get("device_id", 10000 + random.choice(range(1000)))),
        "country_code": h.get("locale", random.choice(LOCALES + [None])),
        "origin_service": h.get("origin_service"),  # do I care about this one?
        "user_is_employee": h.get(
            "user_is_employee", random.choice([True, False, None])
        ),
        "logged_in": h.get("logged_in", random.choice([True, False, None])),
        "app_name": h.get("app_name", random.choice(APP_NAMES + [None])),
        "build_number": int(h.get("build_number", 1000 + random.choice(range(1000)))),
    }


def make_experiment(n, h={}):
    version = int(h.get("version", random.choice(range(10000))))
    variants = h.get(
        "variants", h.get("experiment", {}).get("variants", make_variants())
    )
    shuffle_version = h.get(
        "shuffle_version",
        h.get("experiment", {}).get("shuffle_version", random.choice(range(100))),
    )
    return {
        "id": int(h.get("id", random.choice(range(10000)))),
        "name": str(h.get("name", "genexp_" + str(n))),
        "enabled": True,  # TODO: make this false sometimes?  lowpri
        "owner": "test",
        "version": str(version),
        "type": "range_variant",
        "start_ts": 0,  # we're not interested in testing start/stop
        "stop_ts": 2147483648,
        "experiment": {
            "variants": variants,
            "experiment_version": int(version),
            "shuffle_version": int(shuffle_version),
            "bucket_val": "user_id",  # TODO: make this handle device_id, etc.
            "log_bucketing": False,
            # "overrides": {}, # TODO: build this.
            # "targeting": targeting_tree(),
        },
    }


def make_overrides(variants):
    names = [v["name"] for v in variants]
    return {n: targeting_tree() for n in names}


def targeting_tree():
    """Generate a random targeting tree."""
    return {"EQ": {"field": "user_id", "values": ["3", "5", "7"]}}


def make_variants(h={}):
    return h or [  # TODO: actually generate variantsets.  Lowpri?
        {"range_start": 0.0, "range_end": 0.2, "name": "control_1"},
        {"range_start": 0.2, "range_end": 0.4, "name": "variant_2"},
        {"range_start": 0.4, "range_end": 0.6, "name": "variant_3"},
        {"range_start": 0.6, "range_end": 0.8, "name": "variant_4"},
    ]


def event_json(
    ctx: dict,
    noun: str,
    variant: str,
    experiment_name: Optional[str],
    experiment_id: Optional[int],
    is_override: Optional[bool],
    bucket_val: Optional[str] = None,
):
    event_thrift_json = {
        "1": {"str": "experiment"},
        "2": {"str": "expose"},
        "3": {"str": noun},
        "5": {"i64": ANY},
        "6": {"str": ANY},
        "8": {"str": ANY},
        "107": {
            "rec": {
                "2": {"str": APP_NAME},
                "4": {"i32": BUILD_NUMBER},
                "6": {"str": LOCALE_CODE},
            }
        },
        "109": {
            "rec": {
                "1": {"str": USER_AGENT},
                "3": {"str": BASE_URL},
            }
        },
        "110": {"rec": {"2": {"str": REFERRER_URL}}},
        "112": {
            "rec": {
                "1": {"str": USER_ID},
                "3": {"tf": int(IS_LOGGED_IN)},
                "4": {"i64": COOKIE_CREATED_TIMESTAMP},
                "16": {"tf": int(IS_EMPLOYEE)},
            }
        },
        "129": {
            "rec": {
                "1": {"i64": experiment_id},
                "2": {"str": experiment_name},
                "4": {"str": variant},
                "5": {"i64": ANY},
                "6": {"i64": ANY},
                "7": {"str": noun},
                "8": {"str": GEN_EXP_VERSION},
                "9": {"str": bucket_val or ctx_dict[noun]},
                "10": {"tf": int(is_override)},
            }
        },
        "500": {"rec": {"1": {"str": COUNTRY_CODE}}},
    }

    if "device_id" in ctx:
        event_thrift_json["108"] = {"rec": {"2": {"str": DEVICE_ID}}}

    if "canonical_url" in ctx:
        event_thrift_json["109"] = {
            "rec": {"17": {"str": CANONICAL_URL}, **event_thrift_json["109"]["rec"]}
        }

    if "subreddit_id" in ctx:
        event_thrift_json["114"] = {"rec": {"1": {"str": SUBREDDIT_ID}}}

    return event_thrift_json
