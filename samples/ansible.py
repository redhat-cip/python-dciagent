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
A DCI ansible control command for the OpenShift agent
"""

import os
import sys

from dciagent.core.agent.ansible import Agent as AnsibleAgent


class Agent(AnsibleAgent):
    "ansible-ctl"

    default_playbook = os.path.join(os.path.dirname(__file__), "playbook.yml")

    def __init__(self, **kwargs):
        super().__init__(self.__doc__, __doc__, "0.1", **kwargs)


def main():
    agent = Agent()
    args = agent.cli(sys.argv[1:])
    return agent.run(args)


if __name__ == "__main__":
    sys.exit(main())
