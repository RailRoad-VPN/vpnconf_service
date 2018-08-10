import logging
import sys
import uuid

from psycopg2._psycopg import DatabaseError

from app.exception import *

sys.path.insert(0, '../psql_library')
from storage_service import StorageService, StoredObject


class VPNServerConfigurationTemplate(object):
    __version__ = 1

    _suuid = None
    _vpn_device_platform_id = None
    _vpn_type_id = None
    _template_str = None

    def __init__(self, suuid: str = None, vpn_device_platform_id: int = None, vpn_type_id: str = None, template_str: str = None):
        self._suuid = suuid
        self._vpn_device_platform_id = vpn_device_platform_id
        self._vpn_type_id = vpn_type_id
        self._template_str = template_str

    def to_dict(self):
        return {
            'uuid': self._suuid,
            'vpn_device_platform_id': self._vpn_device_platform_id,
            'vpn_type_id': self._vpn_type_id,
            'template_str': self._template_str,
        }

    def to_api_dict(self):
        return {
            'uuid': str(self._suuid),
            'vpn_device_platform_id': self._vpn_device_platform_id,
            'vpn_type_id': self._vpn_type_id,
            'template_str': self._template_str,
        }


class VPNServerConfigurationTemplateStored(StoredObject, VPNServerConfigurationTemplate):
    __version__ = 1

    def __init__(self, storage_service: StorageService, suuid: str = None, vpn_device_platform_id: int = None,
                 vpn_type_id: str = None, template_str: str = None, limit: int = None, offset: int = None, **kwargs):
        StoredObject.__init__(self, storage_service=storage_service, limit=limit, offset=offset)
        VPNServerConfigurationTemplate.__init__(self, suuid=suuid, vpn_device_platform_id=vpn_device_platform_id,
                                                vpn_type_id=vpn_type_id, template_str=template_str)


