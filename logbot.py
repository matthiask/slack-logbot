from datetime import datetime
from speckenv import read_speckenv, env
import requests


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
        member['id']: '%s (%s)' % (
            member.get('real_name', '?'),
            member['name'],
        )
        for member in response['members']
    }


def fetch(channel):
    response = requests.get(
        'https://slack.com/api/conversations.history',
        params={
            'token': token,
            'channel': channel,
            'count': 1000,
            'oldest': datetime.now().timestamp() - 86400 - 3600,
        },
    ).json()

    return response


def log(user_dict, channel):
    data = fetch(channel)
    log = ['']
    for item in data['messages']:
        if item['type'] == 'message' and 'user' in item:
            log.append('%s at %s:\n%s' % (
                user_dict.get(item['user'], item['user']),
                datetime.fromtimestamp(float(item['ts'])).isoformat(),
                item['text'],
            ))
        else:
            log.append(repr(item))

    return '\n\n'.join(reversed(log))


def header(text):
    return (text.upper() + ' ' + '#' * 70)[:70]


if __name__ == '__main__':
    # from pprint import pprint
    # pprint(fetch())
    # pprint(users())
    user_dict = users()
    for name, channel in groups:
        print(header(name))
        print(log(user_dict, channel))
