#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===========================================================================
import glob
import os
import json
import platform
import tarfile
import shlex

from ansible.module_utils.urls import fetch_url
from ansible.module_utils._text import to_text
from ansible.module_utils.common_info import get_os_and_arch


def get(module, url):
    resp, info = fetch_url(module, url, method='GET', use_proxy=False)
    try:
        content = resp.read()
    except AttributeError:
        content = info.pop('body', '')
    return to_text(content, encoding='utf-8')


def get_protocol(module, host):
    https_url = 'https://{}/c/login'.format(host)
    content = get(module, https_url)
    if 'Not Found' in content:
        return 'https'
    if 'wrong version number' in content:
        return 'http'

    http_url = 'http://{}/c/login'.format(host)
    content = get(module, http_url)
    if 'The plain HTTP request was sent to HTTPS port' in content:
        return 'https'
    return 'http'


def clean_env():
    for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
        os.environ.pop(key, None)


def ensure_nerdctl_installed(module, resources_dir):
    if module.get_bin_path('nerdctl'):
        module.log(msg='nerdctl is already installed, skip')
        return
    tar_name = 'nerdctl-1.4.0-linux-arm64.tar.gz'
    if platform.machine() == 'x86_64':
        tar_name = 'nerdctl-1.4.0-linux-amd64.tar.gz'
    tool_path = os.path.join(resources_dir, 'tool', tar_name)
    if not os.path.exists(tool_path):
        module.log(msg='failed to find pkg: {}, skip'.format(tool_path))
        return
    with tarfile.open(tool_path) as f:
        members = []
        bin_name = 'nerdctl'
        for member in f.getmembers():
            if member.name == bin_name:
                members.append(member)
                break
        f.extractall('/usr/bin/', members=members)
        os.chmod('/usr/bin/nerdctl', 0o750)
    module.log(msg='install nerdctl successfully')


def ensure_docker_daemon_exist(module):
    docker_daemon = "/etc/docker/daemon.json"
    if os.path.exists(docker_daemon):
        return
    content_dict = dict()
    rpm = module.get_bin_path('rpm')
    if not rpm:
        content_dict.update({
            "exec-opts": ["native.cgroupdriver=systemd"],
            "live-restore": True
        })
    elif get_os_and_arch().startswith('OpenEuler'):
        content_dict.update({
            "live-restore": True
        })
    docker_config_path = os.path.dirname(docker_daemon)
    if not os.path.exists(docker_config_path):
        os.makedirs(docker_config_path, mode=0o750)
    with open(docker_daemon, 'w') as f:
        json.dump(content_dict, f, indent=4)
    module.run_command('systemctl daemon-reload')
    module.run_command('systemctl restart docker')


def find_files(path, pattern):
    messages = ["try to find {} for {}".format(path, pattern)]
    matched_files = glob.glob(os.path.join(path, pattern))
    messages.append("find files: " + ",".join(matched_files))
    return matched_files, messages


def run_command(module, command, ok_returns=None, working_dir=None):
    messages = ["calling " + command]
    return_code, out, err = module.run_command(shlex.split(command), cwd=working_dir)
    output = out + err
    if not ok_returns:
        ok_returns = [0]
    if return_code not in ok_returns:
        raise Exception("calling {} failed on {}: {}".format(command, return_code, output))
    messages.append("output of " + command + " is: " + str(output))
    return output, messages


def result_handler(failed_msg=""):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                res, msgs = func(self, *args, **kwargs)
                self.messages.extend(msgs)
            except Exception as e:
                self.messages.append(failed_msg)
                raise e
            if not res:
                raise Exception(failed_msg)

            return res

        return wrapper

    return decorator
