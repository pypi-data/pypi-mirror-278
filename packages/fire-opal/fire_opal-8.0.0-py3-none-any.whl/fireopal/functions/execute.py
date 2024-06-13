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

from typing import Optional

from fireopal._utils import log_activity
from fireopal.config import get_config
from fireopal.credentials import Credentials
from fireopal.functions._utils import (
    check_circuit_submission_validity,
    handle_single_item,
)

from ..fire_opal_job import FireOpalJob
from .base import async_fire_opal_workflow


@async_fire_opal_workflow("compile_and_run_workflow")
def execute(
    circuits: str | list[str],
    shot_count: int,
    credentials: Credentials,
    backend_name: str,
    parameters: Optional[dict[str, float] | list[dict[str, float]]] = None,
) -> FireOpalJob:
    """
    Execute a batch of `circuits` where `shot_count` measurements are taken per circuit.

    Parameters
    ----------
    circuits : str or list[str]
        Quantum circuit(s) in the form of a QASM strings. You may use Qiskit to
        generate these strings.
    shot_count : int
        Number of bitstrings that are sampled from the final quantum state.
    credentials : Credentials
        The credentials for running circuits. See the `credentials` module for functions
        to generate credentials for your desired provider.
    backend_name : str
        The backend device name that should be used to run circuits.
    parameters : dict[str, float] or list[dict[str, float]] or None, optional
        The list of parameters for the circuit(s), if they're parametric.
        Defaults to None.

    Returns
    -------
    FireOpalJob
        A job object for querying execution results.
    """
    log_activity(
        function_called="execute",
        circuits=circuits,
        shot_count=shot_count,
        backend_name=backend_name,
        parameters=parameters,
    )

    check_circuit_submission_validity(
        circuits=circuits,
        shot_count=shot_count,
        credentials=credentials,
        backend_name=backend_name,
        parameters=parameters,
    )
    circuits = handle_single_item(circuits)
    if parameters:
        parameters = handle_single_item(parameters)

    settings = get_config()
    credentials_with_org = credentials.copy()
    credentials_with_org.update({"organization": settings.organization})
    return {
        "circuits": circuits,
        "shot_count": shot_count,
        "credentials": credentials_with_org,
        "backend_name": backend_name,
        "parameters": parameters,
    }  # type: ignore[return-value]
