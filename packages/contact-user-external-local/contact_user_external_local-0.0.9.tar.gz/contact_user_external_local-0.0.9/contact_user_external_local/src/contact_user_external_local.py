import re
from database_mysql_local.generic_mapping import GenericMapping
from logger_local.MetaLogger import MetaLogger
from user_external_local.user_externals_local import UserExternalsLocal
from internet_domain_local.internet_domain_local import DomainLocal

from .contact_user_external_local_constants import CONTACT_USER_EXTERNAL_PYTHON_PACKAGE_CODE_LOGGER_OBJECT

DEFAULT_SCHEMA_NAME = 'contact_user_external'
DEFAULT_ENTITY_NAME1 = 'contact'
DEFAULT_ENTITY_NAME2 = 'user_external'
DEFAULT_ID_COLUMN_NAME = 'contact_user_external_id'
DEFAULT_TABLE_NAME = 'contact_user_external_table'
DEFAULT_VIEW_TABLE_NAME = 'contact_user_external_view'


class ContactUserExternalLocal(GenericMapping, metaclass=MetaLogger,
                               object=CONTACT_USER_EXTERNAL_PYTHON_PACKAGE_CODE_LOGGER_OBJECT):
    def __init__(self, system_id: int, is_test_data: bool = False):

        GenericMapping.__init__(self, default_schema_name=DEFAULT_SCHEMA_NAME,
                                default_entity_name1=DEFAULT_ENTITY_NAME1,
                                default_entity_name2=DEFAULT_ENTITY_NAME2,
                                default_column_name=DEFAULT_ID_COLUMN_NAME,
                                default_table_name=DEFAULT_TABLE_NAME,
                                default_view_table_name=DEFAULT_VIEW_TABLE_NAME,
                                is_test_data=is_test_data)
        self.user_externals = UserExternalsLocal(is_test_data=is_test_data)
        self.internet_domain = DomainLocal(is_test_data=is_test_data)
        self.system_id = system_id

    def insert_contact_and_link_to_existing_or_new_user_external(
            # TODO change dict -> dict[Contact] (not used)
            # TODO change str -> EmailAddress
            self, *, contact_dict: dict, contact_email_address: str,
            contact_id: int, system_id: int = None, user_external_dict: dict = None) -> int or None:
        """
        Insert contact and link to existing or new user_external
        :param contact_dict: contact dict
        :param contact_id: contact id
        :param contact_email_address: contact email address
        :param system_id: system id
        :param user_external_dict: user_external dict
        :return: contact_user-external_id
        """
        website1 = contact_dict.get("website1")
        website2 = contact_dict.get("website2")
        website3 = contact_dict.get("website3")
        url = contact_dict.get("url")
        contact_user_external_id = None
        system_id = system_id or self.system_id
        access_token = expiry = refresh_token = None
        if user_external_dict:
            # username = user_external_dict.get("username", contact_email_address)
            profile_id = user_external_dict.get("profile_id")
            system_id = user_external_dict.get("system_id", system_id)
            access_token = user_external_dict.get("access_token")
            expiry = user_external_dict.get("expiry")
            refresh_token = user_external_dict.get("refresh_token")
            # oauth_token = user_external_dict.get("oauth_token")
            # oauth_token_secret = user_external_dict.get("oauth_token_secret")
            # oauth_callback_confirmed = user_external_dict.get("oauth_callback_confirmed")
            # environment_id_old = user_external_dict.get("environment_id_old")
        else:
            profiles_ids = contact_dict.get("profiles_ids")
            # TODO: Shall we add/link to all profiles ids and not just to the first one?
            profile_id = profiles_ids[0] if profiles_ids else None

        user_external_id = self.user_externals.select_one_value_by_where(
            select_clause_value="user_external_id", where="username=%s AND system_id=%s",
            # TODO allow to send to order_by also order_by_array with two items "start_timestamp" and DESC enum- This way we can move to other non SQL databases
            params=(contact_email_address, system_id), order_by="start_timestamp DESC")

        if not user_external_id:
            if not access_token:
                self.logger.warning("access_token is None")
            profiles_ids_dicts = self.__get_external_profile_id_dict_from_urls(urls=[url, website1, website2, website3])
            if profiles_ids_dicts:
                for profile_id_dict in profiles_ids_dicts:
                    for key, value in profile_id_dict.items():
                        system_id = self.get_system_id_by_external_profile_id_type(key)
                        external_profile_id = value
                        # create new user_external and add it to user_external_table
                        self.logger.info("user_external_id is None, creating new user_external")
                        # TODO: when ready, use the minsert method that returns the id
                        # profile_id is not of our system, it's external id
                        user_external_dict_for_upsert = {
                            "username": external_profile_id, "system_id": system_id,
                            "access_token": access_token, "expiry": expiry, "refresh_token": refresh_token
                        }
                        user_external_dict_for_compare = {
                            "username": external_profile_id, "system_id": system_id
                        }
                        user_external_id = self.user_externals.upsert(
                            table_name="user_external_table", view_table_name="user_external_view",
                            data_dict=user_external_dict_for_upsert, data_dict_compare=user_external_dict_for_compare)
                        # TODO: when ready, use the minsert method that returns the id
                        if not user_external_id:
                            raise Exception("upsert user_external was not successful")
                        contact_user_external_id = self.insert_mapping(
                            entity_name1=self.default_entity_name1, entity_name2=self.default_entity_name2,
                            entity_id1=contact_id, entity_id2=user_external_id,
                            ignore_duplicate=True)
        else:
            # link to existing user_external
            self.logger.info("user_external_id is not None, linking to existing user_external")
            # TODO contact_user_external_mapping_result_tuple
            mapping_tuple = self.select_multi_mapping_tuple_by_id(
                entity_name1=self.default_entity_name1, entity_name2=self.default_entity_name2,
                entity_id1=contact_id, entity_id2=user_external_id)
            if not mapping_tuple:
                self.logger.info("mapping_tuple is None, creating new mapping")
                contact_user_external_id = self.insert_mapping(
                    entity_name1=self.default_entity_name1, entity_name2=self.default_entity_name2,
                    entity_id1=contact_id, entity_id2=user_external_id,
                    ignore_duplicate=True)
            else:
                self.logger.info("mapping_tuple is not None")
                contact_user_external_id = mapping_tuple[0]

        return contact_user_external_id

    def __get_external_profile_id_dict_from_urls(self, *, urls: list[str]) -> list[dict]:
        """
        Get usernames
        :param websites: websites
        :return: usernames
        """
        external_profiles_ids_dicts: list[dict] = []
        try:
            for url in urls:
                organization_name = self.internet_domain.get_organization_name(url)
                if organization_name:
                    organization_name_lower = organization_name.lower()
                    profile_id_dict: dict = {}
                    if organization_name_lower == "linkedin":
                        profile_id_dict = ContactUserExternalLocal.extract_linkedin_profile_id(linkedin_profile_url=url)
                    elif organization_name_lower == "facebook":
                        profile_id_dict = ContactUserExternalLocal.extract_facebook_profile_id(facebook_profile_url=url)
                    elif organization_name_lower == "instagram":
                        profile_id_dict = ContactUserExternalLocal.extract_instagram_profile_id(instagram_profile_url=url)
                    if profile_id_dict:
                        external_profiles_ids_dicts.append(profile_id_dict)
        except Exception as exception:
            self.logger.warning("get_usernames_from_urls exception: Failed", object={"exception": exception})
        finally:
            return external_profiles_ids_dicts

    @staticmethod
    def extract_facebook_profile_id(facebook_profile_url: str) -> dict[str, str] or None:
        # Regex pattern for extracting the profile id
        # TODO: add these regexes to url_type_regex_table and get them from there
        regex_string_id = r'https?://www\.facebook\.com/([a-zA-Z0-9.]+)'
        regex_int_id = r'https?://www\.facebook\.com/profile\.php\?id=([0-9]+)'

        # Check if the url matches the pattern for string id
        match_string_id = re.match(regex_string_id, facebook_profile_url)
        if match_string_id and 'profile.php?id=' not in facebook_profile_url:
            return {'facebook string profile id': match_string_id.group(1)}

        # Check if the url matches the pattern for int id
        match_int_id = re.match(regex_int_id, facebook_profile_url)
        if match_int_id:
            return {'facebook int profile id': match_int_id.group(1)}

        return None

    @staticmethod
    def extract_instagram_profile_id(instagram_profile_url: str) -> dict[str, str] or None:
        # Regex pattern for extracting the Instagram username
        # TODO: add this regex to url_type_regex_table and get it from there
        regex_instagram_id = r'https?://www\.instagram\.com/([a-zA-Z0-9._]+)/?'

        match_instagram_id = re.match(regex_instagram_id, instagram_profile_url)
        if match_instagram_id:
            return {'instagram profile id': match_instagram_id.group(1)}

        return None

    @staticmethod
    def extract_linkedin_profile_id(linkedin_profile_url: str) -> dict[str, str] or None:
        # Regex patterns for extracting the LinkedIn profile id
        # TODO: add these regexes to url_type_regex_table and get them from there
        regex_linkedin_string_id = r'https?://www\.linkedin\.com/in/([a-zA-Z0-9-]+)/?'
        regex_linkedin_int_id = r'https?://www\.linkedin\.com/profile/view\?id=([0-9]+)'

        match_linkedin_string_id = re.match(regex_linkedin_string_id, linkedin_profile_url)
        if match_linkedin_string_id:
            return {'linkedin string profile id': match_linkedin_string_id.group(1)}

        match_linkedin_int_id = re.match(regex_linkedin_int_id, linkedin_profile_url)
        if match_linkedin_int_id:
            return {'linkedin int profile id': match_linkedin_int_id.group(1)}

        return None

    def get_system_id(self, platform_name: str) -> int:
        system_id = self.select_one_value_by_column_and_value(
            schema_name="system", view_table_name="system_ml_view",
            select_clause_value="system_id", column_name="title", column_value=platform_name)
        self.set_schema(schema_name=DEFAULT_SCHEMA_NAME)
        return system_id

    def get_system_id_by_external_profile_id_type(self, external_profile_id_type: str) -> int:
        if 'facebook' in external_profile_id_type:
            platform_name = 'Facebook'
        elif 'instagram' in external_profile_id_type:
            platform_name = 'Instagram'
        elif 'linkedin' in external_profile_id_type:
            platform_name = 'LinkedIn'
        system_id = self.get_system_id(platform_name=platform_name)
        return system_id
