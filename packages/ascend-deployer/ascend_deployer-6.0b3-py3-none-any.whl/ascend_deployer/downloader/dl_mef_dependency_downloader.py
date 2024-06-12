#!/usr/bin/env python3
# coding: utf-8
# Copyright 2020 Huawei Technologies Co., Ltd
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
from functools import reduce
from typing import List

from . import logger_config
from .download_data import DownloadData
from .parallel_file_downloader import DownloadFileInfo
from .software_mgr import PkgInfo

LOG = logger_config.LOG


class DlMefDependencyDownloader:
    DELETE = "Delete"
    UPDATE = "Update"

    def __init__(self, download_data: DownloadData):
        self._download_data = download_data
        self._software_mgr = download_data.software_mgr
        self._software_list = download_data.selected_soft_list
        self._os_list = download_data.selected_os_list

    @staticmethod
    def _get_pkg_info_from_json(resources_json) -> List[PkgInfo]:
        with open(resources_json, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return [PkgInfo(**item) for item in data]

    def _update_or_del_pkg(self, pkg_list: List[PkgInfo], pkg: PkgInfo) -> List[PkgInfo]:
        """
        Delete or update COMMON pkg based on COMMON_UPDATE json configuration.
        :param pkg_list: the list of origin PkgInfo from COMMON
        :param pkg: PkgInfo from COMMON_UPDATE
        :eg. {
             "filename": "aarch64.tar.gz",
             "dest": "resources/docker/OpenEuler_20.03_LTS",
             "remark": "Update"
           }
        :return: PkgInfo list
        """
        if pkg.remark == self.DELETE:
            return [p for p in pkg_list if not (p.filename == pkg.filename and p.dest == pkg.dest)]
        elif pkg.remark == self.UPDATE:
            return [p for p in pkg_list if not (p.filename == pkg.filename and p.dest == pkg.dest)] + [pkg]
        else:
            return pkg_list + [pkg]

    def _collect_common_resources(self, os_item: str, version: str) -> List[PkgInfo]:
        pkg_list: List[PkgInfo] = []
        common_os_resources = os.path.join(self._download_data.base_dir,
                                           f'downloader/dependency/COMMON/{os_item}.json')
        if os.path.exists(common_os_resources):
            pkg_list.extend(self._get_pkg_info_from_json(common_os_resources))
        resources_json = os.path.join(self._download_data.base_dir,
                                      f'downloader/dependency/{version}/COMMON_UPDATE/{os_item}.json')
        if not os.path.getsize(resources_json):
            return pkg_list
        resources = self._get_pkg_info_from_json(resources_json)
        return reduce(self._update_or_del_pkg, resources, pkg_list)

    def _has_dl_or_mef(self):
        for soft in self._download_data.selected_soft_list:
            if "DL" in soft or "MEF" in soft:
                return True
        return False

    def collect_dl_mef_dependency(self):
        result = []
        if not self._has_dl_or_mef():
            return result
        download_dl = any("DL" in pkg_name for pkg_name in self._software_list)
        download_mef = any("MEF" in pkg_name for pkg_name in self._software_list)
        download_aarch64 = any("aarch64" in os_item for os_item in self._os_list)
        download_x86_64 = any("x86_64" in os_item for os_item in self._os_list)
        software_with_version_list = [self._software_mgr.get_name_version(item, std_out=False) for item in
                                      self._software_list]
        dl_version = mef_version = ""
        for pkg_name in software_with_version_list:
            if "DL" in pkg_name and "_" in pkg_name:
                dl_version = pkg_name.split("_")[1]
            if "MEF" in pkg_name and "_" in pkg_name:
                mef_version = pkg_name.split("_")[1]
        pkg_info_list: List[PkgInfo] = []
        for os_item in self._os_list:
            if dl_version:
                pkg_info_list.extend(self._collect_common_resources(os_item, dl_version))
            if mef_version:
                pkg_info_list.extend(self._collect_common_resources(os_item, mef_version))
        for arch, is_download in (('aarch64', download_aarch64), ('x86_64', download_x86_64)):
            if not is_download:
                continue
            if download_dl:
                resources_json = os.path.join(self._download_data.base_dir,
                                              f'downloader/dependency/{dl_version}/DL/{arch}/resource.json')
                pkg_info_list.extend(self._get_pkg_info_from_json(resources_json))
            if download_mef:
                resources_json = os.path.join(self._download_data.base_dir,
                                              f'downloader/dependency/{mef_version}/MEF/{arch}/resource.json')
                pkg_info_list.extend(self._get_pkg_info_from_json(resources_json))

        for pkg in pkg_info_list:
            dest_file_path = os.path.join(self._download_data.base_dir, pkg.dest, pkg.filename)
            result.append(DownloadFileInfo(filename=pkg.filename, url=pkg.url, sha256=pkg.sha256,
                                           dst_file_path=dest_file_path))
        return result
