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
import os.path
import subprocess

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import common_info

OK = "OK"
ERROR = "ERROR"

messages = []


def run_command(command, custom_env=None):
    try:
        env = os.environ.copy()
        if custom_env:
            env.update(custom_env)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env, executable="/bin/bash")
        stdout, stderr = process.communicate()
        if not isinstance(stdout, str):
            stdout = str(stdout, encoding='utf-8')
        if not isinstance(stderr, str):
            stderr = str(stderr, encoding='utf-8')
        return process.returncode == 0, stdout + stderr
    except Exception as e:
        return False, str(e)


def get_npu_ids():
    ok, outputs = run_command("npu-smi info -m")
    if not ok:
        messages.append(outputs)
        return []
    npu_ids = []
    for line in outputs.splitlines():
        split_line = line.split()
        if not split_line:
            continue
        if '310' in split_line[-1] or '910' in split_line[-1] or '710' in split_line[-1]:
            npu_ids.append(split_line[0].strip())
    return npu_ids


def test_driver(cus_npu_info):
    if not os.path.exists("/usr/local/Ascend/driver/version.info"):
        return "not installed"
    ok, output = run_command(
        "npu-smi info",
        {"LD_LIBRARY_PATH": "/usr/local/Ascend/driver/lib64:/usr/local/Ascend/driver/lib64/common:"
                            "/usr/local/Ascend/driver/lib64/driver:"})
    if not ok:
        return ERROR

    if cus_npu_info == "300i-pro":
        checking_words = "300i"
    elif cus_npu_info == "300v-pro":
        checking_words = "300v"
    else:
        return OK

    for npu_id in get_npu_ids():
        ok, outputs = run_command("npu-smi info -t product -i {}".format(npu_id))
        if not ok:
            return ERROR
        if checking_words not in outputs.lower():
            messages.append("you are installing driver of {} on hardware of {}".format(
                cus_npu_info, "300i-pro" if cus_npu_info == "300v-pro" else "300v-pro"))
            return ERROR
    return OK


def test_firmware():
    if not os.path.exists("/usr/local/Ascend/firmware/version.info"):
        return "not installed"

    if not os.path.exists("/usr/local/Ascend/driver/tools/upgrade-tool"):
        return "not installed"
    ok, output = run_command(
        "/usr/local/Ascend/driver/tools/upgrade-tool --device_index -1 --system_version",
        {"LD_LIBRARY_PATH": "/usr/local/Ascend/driver/lib64:/usr/local/Ascend/driver/lib64/common:"
                            "/usr/local/Ascend/driver/lib64/driver:"})
    if ok and "succeed" in output:
        return OK
    return ERROR


def test_toolbox():
    ascend_install_path = common_info.get_ascend_install_path(os.getuid(), os.path.expanduser("~"))
    bin_path = os.path.join(ascend_install_path, "toolbox/latest/Ascend-DMI/bin/ascend-dmi")
    if not os.path.exists(bin_path):
        return "not installed"
    commands = [". {}/toolbox/set_env.sh".format(ascend_install_path), ]
    if os.path.exists("{}/nnae/set_env.sh".format(ascend_install_path)):
        commands.append(". {}/nnae/set_env.sh".format(ascend_install_path))
    elif os.path.exists("{}/nnrt/set_env.sh".format(ascend_install_path)):
        commands.append(". {}/nnrt/set_env.sh".format(ascend_install_path))
    elif os.path.exists("{}/ascend-toolkit/set_env.sh".format(ascend_install_path)):
        commands.append(". {}/ascend-toolkit/set_env.sh".format(ascend_install_path))
    else:
        return ERROR
    commands.append("echo y | ascend-dmi -f -et 10")
    ok, output = run_command(" && ".join(commands))
    if ok:
        return OK
    return ERROR


def test_python_package(package_name, python_version):
    local_path = common_info.get_local_path(os.getuid(), os.path.expanduser("~"))
    ascend_install_path = common_info.get_ascend_install_path(os.getuid(), os.path.expanduser("~"))
    paths = os.environ.get("PATH", "")
    paths = "{}/{}/bin:".format(local_path, python_version) + paths
    ld_paths = "{}/{}/lib:".format(local_path, python_version)
    ok, output = run_command("python3 -m pip list | grep {}".format(package_name), custom_env={
        "PATH": paths, "LD_LIBRARY_PATH": ld_paths
    })
    if not ok:
        return "not installed"
    paths = "{}/ascend-toolkit/latest/atc/ccec_compiler/bin/:".format(ascend_install_path) + paths
    ld_paths = ("{}/gcc7.3.0/lib64;{}/{}/lib/{}/site-packages/{}/lib:{}/add-ons/:".
                format(local_path, local_path, python_version, python_version[:9],
                       package_name, ascend_install_path) + ld_paths)
    commands = []
    if os.path.exists("{}/nnrt/set_env.sh".format(ascend_install_path)):
        commands.append(". {}/nnrt/set_env.sh".format(ascend_install_path))
    if os.path.exists("{}/nnae/set_env.sh".format(ascend_install_path)):
        commands.append(". {}/nnae/set_env.sh".format(ascend_install_path))
    if os.path.exists("{}/ascend-toolkit/set_env.sh".format(ascend_install_path)):
        commands.append(". {}/ascend-toolkit/set_env.sh".format(ascend_install_path))
    commands.append('python3 -c "import {} as framework; print(framework.__version__);"'.format(package_name))
    if package_name == "torch":
        commands.append('python3 -c "import torch; import torch_npu; a = torch.randn(3, 4).npu(); print(a + a)"')
    ok, output = run_command(" && ".join(commands), custom_env={
        "PATH": paths, "LD_LIBRARY_PATH": ld_paths
    })
    if not ok:
        return ERROR
    return OK


