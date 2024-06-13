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

import logging
from typing import Optional

import networkx as nx
from qctrlcommons.exceptions import QctrlArgumentsValueError
from sympy import Expr

from fireopal._utils import log_activity
from fireopal.credentials import Credentials

from ..fire_opal_job import FireOpalJob
from .base import async_fire_opal_workflow


@async_fire_opal_workflow("solve_qaoa_workflow")
def solve_qaoa(
    problem: Expr | nx.Graph,
    credentials: Credentials,
    problem_type: Optional[str] = None,
    backend_name: Optional[str] = None,
) -> FireOpalJob:
    """
    Solve a QAOA problem.

    Parameters
    ----------
    problem : Expr or nx.Graph
        The QAOA problem definition, represented as either an
        `nx.Graph` or `sympy.Expr`.
    credentials : Credentials
        The credentials for running circuits on an IBM backend.
        Use the `make_credentials_for_ibmq` function from the `credentials` module
        to generate properly formatted credentials.
    problem_type : str, optional
        The class of QAOA problem to solve. Required for graph problem definitions,
        which currently only includes support for "maxcut".
    backend_name : str, optional
        The backend device that should be used to run circuits. Defaults to None.

    Returns
    -------
    FireOpalJob
        A job object containing results and warnings from the execution. The
        results have the following keys:
        final_aggregate_cost (float)
        final_bitstring_distribution (dict[str, int])
        solution_bitstring (str)
        iteration_count (int)
    """
    log_activity(
        function_called="solve_qaoa",
        problem=problem,
        problem_type=problem_type,
        backend_name=backend_name,
    )
    if isinstance(problem, nx.Graph):
        if not isinstance(problem_type, str):
            logging.error(
                "QCTRL - problem_type is required when a Graph problem is provided."
            )
            raise QctrlArgumentsValueError(
                "problem_type is required when a Graph problem is provided",
                arguments={
                    "type(problem)": type(problem),
                    "type(problem_type)": type(problem_type),
                },
            )
    else:
        # Note: Forcing `problem_type` to `""` to avoid passing None down QAOA stack.
        problem_type = ""

    print(
        "This function performs multiple circuit executions. "
        "The total execution time is expected to take a few minutes but will take "
        "much longer if waiting in the public queue. It is highly recommended to visit "
        "https://quantum-computing.ibm.com/reservations and make a dedicated reservation.\n"
    )
    print("Visit https://quantum-computing.ibm.com/jobs to check your queue position.")
    return {
        "problem": problem,
        "problem_type": problem_type,
        "credentials": credentials,
        "backend_name": backend_name,
    }  # type: ignore[return-value]
