from datetime import datetime
import re
import requests
from speckenv import read_speckenv, env


read_speckenv()
token = env('TOKEN', required=True)
groups = [
    group.split(':')
    for group in env('GROUPS', required=True).split()
]


def users():
    response = requests.get(
        'https://slack.com/api/users.list',
        params={
            'token': token,
            'limit': 1000,
            'presence': 'false',
        },
    ).json()

    return {
        member['id']: member['name'] for member in response['members']
    }


def fetch(channel):
    response = requests.get(
        'https://slack.com/api/conversations.history',
        params={
            'token': token,
            'channel': channel,
            'count': 1000,
            'oldest': datetime.now().timestamp() - 10 * 86400 - 3600,
        },
    ).json()

    return response


def fill_usernames(user_dict, text):
    def id_to_user(match):
        id = match.groups()[0]
        return '@' + user_dict.get(id, id)

    return re.sub(r'<@(\w+)>', id_to_user, text)


def format_attachments(item):
    lines = []
    if item.get('text'):
        lines.append(item['text'])
    for attachment in item['attachments']:
        lines.extend(
            line for line in (
                attachment.get('title'),
                attachment.get('title_link'),
                attachment.get('text'),
            ) if line
        )
    return '\n'.join(lines)


def log(user_dict, channel):
    data = fetch(channel)
    log = ['']
    for item in data['messages']:
        if item['type'] == 'message' and 'user' in item:
            log.append('%s at %s:\n%s' % (
                user_dict.get(item['user'], item['user']),
                datetime.fromtimestamp(float(item['ts'])).strftime(
                    '%Y-%m-%d %H:%M:%S',
                ),
                fill_usernames(user_dict, item['text']),
            ))
        elif item.get('subtype') == 'bot_message' and 'attachments' in item:
            log.append('%s at %s:\n%s' % (
                item.get('username', '(Bot)'),
                datetime.fromtimestamp(float(item['ts'])).strftime(
                    '%Y-%m-%d %H:%M:%S',
                ),
                format_attachments(item),
            ))
        else:
            log.append(repr(item))

    return '\n\n'.join(reversed(log))


def header(text):
    return (text.upper() + ' ' + '#' * 50)[:50]


if __name__ == '__main__':
    # from pprint import pprint
    # pprint(fetch())
    # pprint(users())
    user_dict = users()
    # pprint(user_dict)
    for name, channel in groups:
        print(header(name))
        print(log(user_dict, channel))
