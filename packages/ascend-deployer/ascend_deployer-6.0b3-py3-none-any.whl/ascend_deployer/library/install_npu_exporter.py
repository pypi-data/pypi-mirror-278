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


class NpuExporterInstaller(Installer):
    component_name = 'npu-exporter'
    secret_for_harbor = 'npu-exporter-secret-for-harbor'

    def get_modified_yaml_contents(self):
        return self._get_modified_yaml_contents('containers:')

    @staticmethod
    def get_labels():
        return []

    def create_pull_secret(self):
        create_namespace_cmd = 'kubectl create namespace npu-exporter'
        create_secret_cmd = 'kubectl create secret generic {} ' \
                            '--from-file=.dockerconfigjson=/root/.docker/config.json ' \
                            '--type=kubernetes.io/dockerconfigjson' \
                            ' -n npu-exporter'.format(self.secret_for_harbor)
        self.module.run_command(create_namespace_cmd)
        self.module.run_command(create_secret_cmd)


if __name__ == '__main__':
    NpuExporterInstaller().run()
