import json
import os
from pathlib import Path
import sys
from typing import Any

import jsonschema
import jsonschema.protocols
import requests
from referencing import Registry, Resource

_DEFAULT_CACHE = str((Path.home() / ".mhhs-validate").resolve())
_DEFAULT_DOMAINS = "DataCatalogue,DataTypes,RealCommonBlocks,Interfaces-EventCodes,ECS-Reports,ECS-CommonBlocks"
CACHE = Path(os.environ.get("MHHS_VALIDATE_CACHE_DIR", _DEFAULT_CACHE))
VERSION = os.environ["MHHS_VALIDATE_VERSION"]
DOMAINS = os.environ.get("MHHS_VALIDATE_DOMAINS", _DEFAULT_DOMAINS).split(",")
ROOT_URL = "https://app.swaggerhub.com/apiproxy/schema/file/domains/MHHSPROGRAMME"


def validate() -> None:
    if not len(sys.argv) == 2:
        raise RuntimeError("Call with argument: mhhs-validate foo.json")
    _, data_path_str = sys.argv
    data = json.loads(Path(data_path_str).read_text())

    payload = data[0]["payload"]
    s0 = payload["CommonBlock"]["S0"]
    interface_id = s0["interfaceID"]
    event_code = s0["eventCode"][1:-1]
    interface_name = f"{interface_id}-{event_code}"

    if not CACHE.exists():
        CACHE.mkdir()
    if not (CACHE / VERSION).exists():
        (CACHE / VERSION).mkdir()

    # Put all of the definitions into a global urn:mhhs-validate namespace
    defs = {}
    for domain in DOMAINS:
        cached_json = (CACHE / VERSION) / f"{domain}.json"
        if not cached_json.exists():
            url = f"{ROOT_URL}/{domain}/{VERSION}?format=json"
            resp = requests.get(url)
            resp.raise_for_status()
            cached_json.write_text(json.dumps(resp.json(), indent=4))

        schemas = _replace_references(json.loads(cached_json.read_text()))
        for k, v in schemas["components"]["schemas"].items():
            v["$anchor"] = k
            defs[k] = v

    resource = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:mhhs-validate",
        "$defs": defs,
    }

    registry = Resource.from_contents(resource) @ Registry()
    print(f"Validating {interface_name} message")
    validator = jsonschema.Draft202012Validator(defs[interface_name], registry=registry)
    validator.validate(payload)
    print(data_path_str, "appears valid")


def _replace_references(o: Any) -> Any:
    if isinstance(o, list):
        return [_replace_references(n) for n in o]
    if isinstance(o, dict):
        # `nullable` is an OpenAPI thing, to conform to JSONSchema
        # we replace `type: T` with `type: [T, null]`
        # There may be other inconsistencies!
        if o.get("nullable") is True:
            o["type"] = [o["type"], "null"]
        return {k: _replace_references(v) for k, v in o.items()}
    if isinstance(o, str) and "#/components/schemas/" in o:
        l, r = o.split("#/components/schemas/")
        return "urn:mhhs-validate#" + r
    return o
