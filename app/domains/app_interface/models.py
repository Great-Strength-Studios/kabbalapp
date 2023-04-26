from typing import List
from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist
from schematics.types.serializable import serializable

class AppArgument(Model):
    pass

class AppSubcommand(Model):
    arguments = t.ListType(t.ModelType(AppArgument), default=[])

class AppCommand(Model):
    subcommands = t.DictType(t.ModelType(AppSubcommand), default={})

class AppInterface(Model):
    commands = t.DictType(t.ModelType(AppCommand), default={})