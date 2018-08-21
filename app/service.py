import logging
import subprocess
from typing import List

from app.ansible_playbooks import *


class VPNMgmtService(object):
    __version__ = 1

    logger = logging.getLogger(__name__)

    _ansible_service = None

    def __init__(self, ansible_service: AnsibleService):
        self._ansible_service = ansible_service

    '''
        generate user certificate on PKI infrastructure server and register it on every server
    '''

    def create_vpn_user(self, user_email: str):
        self.logger.debug(f"create_vpn_user method with parameters user_email: {user_email}")
        self.logger.debug("create ansible playbook to create VPN user")
        apcvu = AnsiblePlaybookCreateVPNUser()
        self.logger.debug("add user email")
        apcvu.add_user(user_email=user_email)
        self.logger.debug("call ansible service")
        code = self._ansible_service.exec_playbook(ansible_playbook=apcvu)
        self.logger.debug("check code")
        if code == 0:
            self.logger.debug("code OK")
            return True
        else:
            self.logger.debug("failed")
            return False

    '''
        withdaw user certificate on PKI infrastructure server and withdraw in on every server
    '''

    def withdraw_vpn_user(self, user_email: str):
        self.logger.debug(f"withdraw_vpn_user method with parameters user_email: {user_email}")
        self.logger.debug("create ansible playbook to withdraw VPN user")
        apcvu = AnsiblePlaybookWithdrawVPNUser()
        self.logger.debug("add user email")
        apcvu.add_user(user_email=user_email)
        self.logger.debug("call ansible service")
        code = self._ansible_service.exec_playbook(ansible_playbook=apcvu, is_async=False)
        self.logger.debug("check code")
        if code == 0:
            self.logger.debug("code OK")
            self.logger.debug("create ansible playbook to get updated CRL from PKI server")
            apgc = AnsiblePlaybookGetCRL()
            self.logger.debug("call ansible service")
            code = self._ansible_service.exec_playbook(ansible_playbook=apgc, is_async=False)
            self.logger.debug("check code")
            if code == 0:
                self.logger.debug("code OK")
                self.logger.debug("create ansible playbook to update CRL on every VPN server")
                appc = AnsiblePlaybookPutCRL()
                self.logger.debug("call ansible service")
                self._ansible_service.exec_playbook(ansible_playbook=appc, is_async=True)
            else:
                self.logger.error("failed to update CRL on every VPN server")
        else:
            self.logger.error("failed to get updated CRL from PKI server")

    '''
        retrieve connections information from every VPN server (call scripts)
    '''

    def update_server_connections(self, server_ip_list: List[str]) -> bool:
        self.logger.debug(f"create ansible playbook to update server connections depends on list: {server_ip_list}")
        apusc = AnsiblePlaybookUpdateServerConnections(ip_addresses_list=server_ip_list)
        self.logger.debug("call ansible service")
        code = self._ansible_service.exec_playbook(ansible_playbook=apusc)
        if code == 0:
            return True
        else:
            return False


class AnsibleService(object):
    __version__ = 1

    _cmd_wo_args = None

    logger = logging.getLogger(__name__)

    def __init__(self, ansible_path, ansible_inventory_file, ansible_playbook_path):
        self.logger.debug("ansible Root Path: " + ansible_path)
        self.logger.debug("ansible inventory file: " + ansible_inventory_file)
        self.logger.debug("ansible Playbooks Path: " + ansible_playbook_path)

        self.logger.debug("create ansible command with out arguments")
        self._cmd_wo_args = f"ansible-playbook {ansible_path}/{ansible_playbook_path}/" + "{pb_name}" + f"-i {ansible_path}/{ansible_inventory_file} -l" + "{inventory_group} -f 1"

        self.logger.info("base ansible shell command: " + self._cmd_wo_args)

    def exec_playbook(self, ansible_playbook: AnsiblePlaybook, is_async: bool = False) -> int:
        name = ansible_playbook.name
        inventory = ansible_playbook.inventory_group_name
        ext_args = ansible_playbook.get_extended_args()
        self.logger.debug(f"playbook Name: {name}")
        self.logger.debug(f"inventory Group: {inventory}")
        self.logger.debug(f"args: {ext_args}")

        cmd = self._cmd_wo_args
        self.logger.debug(cmd)
        cmd = cmd.format(pb_name=ansible_playbook.name, inventory_group=ansible_playbook.inventory_group_name)
        self.logger.debug(cmd)
        cmd += " -e " + ansible_playbook.get_extended_args()
        self.logger.debug(f"final cmd: {cmd}")

        self.logger.info("execute ansible shell command")
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, err) = p.communicate()

        if not is_async:
            p_status = p.wait()
            if output is not None:
                self.logger.error(f"execute ansible playbook {name} output: {output}")
            if err is not None:
                self.logger.error(f"execute ansible playbook {name} error: {err}")
            if p_status is not None:
                try:
                    p_status = int(p_status)
                except KeyError:
                    self.logger.info(f"exec ansible playbook {name} return code: {p_status}")
                return p_status
            return 9090909090
        else:
            return 0
