slack-logbot
============

Retrieve and print logs from Slack channels and groups to the console.

Usage
~~~~~

- Create a Python 3 venv
- ``pip install -r requirements.txt``
- Create a ``.env`` file in the same folder containing a Slack user token and
  a list of channels to retrieve::

      TOKEN=xoxp-...
      GROUPS="general:C:.. channel2:C... group:G..."

  Search Google to find out how to retrieve a user token. The channel and group
  IDs can be found easily by opening Slack in the browser and looking at the
  location bar while inside a channel.
- Run ``python logbot.py`` and enjoy, or even better, add the following to a
  crontab of your choice::

    0 6 * * * .../bin/python logbot.py | mail -s slack-logbot yourmail@example.com

- Enjoy the quiet that comes from not missing out on stuff that is only
  communicated via Slack, while completely avoiding the stress that comes from
  obsessively checking Slack all the time.
