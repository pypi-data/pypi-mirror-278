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

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.check_output_manager import check_event, set_error_msg
from ansible.module_utils.common_info import get_os_and_arch, get_npu_info
from ansible.module_utils.common_utils import run_command
from ansible.module_utils.compatibility_config import EOL_CARD, EOL_MODEL, CARD_DICT, MODEL_TAGS_NOT_SUPPORT, \
    OS_ARCH_TAGS_SUPPORT

EOL_MSG = "[ASCEND] The lifecycle of {} is over and is no longer supported"
SUPPORT_MSG = "[ASCEND] {} has no support for {} on this device"


class CompatibilityCheck(object):
    def __init__(self):
        self.module = AnsibleModule(argument_spec=dict(tags=dict(type='list')))
        self.tags = self.module.params['tags']
        if 'all' in self.tags:
            self.tags.remove('all')
        self.npu_info = get_npu_info()
        self.os_and_arch = get_os_and_arch()
        self.error_messages = []

    def record_error(self, msg):
        if msg not in self.error_messages:
            self.error_messages.append(msg)
            set_error_msg(msg)

    def run(self):
        self.check_card()
        self.check_model()
        self.check_os()
        self.check_sys_pkg()
        if self.error_messages:
            return self.module.fail_json('\n'.join(self.error_messages))
        self.module.exit_json(changed=True, rc=0)

    @check_event
    def check_card(self):
        card = self.npu_info.get('card')
        if card in EOL_CARD:
            self.record_error(EOL_MSG.format(card))
        support_os_arch_list = CARD_DICT.get(card)
        if support_os_arch_list and self.os_and_arch not in support_os_arch_list:
            self.record_error(SUPPORT_MSG.format(card, self.os_and_arch))

    @check_event
    def check_model(self):
        model = self.npu_info.get('model')
        if model in EOL_MODEL:
            self.record_error(EOL_MSG.format(model))
        unsupported_tags = MODEL_TAGS_NOT_SUPPORT.get(model, [])
        for tag in self.tags:
            if tag in unsupported_tags:
                self.record_error(SUPPORT_MSG.format(tag, model))

    @check_event
    def check_os(self):
        not_support_components = []
        supported_tags = OS_ARCH_TAGS_SUPPORT.get(self.os_and_arch, [])
        infer_devices = ('A300i-pro', 'A300i-duo', 'A200i-a2', 'Atlas 800I A2')
        card = self.npu_info.get('card')
        for tag in self.tags:
            if tag not in supported_tags or (card in infer_devices and tag == 'mindspore'):
                # infer devices do not support mindspore anymore.
                not_support_components.append(tag)
        if not_support_components:
            self.record_error(SUPPORT_MSG.format(','.join(not_support_components), self.os_and_arch))

    @check_event
    def check_sys_pkg(self):
        need_print_sys_pkg_warning = False
        try:
            if not self.module.get_bin_path("yum"):
                return
            output, messages = run_command(self.module, "yum history")
            self.module.log(" ".join(messages))
            self.module.log(output)
            for line in output.splitlines():
                # e.g.:
                # Loaded plugins: fastestmirror
                # ID     | Command line             | Date and time    | Action(s)      | Altered
                # -------------------------------------------------------------------------------
                #     22 | install -y screen        | 2024-03-01 09:03 | Install        |    1
                words = line.split()
                if len(words) > 1 and words[0].isdigit() and words[0] != '1':
                    need_print_sys_pkg_warning = True
                    break
        except Exception as e:
            self.module.log(str(e))
            need_print_sys_pkg_warning = True
        if need_print_sys_pkg_warning:
            self.record_error("ascend-deployer is designed for initial system installation. After the "
                              "initial installation, there may be changes to the system packages on "
                              "this system. In this case, ascend-deployer may not be able to handle the"
                              " system packages correctly. If you encounter errors in this scenario, "
                              "please consider not using the auto nor sys_pkg parameters by ascend-deployer."
                              " Instead, rely on the instructions in the NPU and CANN documents to "
                              "manually install the system packages.")


if __name__ == '__main__':
    CompatibilityCheck().run()
