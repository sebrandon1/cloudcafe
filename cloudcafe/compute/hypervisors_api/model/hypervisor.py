"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import xml.etree.ElementTree as ET

from cafe.engine.models.base import AutoMarshallingModel, AutoMarshallingListModel
from cloudcafe.compute.common.equality_tools import EqualityTools
from cloudcafe.compute.servers_api.models.servers import Server


class Service(AutoMarshallingModel):

    def __init__(self, host=None, id_=None):
        super(Service, self).__init__()
        self.host = host
        self.id_ = id_

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return Service(host=json_dict.get('host'),
                       id_=json_dict.get('id'))


class Hypervisor(AutoMarshallingModel):

    def __init__(self, id_=None, hypervisor_hostname=None,
                 servers=None, cpu_info=None, free_disk_gb=None,
                 hypervisor_version=None, disk_available_least=None,
                 local_gb=None, free_ram_mb=None, vcpus_used=None,
                 hypervisor_type=None, local_gb_used=None,
                 memory_mb_used=None, memory_mb=None,
                 current_workload=None, vcpus=None,
                 running_vms=None, service=None):
        super(Hypervisor, self).__init__()
        self.id_ = id_
        self.hypervisor_hostname = hypervisor_hostname
        self.servers = servers
        self.cpu_info = cpu_info
        self.free_disk_gb = free_disk_gb
        self.hypervisor_version = hypervisor_version
        self.disk_available_least = disk_available_least
        self.local_gb = local_gb
        self.free_ram_mb = free_ram_mb
        self.vcpus_used = vcpus_used
        self.hypervisor_type = hypervisor_type
        self.local_gb_used = local_gb_used
        self.memory_mb_used = memory_mb_used
        self.memory_mb = memory_mb
        self.current_workload = current_workload
        self.vcpus = vcpus
        self.running_vms = running_vms
        self.service = service

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Hypervisor object to compare with
        @type other: Hypervisor
        @return: True if Host objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Hypervisor object to compare with
        @type other: Hypervisor
        @return: True if Hypervisor objects are not equal, False otherwise
        @rtype: bool
        """
        return not self.__eq__(other)

    @classmethod
    def _dict_to_obj(cls, hypervisor_dict):
        args = {
            'id_': hypervisor_dict.get('id'),
            'hypervisor_hostname': hypervisor_dict.get('hypervisor_hostname'),
            'cpu_info': hypervisor_dict.get('cpu_info'),
            'free_disk_gb': hypervisor_dict.get('free_disk_gb'),
            'hypervisor_version': hypervisor_dict.get('hypervisor_version'),
            'disk_available_least': hypervisor_dict.get(
                'disk_available_least'),
            'local_gb': hypervisor_dict.get('local_gb'),
            'free_ram_mb': hypervisor_dict.get('free_ram_mb'),
            'vcpus_used': hypervisor_dict.get('vcpus_used'),
            'hypervisor_type': hypervisor_dict.get('hypervisor_type'),
            'local_gb_used': hypervisor_dict.get('local_gb_used'),
            'memory_mb_used': hypervisor_dict.get('memory_mb_used'),
            'memory_mb': hypervisor_dict.get('memory_mb'),
            'current_workload': hypervisor_dict.get('current_workload'),
            'vcpus': hypervisor_dict.get('vcpus'),
            'running_vms': hypervisor_dict.get('running_vms'),
            'service': Service._dict_to_obj(hypervisor_dict.get('service'))
        }

        return Hypervisor(**args)

    @classmethod
    def _int_to_version_str(cls, version_int):
        """
        @param version_int: The version in munge form of integer
            ex: 6000000
        @type version_int: Integer
        @return: dot seperated version string
            ex: '6.0.0'
        """
        if isinstance(version_int, str):
            version_int = int(version_int)
        major = version_int // 1000000
        minor = (version_int - major * 1000000) // 1000
        patch = (version_int - major * 1000000 - minor * 1000)
        return '{0}.{1}.{2}'.format(major, minor, patch)


class Hypervisors(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a Hypervisor
        based on the json serialized_str
        passed in.
        @param serialized_str: JSON serialized string
        @type serialized_str: String
        @return: List of Hypervisor
        @rtype: List
        """
        json_dict = json.loads(serialized_str)

        hypervisors = Hypervisors()
        for hypervisor_dict in json_dict.get('hypervisors'):
            hypervisors.append(Hypervisor._dict_to_obj(hypervisor_dict))

        ret = hypervisors
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Returns an instance of a Hypervisor
        based on the xml serialized_str
        passed in.
        @param serialized_str: XML serialized string
        @type serialized_str: String
        @return: List of Hypervisors
        @rtype: List
        """
        element = ET.fromstring(serialized_str)
        hypervisors = Hypervisors()
        for hypervisor_ele in element.findall('hypervisor'):
            hypervisor_dict = hypervisor_ele.attrib
            hypervisor_dict['service'] = hypervisor_ele.find('service').attrib
            hyp_obj = Hypervisor._dict_to_obj(hypervisor_dict)
            hypervisors.append(hyp_obj)

        return hypervisors


class HypervisorMin(AutoMarshallingModel):

    def __init__(self, id=None, hypervisor_hostname=None,
                 servers=None):
        super(HypervisorMin, self).__init__()
        self.id = int(id)
        self.hypervisor_hostname = hypervisor_hostname
        self.servers = servers

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: HypervisorMin object to compare with
        @type other: HypervisorMin
        @return: True if HypervisorMin objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: HypervisorMin object to compare with
        @type other: HypervisorMin
        @return: True if HypervisorMin objects are not equal, False otherwise
        @rtype: bool
        """
        return not self.__eq__(other)


