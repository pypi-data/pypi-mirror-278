#!/usr/bin/env python3
# coding: utf-8
# Copyright 2024 Huawei Technologies Co., Ltd
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
import json
import os
import shutil
import socket
import ssl
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common_utils import get_protocol


class Harbor(object):
    docker_daemon = "/etc/docker/daemon.json"

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                current_hostname=dict(type='str'),
                harbor_server=dict(type='str', required=True),
                user=dict(type='str', required=True),
                password=dict(type='str', required=True, no_log=True),
                ca_file=dict(type='str', default='')
            )
        )
        self.current_hostname = self.module.params['current_hostname']
        self.harbor_server = self.module.params['harbor_server']
        self.user = self.module.params['user']
        self.password = self.module.params['password']
        self.ca_file = self.module.params['ca_file']
        self.facts = dict()

    @staticmethod
    def need_copy(src, dst):
        if not os.path.exists(dst):
            return True
        with open(src) as src_file, open(dst) as dst_file:
            src_content = src_file.read()
            dst_content = dst_file.read()
            return src_content != dst_content

    def handle_http(self):
        if not os.path.exists(self.docker_daemon):
            self.module.fail_json(msg='file {} not found'.format(self.docker_daemon))
        with open(self.docker_daemon) as f:
            content = json.load(f)
        insecure_registries = content.get('insecure-registries', [])
        if self.harbor_server not in insecure_registries:
            insecure_registries.append(self.harbor_server)
        content['insecure-registries'] = insecure_registries
        with open(self.docker_daemon, 'w') as f:
            json.dump(content, f, indent=4)

    def handle_https(self):
        cert_dir = '/etc/docker/certs.d/{}'.format(self.harbor_server)
        if not os.path.exists(cert_dir):
            os.makedirs(cert_dir, 0o755)
        cert_path = os.path.join(cert_dir, self.ca_file)
        if self.need_copy(self.ca_file, cert_path):
            shutil.copy(self.ca_file, cert_path)
        os.chmod(cert_path, 0o600)

    def login(self):
        cmd = 'docker login {} --username={} --password={}'.format(self.harbor_server, self.user, self.password)
        rc, out, err = self.module.run_command(cmd)
        if rc or 'Login Succeeded' not in out:
            self.module.fail_json(msg='login harbor failed, reason: {}'.format(err))

    def save_ca_cert(self):
        ca_file = '/etc/ssl/certs/{}'.format(self.harbor_server)
        hostname, port = self.harbor_server.rsplit(':', 1)
        port = int(port)
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        sock = socket.create_connection((hostname, port))
        wrap_sock = context.wrap_socket(sock, server_hostname=hostname)
        try:
            cert = wrap_sock.getpeercert(True)
            with open(ca_file, 'w') as f:
                f.write(ssl.DER_cert_to_PEM_cert(cert))
        finally:
            wrap_sock.close()
            sock.close()

    def run(self):
        protocol = get_protocol(self.module, self.harbor_server)
        use_http = protocol == 'http'
        self.facts['HARBOR_HTTP'] = use_http
        if self.current_hostname == 'localhost':
            self.module.exit_json(changed=False, msg='no need to login harbor', ansible_facts=self.facts)
        if use_http or not os.path.exists(self.ca_file):
            self.handle_http()
        else:
            self.handle_https()
        self.module.run_command('systemctl restart docker', check_rc=True)
        self.login()
        self.save_ca_cert()
        self.module.exit_json(changed=True, msg='login harbor ok', ansible_facts=self.facts)


if __name__ == '__main__':
    Harbor().run()
