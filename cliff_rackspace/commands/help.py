import argparse
import sys

from cliff.command import Command


class HelpAction(argparse.Action):
    """
    Custom HelpAction which recognizes commands in <command> <sub command>
    format.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        app = self.default
        parser.print_help(app.stdout)
        app.stdout.write('\nCommands:\n')
        command_manager = app.command_manager

        for command, sub_commands in sorted(command_manager):
            for sub_command, ep in sub_commands.items():

                try:
                    factory = ep.load()
                except Exception as err:
                    app.stdout.write('Could not load %r\n' % ep)
                    continue

                try:
                    cmd = factory(self, None)
                except Exception as err:
                    app.stdout.write('Could not instantiate %r: %s\n' %
                                    (ep, err))
                    continue
                one_liner = cmd.get_description().split('\n')[0]

                if sub_command == 'index':
                    name = command
                else:
                    name = '%s %s' % (command, sub_command)

                app.stdout.write('  %-13s  %s\n' % (name, one_liner))
        sys.exit(0)


class HelpCommand(Command):
    """print detailed help for another command
    """

    def get_parser(self, prog_name):
        parser = super(HelpCommand, self).get_parser(prog_name)
        parser.add_argument('cmd',
                            nargs='*',
                            help='name of the command',
                            )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.cmd:
            try:
                the_cmd = self.app.command_manager.find_command(
                    parsed_args.cmd,
                )
                cmd_factory, cmd_name, search_args = the_cmd
            except ValueError:
                # Did not find an exact match
                cmd = parsed_args.cmd[0]
                fuzzy_matches = [k for k in self.app.command_manager
                                 if k[0].startswith(cmd)
                                 ]
                if not fuzzy_matches:
                    raise
                self.app.stdout.write('Command "%s" matches:\n\n' % (cmd))
                for fm in fuzzy_matches:
                    for sub_command, _ in fm[1].items():
                        self.app.stdout.write(' - %s %s\n' % (fm[0],
                                                              sub_command))
                return
            cmd = cmd_factory(self.app, search_args)
            full_name = (cmd_name
                         if self.app.interactive_mode
                         else ' '.join([self.app.NAME, cmd_name])
                         )
            cmd_parser = cmd.get_parser(full_name)
        else:
            cmd_parser = self.get_parser(' '.join([self.app.NAME, 'help']))
        cmd_parser.print_help(self.app.stdout)
        return 0
