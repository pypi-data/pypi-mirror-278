#!/usr/bin/env python3
# coding: utf-8
# Copyright 2023 Huawei Technologies Co., Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ===========================================================================
import json
import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
from ansible.module_utils.common_utils import get_protocol, clean_env


class ManifestData(object):
    arch = ''
    image_name = ''
    image_name_with_arch = ''
    manifest_name = ''
    manifest_name_with_arch = ''

    def __init__(self, prefix, image_name, arch):
        self.arch = arch
        self.image_name = image_name
        name, tag = image_name.split(':')
        self.image_name_with_arch = '{}_{}:{}'.format(name, arch, tag)
        self.manifest_name = '{}/{}'.format(prefix, image_name)
        self.manifest_name_with_arch = '{}/{}'.format(prefix, self.image_name_with_arch)


class ImagePusher(object):
    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                harbor_server=dict(type='str', required=True),
                project_name=dict(type='str', required=True),
                public=dict(type='str', required=True),
                url_username=dict(type='str', aliases=['user'], required=True),
                url_password=dict(type='str', aliases=['password'], required=True, no_log=True),
                image_dir=dict(type='str', required=True),
                component_name=dict(type='str', required=True),
                validate_certs=dict(type='bool', default=False),
                force_basic_auth=dict(type='bool', default=True),
            )
        )
        self.harbor_server = self.module.params['harbor_server']
        self.project_name = self.module.params['project_name']
        self.public = self.module.params['public']
        self.image_dir = os.path.expanduser(self.module.params['image_dir'])
        self.component_name = self.module.params['component_name']
        self.prefix = '{}/{}'.format(self.harbor_server, self.project_name)
        self.protocol = None
        self.image_tags = []

    def create_harbor_project(self):
        if not self.protocol:
            self.protocol = get_protocol(self.module, self.harbor_server)
            self.module.log(msg='harbor server uses {} protocol'.format(self.protocol))
        url = '{}://{}/api/v2.0/projects'.format(self.protocol, self.harbor_server)
        data = json.dumps({
            "project_name": self.project_name,
            "metadata": {"public": self.public},
            "storage_limit": -1
        })
        headers = {'Content-Type': 'application/json'}
        fetch_url(self.module, url, data=data, headers=headers, method='POST', use_proxy=False, timeout=30)
        self.module.log(msg='create harbor project successfully')

    def run_cmd(self, args, **kwargs):
        rc, out, err = self.module.run_command(args, **kwargs)
        self.module.log(msg='run cmd: {} successfully'.format(args))
        return rc, out, err

    def tag_image(self, image_file, dir_path, arch):
        rc, out, err = self.run_cmd('docker load -i {}'.format(image_file), cwd=dir_path)
        if rc or err or not out:
            self.module.fail_json(msg='failed to load image: {} in {}'.format(image_file, dir_path))
        for line in out.splitlines():
            if 'Loaded image:' in line:
                image_name = line.replace('Loaded image:', '').strip()
                data = ManifestData(self.prefix, image_name, arch)
                tag_cmd = 'docker tag {} {}'.format(image_name, data.manifest_name_with_arch)
                self.run_cmd(tag_cmd, check_rc=True)
                return data
        else:
            return self.module.fail_json(msg='failed to find image name: {}'.format(out))

    def parse_image_tags(self):
        for arch in os.listdir(self.image_dir):
            dir_path = os.path.join(self.image_dir, arch, self.component_name)
            for image_file in os.listdir(dir_path):
                if arch not in image_file:
                    continue
                manifest_data = self.tag_image(image_file, dir_path, arch)
                self.image_tags.append(manifest_data)
        if not self.image_tags:
            self.module.fail_json(
                msg='no valid image for component: {} found in path: {}'.format(self.component_name, self.image_dir))

    def clean_old_manifest(self):
        for name in set([data.manifest_name for data in self.image_tags]):
            cmd = 'docker manifest rm {}'.format(name)
            self.run_cmd(cmd)

    def create_manifest_node(self):
        for data in self.image_tags:
            self.run_cmd('docker push {}'.format(data.manifest_name_with_arch), check_rc=True)
            self.run_cmd('docker manifest create --insecure {} --amend {}'.format(
                data.manifest_name, data.manifest_name_with_arch), check_rc=True)
            self.run_cmd('docker manifest annotate --arch {} {} {}'.format(
                'amd64' if data.arch == 'x86_64' else 'arm64',
                data.manifest_name,
                data.manifest_name_with_arch
            ), check_rc=True)

    def push_manifest(self):
        for name in set([data.manifest_name for data in self.image_tags]):
            cmd = 'docker manifest push -p --insecure {}'.format(name)
            self.run_cmd(cmd, check_rc=True)

    def run(self):
        clean_env()
        self.create_harbor_project()
        self.parse_image_tags()
        self.clean_old_manifest()
        self.create_manifest_node()
        self.push_manifest()
        self.module.exit_json(msg='push image successfully')


if __name__ == '__main__':
    ImagePusher().run()
