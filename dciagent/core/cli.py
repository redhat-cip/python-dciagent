#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
Unified command line interface for the DCI agents.

This script acts a single point of entry to execute all possible agents and
other utilities from DCI

This script auto-discovers agents in the `dciagent.agents` Namespace.
"""

import argparse
import importlib
import pkgutil
import sys

import dciagent.agents as agent_ns
import dciagent.core


def main(argv=[]):
    """
    Serve the main script entrypoint.

    Main entrypoint, the dci-agent-ctl script points here, receives only the
    arguments to the script.
    """

    ap = argparse.ArgumentParser(
        prog="dci-agent-ctl",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "-v",
        "--version",
        help="print the version",
        action="version",
        version="%(prog)s {}".format(dciagent.core.__version__),
    )

    sp = ap.add_subparsers(help="Agent to run")
    subs = {}

    # auto-discover agents, pretty much taken as-is from
    # https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-namespace-packages
    agents = {
        name: importlib.import_module(name)
        for finder, name, ispkg in pkgutil.iter_modules(
            agent_ns.__path__, agent_ns.__name__ + "."
        )
    }

    # build the sub-commands
    for fqa, mod in agents.items():
        # check if there's an Agent class defined in the agent module
        try:
            a = getattr(mod, "Agent")
            assert issubclass(a, dciagent.core.agent.base.Agent)
        except AttributeError:
            continue
        except AssertionError:
            continue
        agent = fqa.split(".")[-1]
        # add as a subparser
        subs[agent] = sp.add_parser(
            agent,
            help=mod.Agent.__doc__,
            description=mod.__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        for e in mod.Agent._args():
            args, kwargs = e.signature()
            subs[agent].add_argument(*args, **kwargs)
        subs[agent].set_defaults(Agent=mod.Agent)

    args = ap.parse_args()
    print(args)
    try:
        agent = args.Agent(**vars(args))
        args = agent.cli(argv)
        sys.exit(agent.run(args))
    except AttributeError:
        ap.print_help()
    except Exception as e:
        raise e

    return


# this only runs when you execute it through python cli.py
if __name__ == "__main__":
    sys.exit(main(sys.argv[2:]))
