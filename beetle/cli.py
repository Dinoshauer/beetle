import importlib
from .builder import Builder
from .base import Config
import sys
import os


class BeetlePluginImportError(Exception):
    pass


def render(config):
    builder = Builder(config)
    builder.run()

def _parse_plugin_name(plugin_name):
    return 'beetle_{0}'.format(plugin_name.replace('-', '_'))

def main():
    config = Config.from_path('config.yaml')

    commands = [
        {
            'name': 'render',
            'command': render,
            'args': [
                config
            ],
            'kwargs': {
            },
        },
    ]

    for plugin in config.plugins:
        try:
            a = importlib.import_module(_parse_plugin_name(plugin['name']))
            plugin['command'] = a.command
            commands.append(plugin)
        except ImportError, e:
            raise BeetlePluginImportError(e)

    for command in commands:
        try:
            command['command'](*command.get('args', []), **command.get('kwargs', {}))
        except KeyError, e:
            print 'Warning: "{0}" does not use the commands paradigm'.format(
                command['name']
            )
