# sopel-slap

Plugin for Sopel that lets users slap each other in fun ways

## Installation

```sh
pip install sopel-slap
```

_Substitute the appropriate `pip` command based on your environment (e.g.
`pip3` or `pip3.10` on systems with multiple Python versions available)._

_If your Sopel configuration requires it, run `sopel-plugins enable slap`,
passing the appropriate config name to `-c` if you have multiple bots._

## Commands

<dl>
  <dt>.slap</dt>
  <dd>Make the bot slap you</dd>

  <dt>.slap nickname [reason]</dt>
  <dd>Slap someone else, with an optional reason</dd>
</dl>

_If your bot has a non-default `prefix`, substitute it for `.` above._

## Credits

This is based on [the original `slap.py`][original-slap.py] by Michael Yanovich
from [sopel-extras][], dating back to the late '00s/early '10s. It's been
rewritten more or less from scratch to do things in the modern Sopel way. The
only meaningful behavior change was dropping substitution of the caller's nick
for `me` and `myself`, as it's quite possible for a real person to use either of
those as a nick and _no one_\* should be safe from slaps!

\* — No one except the bot and its admins, that is.

[original-slap.py]: https://github.com/sopel-irc/sopel-extras/blob/81ee756223474cacdac6f5847772d6085d006a50/slap.py
[sopel-extras]: https://github.com/sopel-irc/sopel-extras
