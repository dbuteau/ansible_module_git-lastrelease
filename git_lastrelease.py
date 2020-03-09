#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Daniel BUTEAU <daniel.buteau@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import json, re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': 'preview',
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: git_lastrelease
short_description: get the latest release name and download links from github or gitlab
description: get the latest release name and download links from github or gitlab
version_added: 2.8.5
options:
    repo:
        description:
            - url to the git repo
        required: true
        choices: ['github.com', 'gitlab.com', 'gitlab.your_instance.suffix']
    namespace:
        description:
            - the group, namespace or owner where the git project is
        required: true
    project:
        description:
            - the name of the project, usually in the url it's the part before the .git
        required: true
    draft:
        description:
            - only used with github.com, set to true if you want to get the latest draft release
        required: false
        choices: [ 'true', 'false']
        default: 'false'
    prerelease:
        description:
            - put to yes if you want to get future release, false if only existing one
        required: false
        choices: [ 'true', 'false']
        default: 'false'
    token:
        description: 
            - if your project is not publicly available give your personnal token
        required: false

author: "Daniel BUTEAU (@daniel_buteau)"
'''

def list_releases(module, repo, namespace, project, token):
    if repo == "github.com":
        RELEASE_URL = "https://api.%s/repos/%s/%s/releases" % ('github.com', namespace, project)
        if token in vars() and token != '':
            headers = {
                "Accept": "application/json",
                "Authorization": ("token %s" % token)
            }
        else:
            headers = {"Accept": "application/json"}
    elif re.search('gitlab', repo):
        RELEASE_URL = "https://%s/api/v4/projects/%s%%2F%s/releases"  % (repo, namespace, project)
        if token in vars() and token != '':
            headers = {
                "Accept": "application/json",
                "Authorization": ("Bearer %s" % token)
            }
        else:
            headers = {"Accept": "application/json"}
    try:
        module.debug('debug %s' % RELEASE_URL)
        req = open_url(RELEASE_URL, headers=headers, timeout=6)
        return json.loads(req.read())
    except Exception as err:
        return module.fail_json(msg=str(err))

def select_release(releases, repo, draft, prerelease):
    if repo == "github.com" and draft == 'true':
        for key in releases:
            if key['draft'] == 'false':
                releases.pop(key)

        releases.sort(key=lambda r: r['created_at'])
        releases = releases[0]['name']
    elif prerelease == 'true':
        for key in releases:
            if repo == 'github.com':
                if key['prerelease'] == 'false':
                    releases.pop(key)
            else:
                if key['upcoming_release'] == 'false':
                    releases.pop(key)
        releases.sort(key=lambda r: r['created_at'])

    if repo == 'github.com':
        release = {
            'name': releases[0]['name'], 'links':
            [
                {'zip': releases[0]['zipball_url']},
                {'tar': releases[0]['tarball_url']}
            ]}
    else:
        release = {'name':releases[0]['name'], 'links': []}
        for rel_format, url in releases[0]['assets']['sources']:
            release['links'].append({rel_format: url})

    return release

def main():
    module = AnsibleModule(
        argument_spec=dict(
            repo=dict(required=True),
            namespace=dict(required=True),
            project=dict(required=True),
            draft=dict(required=False, default='false'),
            prerelease=dict(required=False, default='false'),
            token=dict(required=False)
        ),
        supports_check_mode=True
    )

    repo = module.params['repo']
    namespace = module.params['namespace']
    project = module.params['project']
    draft = module.params['draft']
    prerelease = module.params['prerelease']
    token = module.params['token']


    if module.check_mode:
        latest_release = {
            'name': 'v0.0.0', 'links':
            [
                {'zip'   : 'https://%s/%s/%s/%s-v0.0.0.zip' % (repo, namespace, project, project)},
                {'tar'   : 'https://%s/%s/%s/%s-v0.0.0.tar' % (repo, namespace, project, project)},
                {'tar.gz': 'https://%s/%s/%s/%s-v0.0.0.tgz' % (repo, namespace, project, project)}
            ]
        }
    else:
        try:
            releases = list_releases(module, repo, namespace, project, token)
            latest_release = select_release(releases, repo, draft, prerelease)
        except Exception as err:
            return module.fail_json(msg=str(err))

    return module.exit_json(results=latest_release)

if __name__ == '__main__':
    main()