class HypervisorsMin(AutoMarshallingListModel):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @summary: Returns a list of a HypervisorMin
        based on the json serialized_str
        passed in.
        @param serialized_str: JSON serialized string
        @type serialized_str: String
        @return: List of HypervisorMin
        @rtype: List
        """
        json_dict = json.loads(serialized_str)
        hypervisors = HypervisorsMin()
        for hypervisor_dict in json_dict['hypervisors']:
            id = hypervisor_dict['id']
            hypervisor_hostname = hypervisor_dict['hypervisor_hostname']
            if 'servers' in hypervisor_dict.keys():
                servers = []
                for server_dict in hypervisor_dict['servers']:
                    servers.append(Server._dict_to_obj(server_dict))
                hypervisors.append(HypervisorMin(id, hypervisor_hostname,
                                                 servers))
            else:
                servers = None
                hypervisor_dict.update({"servers": servers})
                hypervisors.append(HypervisorMin(id, hypervisor_hostname,
                                                 servers))
        return hypervisors

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        @summary: Returns a list of a HypervisorMin
        based on the xml serialized_str
        passed in.
        @param serialized_str: XML serialized string
        @type serialized_str: String
        @return: List of HypervisorMin
        @rtype: List
        """
        element = ET.fromstring(serialized_str)
        hypervisors = HypervisorsMin()
        for hypervisor in element.findall('hypervisor'):
            hypervisor_dict = hypervisor.attrib
            id = hypervisor_dict['id']
            hypervisor_hostname = hypervisor_dict['hypervisor_hostname']
            if "servers" in [elem.tag for elem in hypervisor.iter()]:
                servers = []
                for server in hypervisor.iter('server'):
                    servers.append(Server._dict_to_obj(server.attrib))
                hypervisors.append(HypervisorMin(id, hypervisor_hostname,
                                                 servers))
            else:
                servers = None
                hypervisor.attrib.update({"servers": servers})
                hypervisors.append(HypervisorMin(id, hypervisor_hostname,
                                                 servers))
        return hypervisors

