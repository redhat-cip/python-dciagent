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
Module for the base agent.
"""
import argparse
import shutil
import subprocess

import dciagent.core.agent as agent
import dciagent.core.context as ctx
import dciagent.core.error as error
import dciagent.core.printer as printer


class Agent(object):
    """
    The most basic agent class.

    An agent is, down to its core, just a command that executes some
    validations and then runs a given command.
    """

    executable = None
    environment = {}
    command_line = []
    ap = None
    verbosity = agent.Argument(
        "increase the verbosity",
        short="-v",
        long="--verbosity",
        default=0,
        action="count",
        env="VERBOSITY",
    )
    dry_run = agent.Argument(
        "do not run the command line, only print it",
        long="--dry-run",
        action="store_true",
        default=False,
        env="DRY_RUN",
    )
    no_validation = agent.Argument(
        "UNSAFE: skip various validations e.g. full path, file checks, etc",
        long="--no-validation",
        action="store_true",
        default=False,
        env="NO_VALIDATION",
    )

    def __init__(self, prog, desc, version, parents=[], *args, **kwargs):
        self.ap = argparse.ArgumentParser(
            prog=prog,
            description=desc,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=parents,
        )
        self.ap.add_argument(
            "-V", "--version", action="version", version="{} {}".format(prog, version)
        )

    def _build_command(self):
        """
        Build the command line.

        The list will be fed to Popen at execution time. Child classes
        inheriting from here should define/override their own method to
        actually run, as this method is here at this level only for flow
        control.
        """

        raise NotImplementedError("Define the _build_command() method in your agent")

    def cli(self, argv):
        """
        Build the CLI with `argparse.parse_args()` and return arguments.
        """

        for e in self._args():
            args, kwargs = e.signature()
            self.ap.add_argument(*args, **kwargs)

        return self.ap.parse_args(argv)

    @classmethod
    def _args(cls):
        """
        Return all arguments defined in the class.

        This loops the object members looking for Argument objects.
        """

        attrs = []
        for m in sorted(dir(cls)):
            e = getattr(cls, m)
            if isinstance(e, agent.Argument):
                attrs.append(e)

        return attrs

    def _load_args(self, args):
        """
        Loop through all class elements to parse all `Argument` objects.

        All arguments defined at the class level are then overwritten with
        their actual values for easier access.
        """

        for k, v in args.items():
            e = getattr(self, k)
            if isinstance(e, agent.Argument):
                if e.type is None:
                    if e.action == "count":
                        value = int(v)
                    elif e.action in (
                        "store_true",
                        "store_false",
                    ):
                        value = bool(v)
                    else:
                        value = v
                elif e.type == int:
                    value = int(v)
                elif e.type == float:
                    value = float(v)
                elif e.type == bool:
                    value = bool(v)
                else:
                    value = str(v)

                setattr(self, k, value)

    def _build_env(self):
        """
        Override in child classes to construct your execution environment.
        """

        pass

    def _normalize(self):
        """
        Normalize and fully qualify command and arguments.

        Classes inheriting should _extend_ from this method, in other words,
        they should call `super()._normalize()` at some point.
        """

        if self.executable is not None:
            self.executable = shutil.which(self.executable)

    def _validate(self):
        """
        Validate that the executable exists and arguments are valid.

        Classes inheriting should _extend_ from this method, in other words,
        they should call `super()._validate()` at some point.
        """

        if self.executable is None:
            raise (error.ValidationError("The defined executable does not exist"))

    def _pre(self):
        """
        Execute the pre-execution hook, override to define.
        """

        pass

    def _post(self):
        """
        Execute the post-execution hook, override to define.
        """

        pass

    def run(self, args):
        """
        Run the command line.

        This is the main body of the execution agent. According to the
        configuration it will build the command line and then run it via Popen.
        """

        self._load_args(vars(args))
        self._normalize()

        if not self.no_validation:
            self._validate()

        self._pre()
        self._build_command()
        self._build_env()

        if self.verbosity > 0:
            if len(self.environment) > 0:
                with printer.section("Running with the following extra environment:"):
                    for k, v in self.environment.items():
                        val = v
                        if "password" in k.lower() or "secret" in k.lower():
                            val = "<redacted>"
                        print("{}={}".format(k, val))

        rc = 0
        try:
            if self.dry_run:
                with printer.section("Dry-run mode, should execute this command:"):
                    print(" \\\n".join(self.command_line))
            else:
                if len(self.command_line) > 0:
                    with ctx.env(**self.environment):
                        p = subprocess.Popen(self.command_line)
                        p.communicate()
                        rc = p.returncode
        finally:
            self._post()

        return rc
