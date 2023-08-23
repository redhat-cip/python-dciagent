# Copyright (C) 2021 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""
Just an example agent entrypoint.
"""

import sys

from dciagent.core import printer
from dciagent.core.agent import Argument
from dciagent.core.agent.dci import Agent as DCIAgent


class Agent(DCIAgent):
    """
    An example agent.
    """

    executable = "uptime"
    pretty = Argument("pretty print", short="-p", long="--pretty", action="store_true")

    def __init__(self, **kwargs):
        super().__init__("example-ctl", __doc__, "0.1", **kwargs)

    def _pre(self):
        printer.header("Running pre-execution hook")

    def _post(self):
        printer.header("Running post-execution hook")

    def _build_command(self):
        self.command_line = [self.executable]
        if self.pretty:
            self.command_line.append("-p")


def main(argv=[]):
    """
    Run the main entrypoint.
    """

    agent = Agent()
    args = agent.cli(argv)
    return agent.run(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
