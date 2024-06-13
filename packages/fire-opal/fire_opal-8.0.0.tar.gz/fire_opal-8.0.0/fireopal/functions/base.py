# Copyright 2024 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

from __future__ import annotations

from functools import partial
from typing import (
    Any,
    Callable,
)

from qctrlworkflowclient import (
    core_workflow,
    print_warnings,
)
from qctrlworkflowclient.functions import async_core_workflow
from qctrlworkflowclient.router.api import (
    Action,
    DecodedResult,
)

from fireopal.config import get_config
from fireopal.fire_opal_job import FireOpalJob


def _formatter(input_: DecodedResult) -> Any:
    result = input_.decoded
    if isinstance(result, dict):
        return print_warnings(result)
    return result


def _async_formatter(input_: dict[str, Action]) -> FireOpalJob:
    assert isinstance(input_, dict) and input_.get("async_result") is not None
    return FireOpalJob(action=input_["async_result"])


fire_opal_workflow: Callable = partial(core_workflow, get_config, formatter=_formatter)
async_fire_opal_workflow: Callable = partial(
    async_core_workflow, get_config, formatter=_async_formatter
)