def test_tensorflow(python_version):
    local_path = common_info.get_local_path(os.getuid(), os.path.expanduser("~"))
    ascend_install_path = common_info.get_ascend_install_path(os.getuid(), os.path.expanduser("~"))
    paths = os.environ.get("PATH", "")
    paths = "{}/{}/bin:".format(local_path, python_version) + paths
    ld_paths = "{}/{}/lib:{}/add-ons/:".format(local_path, python_version, ascend_install_path)
    ok, output = run_command('python3 -m pip list | grep -E "tensorflow |tensorflow-cpu"', custom_env={
        "PATH": paths, "LD_LIBRARY_PATH": ld_paths
    })
    if not ok:
        return "not installed"
    if "1.15.0" in output:
        version = "1.15.0"
    elif "2.6.5" in output:
        version = "2.6.5"
    else:
        return ERROR

    commands = [". {}/tfplugin/set_env.sh".format(ascend_install_path)]
    if os.path.exists("{}/nnae/set_env.sh".format(ascend_install_path)):
        commands.append(". {}/nnae/set_env.sh".format(ascend_install_path))
    if os.path.exists("{}/ascend-toolkit/set_env.sh".format(ascend_install_path)):
        commands.append(". {}/ascend-toolkit/set_env.sh".format(ascend_install_path))
    if version == "1.15.0":
        commands.append('python3 -c "import npu_bridge.estimator; import npu_bridge.hccl;'
                        ' from tensorflow.core.protobuf import rewriter_config_pb2"')
    if version == "2.6.5":
        commands.append('python3 -c "import npu_device; from tensorflow.core.protobuf import rewriter_config_pb2"')

    ok, output = run_command(" && ".join(commands), custom_env={
        "PATH": paths, "LD_LIBRARY_PATH": ld_paths
    })
    messages.append(output)
    if not ok:
        return ERROR

    return OK


def test_tfplugin():
    ascend_install_path = common_info.get_ascend_install_path(os.getuid(), os.path.expanduser("~"))
    tfplugin_path = os.path.join(ascend_install_path, "tfplugin/latest")
    if not os.path.exists(tfplugin_path):
        return "not installed"
    return OK


def test_cann_packages(package_name, python_version):
    ascend_install_path = common_info.get_ascend_install_path(os.getuid(), os.path.expanduser("~"))
    cann_path = os.path.join(ascend_install_path, "{}/latest".format(package_name))
    if not os.path.exists(cann_path):
        return "not installed"
    commands = []
    if os.path.exists("{}/{}/set_env.sh".format(ascend_install_path, package_name)):
        commands.append(". {}/{}/set_env.sh".format(ascend_install_path, package_name))
    else:
        return ERROR
    commands.append('python3 -c "import acl"')
    paths = os.environ.get("PATH", "")
    local_path = common_info.get_local_path(os.getuid(), os.path.expanduser("~"))
    paths = "{}/{}/bin:".format(local_path, python_version) + paths
    ld_paths = "{}/{}/lib:".format(local_path, python_version)
    ok, output = run_command(" && ".join(commands), custom_env={
        "PATH": paths, "LD_LIBRARY_PATH": ld_paths
    })
    if not ok:
        return ERROR
    return OK


def main():
    module = AnsibleModule(argument_spec=dict(
            ansible_run_tags=dict(type="list", required=True),
            cus_npu_info=dict(type="str", required=True),
            python_version=dict(type="str", required=True),
        )
    )
    ansible_run_tags = set(module.params["ansible_run_tags"])
    cus_npu_info = module.params.get("cus_npu_info", "")
    python_version = module.params.get("python_version", "")
    if 'whole' in ansible_run_tags:
        ansible_run_tags = ["driver", "firmware", "toolbox", "mindspore",
                            "pytorch", "tensorflow", "tfplugin", "nnae",
                            "nnrt", "toolkit"]
    result = {}
    if "driver" in ansible_run_tags:
        result["driver"] = test_driver(cus_npu_info)
    if "firmware" in ansible_run_tags:
        result["firmware"] = test_firmware()
    if "toolbox" in ansible_run_tags:
        result["toolbox"] = test_toolbox()
    if "mindspore" in ansible_run_tags:
        result["mindspore"] = test_python_package("mindspore", python_version)
    if "pytorch" in ansible_run_tags:
        result["pytorch"] = test_python_package("torch", python_version)
    if "tensorflow" in ansible_run_tags:
        result["tensorflow"] = test_tensorflow(python_version)
    if "tfplugin" in ansible_run_tags:
        result["tfplugin"] = test_tfplugin()
    if "nnae" in ansible_run_tags:
        result["nnae"] = test_cann_packages("nnae", python_version)
    if "nnrt" in ansible_run_tags:
        result["nnrt"] = test_cann_packages("nnrt", python_version)
    if "toolkit" in ansible_run_tags:
        result["toolkit"] = test_cann_packages("ascend-toolkit", python_version)

    module.exit_json(changed=True, rc=0, result=result, msg="\n".join(messages))


if __name__ == "__main__":
    main()
