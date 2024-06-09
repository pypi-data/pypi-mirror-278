# coding=utf8
"""Sopel Slap plugin

Plugin for Sopel that lets users slap each other in fun ways.

Original slap.py copyright 2009, Michael Yanovich, yanovich.net.

This rewritten & packaged version for Sopel 7.1+:
Copyright 2023, dgw, technobabbl.es

https://sopel.chat
"""
import random

from sopel import formatting, plugin, tools

VERBS = (
    'annihilates',
    'destroys',
    'kicks',
    'owns',
    'punches',
    'pwns',
    'roundhouse kicks',
    'slaps',
)


@plugin.commands('slap', 'slaps')
def slap(bot, trigger):
    """Slap a <target> (e.g. nickname)"""
    target = trigger.group(3)

    if target is None:
        target = trigger.nick
    else:
        target = formatting.plain(target)

    # ensure target is an Identifier to increase reliability of "is nick" check
    if not isinstance(target, tools.Identifier):
        if hasattr(bot, 'make_identifier'):
            target = bot.make_identifier(target)
        else:
            # TODO: remove once Sopel 7 support is dropped
            target = tools.Identifier(target)

    if not target.is_nick():
        bot.reply("You can't slap the whole channel!")
        return

    if target not in bot.channels[trigger.sender].users:
        bot.reply("You can't slap someone who isn't here!")
        return

    if target == bot.nick:
        if not trigger.admin:
            target = trigger.nick
        else:
            target = 'itself'

    if target in bot.config.core.admins and not trigger.admin:
        target = trigger.nick

    verb = random.choice(VERBS)

    bot.action(f"{verb} {target}")
