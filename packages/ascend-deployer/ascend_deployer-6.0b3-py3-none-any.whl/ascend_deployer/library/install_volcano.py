#!/usr/bin/env python3
# coding: utf-8
# Copyright 2024 Huawei Technologies Co., Ltd
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
import os.path

from ansible.module_utils.dl import Installer

logrotate_content = """/var/log/mindx-dl/volcano-*/*.log{
   daily
   rotate 8
   size 50M
   compress
   dateext
   missingok
   notifempty
   copytruncate
   create 0640 hwMindX hwMindX
   sharedscripts
   postrotate
       chmod 640 /var/log/mindx-dl/volcano-*/*.log
       chmod 440 /var/log/mindx-dl/volcano-*/*.log-*
   endscript
}"""


class VolcanoInstaller(Installer):
    component_name = 'volcano'
    secret_for_harbor = 'volcano-system-secret-for-harbor'

    def get_yaml_path(self):
        yaml_files = []
        for root, _, files in os.walk(self.extract_dir):
            for filename in files:
                if filename.endswith('.yaml'):
                    yaml_files.append(os.path.join(root, filename))
        if not yaml_files:
            self.module.fail_json('failed to find yaml')
        return sorted(yaml_files, reverse=self.use_new_k8s)[0]

    def build_images(self):
        build_dir = os.path.dirname(self.get_yaml_path())
        for tag, save_name in self.images.items():
            docker_file_name = 'Dockerfile-scheduler'
            if 'controller' in tag:
                docker_file_name = 'Dockerfile-controller'
            self.module.run_command('docker build -t {} -f {} .'.format(tag, docker_file_name),
                                    cwd=build_dir, check_rc=True)
            self.module.run_command('docker save -o {} {}'.format(save_name, tag), cwd=self.images_dir, check_rc=True)

    def create_log_dir(self):
        log_dir_names = ('volcano-controller', 'volcano-scheduler')
        for log_dir in log_dir_names:
            log_path = os.path.join(self.dl_log, log_dir)
            if not os.path.exists(log_path):
                os.makedirs(log_path, 0o750)
                os.chown(log_path, self.user_id, self.group_id)
        rotate_file = '/etc/logrotate.d/volcano'
        if os.path.exists('/etc/logrotate.d/volcano'):
            return
        with open(rotate_file, 'w') as f:
            f.write(logrotate_content)

    def get_modified_yaml_contents(self):
        return self._get_modified_yaml_contents('serviceAccount: volcano')

    def create_pull_secret(self):
        create_namespace_cmd = 'kubectl create namespace volcano-system'
        create_secret_cmd = 'kubectl create secret generic {} ' \
                            '--from-file=.dockerconfigjson=/root/.docker/config.json ' \
                            '--type=kubernetes.io/dockerconfigjson' \
                            ' -n volcano-system'.format(self.secret_for_harbor)
        self.module.run_command(create_namespace_cmd)
        self.module.run_command(create_secret_cmd)


if __name__ == '__main__':
    VolcanoInstaller().run()
