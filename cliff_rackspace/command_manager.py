# Copyright 2012 Rackspace
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
from os.path import join as pjoin
from os.path import basename, splitext
from collections import defaultdict

from cliff.commandmanager import EntryPointWrapper

from cliff_rackspace.commands.help import HelpCommand

LOG = logging.getLogger(__name__)


class CommandManager(object):
    """
    Custom command manager which supports commands in the following format:
    <app> <command> <sub command>

    For example: registry services list
    """
    def __init__(self, namespace, commands_path):
        self.commands = defaultdict(dict)
        self.namespace = namespace
        self.commands_path = commands_path
        self._load_commands()

    def _load_commands(self):
        for commands_directory in os.listdir(self.commands_path):
            directory = pjoin(self.commands_path, commands_directory)

            if not os.path.isdir(directory):
                continue

            for command_file in os.listdir(directory):
                if not self._is_command_field(command_file):
                    continue

                name = splitext(basename(command_file))[0]
                module_name = os.path.dirname(__file__).split(os.sep)[-1]
                module_path = '%s.commands.%s.%s' % (self.namespace,
                                                     commands_directory,
                                                     name)
                command_class = '%sCommand' % (name.title().replace('-', ''))

                LOG.debug('Found command %s %s', directory, name)

                try:
                    mod = __import__(module_path, fromlist=[command_class])
                except ImportError, e:
                    LOG.debug('Failed to load module: %s' % (str(e)))
                    continue

                command_module = getattr(mod, command_class, None)

                if command_module is None:
                    LOG.debug('Module %s doesn\'t export %s class' %
                              (module_path, command_class))
                    continue

                wrapper = EntryPointWrapper(name=name,
                                            command_class=command_module)
                self.commands[commands_directory][name] = wrapper

    def _is_command_field(self, name):
        return name.endswith('.py') and name != '__init__.py'

    def __iter__(self):
        return iter(self.commands.items())

    def add_command(self, name, command_class):
        if name == 'help':
            # Overwrite HelpCommand with one which supports commands in the
            # <command> <sub command> class
            command_class = HelpCommand

        self.commands[name]['index'] = EntryPointWrapper(name, command_class)

    def find_command(self, argv, called_by_help=False):
        command = argv[0]

        if command == 'help':
            command_entry = self.commands.get('help', {}).get('index', None)
            cmd_factory = command_entry.load()
            args = argv[1:]
            return (cmd_factory, command, args)

        if len(argv) > 1:
            start_index = 2
            sub_command = argv[1]
        else:
            start_index = 1
            sub_command = 'index'

        command_entry = self.commands.get(command, {}).get(sub_command, None)

        if not command_entry:
            if called_by_help:
                raise ValueError('Unknown command: %r' %
                                 (' '.join(argv),))
            else:
                command_entry = self.commands.get('help', {}) \
                                             .get('index', None)
                cmd_factory = command_entry.load()
                args = [command]
                return (cmd_factory, command, args)

        cmd_factory = command_entry.load()
        args = argv[start_index:]
        command_name = '%s %s' % (command, sub_command)
        return (cmd_factory, command_name, args)
