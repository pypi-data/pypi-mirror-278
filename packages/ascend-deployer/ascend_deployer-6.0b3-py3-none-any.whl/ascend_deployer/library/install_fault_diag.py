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
import os
import re
import shutil

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import common_info, common_utils, venv_installer
from ansible.module_utils.common_utils import result_handler


class FaultDiagInstaller(object):

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=dict(
                resources_dir=dict(type="str", required=True),
                ansible_run_tags=dict(type="list", required=True),
                python_version=dict(type="str", required=True),
            )
        )
        self.resources_dir = os.path.expanduser(self.module.params["resources_dir"])
        self.arch = common_info.ARCH
        self.local_path = common_info.get_local_path(os.getuid(), os.path.expanduser("~"))
        self.ascend_install_path = os.path.join(self.local_path, "Ascend")
        self.dist_tmp_dir = os.path.join(self.ascend_install_path, "dist_tmp_dir")
        self.ansible_run_tags = self.module.params.get("ansible_run_tags", [])
        self.python_version = self.module.params["python_version"]
        self.python_path = os.path.join(self.local_path, self.python_version)
        self.venv_dir = os.path.join(self.ascend_install_path, "faultdiag")
        self.pylibs_dir = os.path.join(self.resources_dir, "pylibs")
        self.messages = []

    def _module_failed(self):
        return self.module.fail_json(msg="\n".join(self.messages), rc=1, changed=False)

    def _module_success(self):
        return self.module.exit_json(msg="\n".join(self.messages), rc=0, changed=True)

    @result_handler(failed_msg="Please install python by ascend-deployer.")
    def _check_python(self):
        return os.path.exists(self.python_path), []

    def _add_python_env(self):
        os.environ["PATH"] = "{}/bin:".format(self.python_path) + os.environ["PATH"]
        os.environ["LD_LIBRARY_PATH"] = "{}/lib".format(self.python_path)

    def _find_fd_pkg(self):
        pattern = "*faultdiag*{}.whl".format(self.arch)
        pkgs, msgs = common_utils.find_files(os.path.join(self.resources_dir, "FaultDiag"), pattern)
        self.messages.extend(msgs)
        if not pkgs:
            if "auto" in self.ansible_run_tags:
                self.module.exit_json(std_out="[ASCEND]can not find faultdiag package, faultdiag install skipped", rc=0,
                                      changed=False)
            else:
                self.messages.append("[ASCEND]can not find faultdiag package.")
                self._module_failed()
        return pkgs[0]

    def _generate_installer(self, pkg):
        installer = venv_installer.VenvInstaller(module=self.module, venv_dir=self.venv_dir,
                                                 pkg_path=pkg,
                                                 pylibs_dir=self.pylibs_dir,
                                                 python_dir=self.python_path, pkg_cmd="ascend-fd")
        return installer

    @result_handler(failed_msg="Failed to install ascend-fd.")
    def _install_fd(self, installer):
        return installer.run()

    @result_handler(failed_msg="Failed to install pyinstaller.")
    def _install_pyinstaller(self, installer):
        return installer.install_other_pkg("pyinstaller")

    @result_handler(failed_msg="Failed to show ascend-faultdiag info.")
    def _show_ascend_fd_info(self, venv_pip_path):
        return common_utils.run_command(self.module, "{} show ascend-faultdiag".format(venv_pip_path))

    @result_handler(failed_msg="Failed to show ascend-faultdiag info.")
    def _find_fd_site_package_dir(self, venv_pip_path):
        res = self._show_ascend_fd_info(venv_pip_path)
        match = re.search(r"Location: (.+)", res)
        if match:
            return match.group(1), []
        return "", []

    @result_handler(failed_msg="Failed to create binary ascend-fd.")
    def _create_binary_file(self):
        venv_bin_dir = os.path.join(self.venv_dir, "bin")
        pyinstall_path = os.path.join(venv_bin_dir, "pyinstaller")
        ascend_fd_path = os.path.join(venv_bin_dir, "ascend-fd")
        venv_pip_path = os.path.join(venv_bin_dir, "pip3")
        fd_install_dir = self._find_fd_site_package_dir(venv_pip_path)
        if not os.path.exists(self.dist_tmp_dir):
            os.makedirs(self.dist_tmp_dir)
        cmd = """
        {} --onefile {} \
        --hidden-import=ascend_fd \
        --hidden-import=pandas \
        --hidden-import=numpy \
        --hidden-import=sklearn \
        --hidden-import=ply \
        --hidden-import=prettytable \
        --add-data "{}/ascend_fd:ascend_fd" \
        --distpath={} \
        --name="ascend-fd"
        """.format(pyinstall_path, ascend_fd_path, fd_install_dir, self.dist_tmp_dir)
        return common_utils.run_command(self.module, cmd)

    def _copy_binary_to_usr_local_bin(self):
        binary_path = os.path.join(self.dist_tmp_dir, "ascend-fd")
        target_path = os.path.realpath("/usr/local/bin/ascend-fd")
        shutil.copy(binary_path, target_path)
        # 授予所有用户执行权限
        os.chmod(target_path, 0o755)

    @result_handler(failed_msg="Install ascend-fd failed.")
    def _check_fd_existed(self):
        return common_utils.run_command(self.module, "ascend-fd version")

    def _clear(self):
        shutil.rmtree(self.dist_tmp_dir)
        shutil.rmtree(self.venv_dir)

    def run(self):
        try:
            pkg = self._find_fd_pkg()
            self._check_python()
            self._add_python_env()
            installer = self._generate_installer(pkg)
            self._install_fd(installer)
            self._install_pyinstaller(installer)
            self._create_binary_file()
            self._copy_binary_to_usr_local_bin()
            self._check_fd_existed()
            self._clear()
        except Exception as e:
            self.messages.append(str(e))
            self._module_failed()
        self._module_success()


def main():
    FaultDiagInstaller().run()


if __name__ == "__main__":
    main()