class VPNServerConfigurationTemplateDB(VPNServerConfigurationTemplateStored):
    __version__ = 1

    _suuid_field = 'uuid'
    _vpn_device_platform_id_field = 'vpn_device_platform_id'
    _vpn_type_id_field = 'vpn_type_id'
    _template_str_field = 'template_str'

    def __init__(self, storage_service: StorageService, **kwargs):
        super().__init__(storage_service, **kwargs)

    def find(self):
        logging.info('VPNServerConfigurationTemplatesDB find method')
        select_sql = '''
                      SELECT 
                        uuid,
                        vpn_device_platform_id,
                        vpn_type_id,
                        template_str
                      FROM public.vpnserver_config_templates
                      '''
        if self._limit:
            select_sql += f"\nLIMIT {self._limit}\nOFFSET {self._offset}"
        logging.debug(f"Select SQL: {select_sql}")

        try:
            logging.debug('Call database service')
            vpnserverconfig_list_db = self._storage_service.get(sql=select_sql)
        except DatabaseError as e:
            logging.error(e)
            error_message = VPNCError.VPNSERVER_CONFIG_TEMPLATES_FIND_ERROR_DB.message
            error_code = VPNCError.VPNSERVER_CONFIG_TEMPLATES_FIND_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVER_CONFIG_TEMPLATES_FIND_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        vpnserverconfig_list = []

        for vpnserverconfig_db in vpnserverconfig_list_db:
            vpnserverconfig = self.__map_vpnserverconfigtempldb_to_vpnserverconfigtempl(vpnserverconfig_db)
            vpnserverconfig_list.append(vpnserverconfig)

        return vpnserverconfig_list

    def find_by_suuid(self):
        logging.info('VPNServerConfigurationTemplatesDB find_by_server_uuid method')
        select_sql = '''
                      SELECT 
                        uuid,
                        vpn_device_platform_id,
                        vpn_type_id,
                        template_str
                      FROM public.vpnserver_config_templates
                      WHERE uuid = ?
                      '''
        logging.debug(f"Select SQL: {select_sql}")
        params = (self._suuid,)

        try:
            logging.debug('Call database service')
            vpnserver_config_templates_list_db = self._storage_service.get(sql=select_sql, data=params)
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVER_CONFIG_TEMPLATES_FIND_BY_UUID_ERROR_DB.message
            error_code = VPNCError.VPNSERVER_CONFIG_TEMPLATES_FIND_BY_UUID_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVER_CONFIG_TEMPLATES_FIND_BY_UUID_ERROR_DB.developer_message, e.pgcode,
                                    e.pgerror)
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        if len(vpnserver_config_templates_list_db) == 1:
            vpnserver_db = vpnserver_config_templates_list_db[0]
        elif len(vpnserver_config_templates_list_db) == 0:
            error_message = VPNCError.VPNSERVER_CONFIG_TEMPLATES_FIND_BY_UUID_ERROR.message
            error_code = VPNCError.VPNSERVER_CONFIG_TEMPLATES_FIND_BY_UUID_ERROR.code
            developer_message = VPNCError.VPNSERVER_CONFIG_TEMPLATES_FIND_BY_UUID_ERROR.developer_message
            raise VPNNotFoundException(error=error_message, error_code=error_code, developer_message=developer_message)
        else:
            error_message = VPNCError.VPNSERVER_CONFIG_TEMPLATES_FIND_BY_UUID_ERROR.message
            developer_message = "%s. Find by specified uuid return more than 1 object. This is CAN NOT be! Something " \
                                "really bad with database." % VPNCError.VPNSERVER_CONFIG_TEMPLATES_FIND_BY_UUID_ERROR.developer_message
            error_code = VPNCError.VPNSERVER_CONFIG_TEMPLATES_FIND_BY_UUID_ERROR.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

        return self.__map_vpnserverconfigtempldb_to_vpnserverconfigtempl(vpnserver_db)

    def create(self):
        logging.info('VPNServerConfigurationTemplates create method')
        self._suuid = uuid.uuid4()
        logging.info('Create object VPNServerConfigurationTemplates with uuid: ' + str(self._suuid))
        insert_sql = '''
                      INSERT INTO public.vpnserver_config_templates 
                        (uuid, vpn_device_platform_id, vpn_type_id, template_str) 
                      VALUES 
                        (?, ?, ?, ?)
                     '''
        insert_params = (
            self._suuid,
            self._vpn_device_platform_id,
            self._vpn_type_id,
            self._template_str
        )
        logging.debug('Create VPNServerConfigurationTemplates SQL : %s' % insert_sql)

        try:
            logging.debug('Call database service')
            self._storage_service.create(sql=insert_sql, data=insert_params)
        except DatabaseError as e:
            self._storage_service.rollback()
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVER_CREATE_ERROR_DB.message
            error_code = VPNCError.VPNSERVER_CREATE_ERROR_DB.code
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVER_CONFIG_TEMPLATES_CREATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)

            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)
        logging.debug('VPNServerConfigurationTemplates created.')

        return self._suuid

    def update(self):
        logging.info('VPNServerConfigurationTemplates update method')

        update_sql = '''
                    UPDATE public.vpnserver_config_templates 
                    SET
                        vpn_device_platform_id = ?,
                        vpn_type_id = ?,
                        template_str = ?
                    WHERE 
                      uuid = ?
                    '''

        logging.debug('Update SQL: %s' % update_sql)

        update_params = (
            self._vpn_device_platform_id,
            self._vpn_type_id,
            self._template_str,
            self._suuid,
        )

        try:
            logging.debug("Call database service")
            self._storage_service.update(sql=update_sql, data=update_params)
            logging.debug('VPNServerConfigurationTemplates updated.')
        except DatabaseError as e:
            logging.error(e)
            try:
                e = e.args[0]
            except IndexError:
                pass
            error_message = VPNCError.VPNSERVER_CONFIG_TEMPLATES_UPDATE_ERROR_DB.message
            developer_message = "%s. DatabaseError.. " \
                                "Code: %s . %s" % (
                                    VPNCError.VPNSERVER_CONFIG_TEMPLATES_UPDATE_ERROR_DB.developer_message, e.pgcode, e.pgerror)
            error_code = VPNCError.VPNSERVER_CONFIG_TEMPLATES_UPDATE_ERROR_DB.code
            raise VPNException(error=error_message, error_code=error_code, developer_message=developer_message)

    def __map_vpnserverconfigtempldb_to_vpnserverconfigtempl(self, vpnserverconfigtempl_db):
        return VPNServerConfigurationTemplate(
            suuid=vpnserverconfigtempl_db[self._suuid_field],
            vpn_device_platform_id=vpnserverconfigtempl_db[self._vpn_device_platform_id_field],
            vpn_type_id=vpnserverconfigtempl_db[self._vpn_type_id_field],
            template_str=vpnserverconfigtempl_db[self._template_str_field],
        )
