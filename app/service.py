import logging
import subprocess
from typing import List

logger = logging.getLogger(__name__)


class VPNMgmtService(object):
    __version__ = 1

    _ansible_service = None

    def __init__(self, ansible_service: AnsibleService):
        self._ansible_service = ansible_service

    '''
        generation user certificate on PKI infrastructure server and register it on every server in server_uuid_list
    '''
    def generate_and_register_user_cert(self, server_uuid_list: List[str]) -> str:
        pass

    def withdraw_user_cert(self):
        pass


class AnsibleService(object):
    __version__ = 1

    _root_path = None
    _inventory_file = None
    _pb_path = None
    _cmd_wo_args = None

    def __init__(self, ansible_path, ansible_inventory_file, ansible_playbook_path):
        self._root_path = ansible_path
        logger.info("Ansible Root Path: " + self._root_path)

        self._inventory_file = ansible_inventory_file
        logger.info("Ansible inventory file: " + self._inventory_file)

        self._pb_path = ansible_playbook_path
        logger.info("Ansible Playbooks Path: " + self._pb_path)

        self._cmd_wo_args = "ansible-playbook " + self._root_path + "/" + self._pb_path + "/{pb_name}" + \
                            " -i " + self._root_path + "/" + self._inventory_file + " -l " + "{inventory_group} -f 1"
        logger.info("Base ansible shell command: " + self._cmd_wo_args)

    # args.append("key=value")
    def exec_playbook(self, ansible_playbook_name: str, inventory_group: str, args: list) -> int:
        logger.debug("PB name: " + ansible_playbook_name)
        logger.debug("inventory_group: " + inventory_group)
        logger.debug("Args: " + str(args))

        cmd = self._cmd_wo_args
        logger.debug(cmd)
        cmd = cmd.format(pb_name=ansible_playbook_name + ".yml", inventory_group=inventory_group)
        logger.debug(cmd)

        for arg in args:
            cmd += " -e " + arg

        logger.debug(cmd)

        logger.debug("Final cmd: " + cmd)

        logger.info("Execute ansible playbook, command: " + cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, err) = p.communicate()
        p_status = p.wait()
        if output is not None:
            logger.error("Execute ansible output: " + str(output))
        if err is not None:
            logger.error("Execute ansible error: " + str(err))
        if p_status is not None:
            logger.info("Exec return code: " + str(p_status))
            return p_status
        return 100
