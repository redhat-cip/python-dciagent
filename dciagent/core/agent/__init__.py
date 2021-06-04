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
Module for the base classes used by the agents.
"""

import distutils.util as distutil
import os

import dciagent.core.error as error


class Argument:
    """
    An abstraction to define arguments at the class level.
    """

    def __init__(
        self,
        help,
        short=None,
        long=None,
        action=None,
        default=None,
        env=None,
        type=None,
        nargs=None,
        dest=None,
        metavar=None,
    ):
        if nargs is None and short is None and long is None:
            raise error.ArgumentError(
                "Need to define one of short or long argument forms"
            )

        self.help = help
        self.short = short
        self.long = long
        self.action = action
        self.default = default
        self.env = env.upper() if env else None
        self.type = type
        self.nargs = nargs
        self.dest = dest
        self.metavar = metavar

    def signature(self):
        """
        Return argument items to be fed to an `add_argument()` call.

        This returns an args[] and a kwargs{} objects to the caller, which then
        can be fed to the constructor.
        """

        args = []
        if self.short is not None:
            args.append(self.short)
        if self.long is not None:
            args.append(self.long)

        # format help
        help_str = "{}".format(self.help)
        if self.env is not None or self.default is not None:
            help_str += " ("
            if self.env is not None:
                help_str += " env: ${}".format(self.env)
            if self.default is not None:
                help_str += " default: {}".format(self.default)
            help_str += " )"

        kwargs = {
            "help": help_str,
            "action": self.action,
            "dest": self.dest,
        }

        # figure out the right default
        default = None
        if self.env is not None:
            if self.action in (
                "store_true",
                "store_false",
            ):
                default = distutil.strtobool(os.getenv(self.env, "false"))
            else:
                default = os.getenv(self.env, self.default)
        else:
            default = self.default

        kwargs["default"] = default

        if self.type is not None:
            kwargs["type"] = self.type

        if self.nargs is not None:
            kwargs["nargs"] = self.nargs

        if self.metavar is not None:
            kwargs["metavar"] = self.metavar

        return (args, kwargs)
