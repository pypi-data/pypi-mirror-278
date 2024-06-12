import re

from database_mysql_local.generic_crud import GenericCRUD
from group_local.group_local_constants import GroupLocalConstants
from logger_local.MetaLogger import MetaLogger
from python_sdk_remote.utilities import remove_digits

from .people_constants import PeopleLocalConstants


# FirstName and LastName act differently (i.e. nickname), multiple nick names, name with four parts, Hebrew last names, Soundex ... 
# TODO Create FirstName class
# TODO Create LastName class 

# TODO We want to keep the history of social network profiles in our storage- To know what they have changed? When? 
#  Please call storage-local-python-package with the URLs of contacts, persons, and profiles. Maybe you, should add it to people-local-python-package.


# TODO: When fields such as first name, last name, organization, job_title, group_name, city ... contains "?" then is_sure=false
# TODO Should person, profile, contact, and user inherit PeopleLocal or not?
class PeopleLocal(GenericCRUD, metaclass=MetaLogger,
                  object=PeopleLocalConstants.PEOPLE_LOCAL_PYTHON_PACKAGE_CODE_LOGGER_OBJECT):
    def __init__(self, *, default_schema_name: str, default_table_name: str = None,
                 default_view_table_name: str = None, default_column_name: str = None,
                 default_view_with_deleted_and_test_data: str = None,
                 default_select_clause_value: str = "*", default_where: str = None,
                 first_name_original: str = None, last_names_original: list = None,
                 organizations_names_original: list = None, email_addresses: list = None, urls: list = None,
                 is_test_data: bool = False) -> None:
        super().__init__(is_test_data=is_test_data, default_schema_name=default_schema_name,
                         default_table_name=default_table_name, default_view_table_name=default_view_table_name,
                         default_column_name=default_column_name,
                         default_view_with_deleted_and_test_data=default_view_with_deleted_and_test_data,
                         default_select_clause_value=default_select_clause_value, default_where=default_where)
        self.first_name_original = None
        self.last_names_original = []
        self.normalized_first_name = None
        self.normalized_last_names = []
        self.organizations_names_original = []
        self.organizations_names_short = []
        self.email_addresses = []
        self.urls = []
        # Don't change PeopleLoca.set_details to self.set_details
        # As this can break inheriting classes, for example ContactsLocal
        PeopleLocal.set_details(
             self,
             first_name_original=first_name_original, last_names_original=last_names_original,
             organizations_names_original=organizations_names_original, email_addresses=email_addresses,
             urls=urls)

    def set_details(self, *, first_name_original: str = None, last_names_original: list = None,
                    organizations_names_original: list = None, email_addresses: list = None,
                    urls: list = None) -> None:
        self.first_name_original = first_name_original
        self.last_names_original = last_names_original or []
        self.normalized_first_name = None
        self.normalized_last_names = []
        self.organizations_names_original = organizations_names_original or []
        self.organizations_names_short = []
        self.email_addresses = email_addresses or []
        self.urls = urls or []
        self.__extract_first_name_from_email_address()
        self.__extract_organization_str_from_email_addresses_str()
        self.__extract_organization_strs_from_urls_str()
        self.__extract_organizations_names_short_from_organizations_names_original()
        self.normalize_names()

    def _process_first_name_str(self, add_people_to_a_group_function: callable, **kwargs) -> str or None:

        if not self.normalized_first_name:
            self.logger.warning("normalized_first_name is None")
            return
        self.logger.info("normalized_first_name", object={
            'normalized_first_name': self.normalized_first_name})
        group_dict = {
            'title': self.normalized_first_name,
            'name': self.normalized_first_name,
        }
        kwargs['groups_dicts'] = [group_dict]
        if "?" in self.normalized_first_name:
            kwargs["mapping_data_json"] = {
                "is_sure": False
            }
        result = add_people_to_a_group_function(**kwargs)
        # TODO Please use GenericCrudMl to update the person.first_name_table
        # TODO Create a group to all people with the same first name and add this contact/profile to the group
        return result

    def _process_last_names_str(self, add_people_to_a_group_function: callable, **kwargs) -> list:
        results = []
        for normalized_last_name in self.normalized_last_names:
            self.logger.info("normalized_last_name", object={
                'normalized_last_name': normalized_last_name})
            group_dict = {
                'title': normalized_last_name,
                'name': normalized_last_name,
            }
            kwargs['groups_dicts'] = [group_dict]
            if "?" in normalized_last_name:
                kwargs["mapping_data_json"] = {
                    "is_sure": False
                }
            results.append(add_people_to_a_group_function(**kwargs))
        # TODO Create a group to the family and add this contact/profile to the group
        return results

    def _process_organizations_str(self, add_people_to_a_group_function, **kwargs) -> list:
        results = []
        for organization_name in self.organizations_names_original:
            group_dict = {
                'title': organization_name,
                'name': organization_name,
            }
            kwargs['groups_dicts'] = [group_dict]
            # TODO: if there's "Ventures" in the organization name, shall we add
            # GroupLocalConstants.VENTURE_CAPITAL_GROUP_ID as parent_group_id
            # to all groups in self.organizations_names_original?
            if "Ventures" in organization_name:
                kwargs['parent_group_id'] = GroupLocalConstants.VENTURE_CAPITAL_GROUP_ID
            if "?" in organization_name:
                kwargs["mapping_data_json"] = {"is_sure": False}
            results.append(add_people_to_a_group_function(**kwargs))

        return results

    # TODO: is this supposed to call methods like link_contact_to_domain in DomainLocal?
    # def _process_urls_str(self, link_people_to_domain_function, **kwargs):
    def __extract_organization_str_from_email_addresses_str(self) -> None:
        if not self.email_addresses:
            self.logger.warning("email address is None")
            return
        for email_address in self.email_addresses:
            domain_part = email_address.split('@')[-1]
            organization_name_parts = domain_part.rsplit('.', 1)[0]
            organization_name = ' '.join(part for part in organization_name_parts.split('.'))
            self.__append_if_not_exists(lst=self.organizations_names_original, item=organization_name.capitalize())

    #  organizations_names_short is organizations_names_original without "Ltd", "Inc" ...
    def __extract_organizations_names_short_from_organizations_names_original(self) -> None:
        if not self.organizations_names_original:
            self.logger.warning("organizations_names_original is None")
            return

        for organization_name in self.organizations_names_original:
            pattern = re.compile(r'\b(?:Ltd|Inc|Corporation|Corp|LLC|L.L.C.|GmbH|AG|S.A.|SARL)\b\.?', re.IGNORECASE)
            short_organization_name = re.sub(pattern, '', organization_name).strip()
            short_organization_name = re.sub(r',\s*$', '', short_organization_name).strip()
            self.__append_if_not_exists(lst=self.organizations_names_short, item=short_organization_name)

    def __extract_organization_strs_from_urls_str(self) -> None:
        if not self.urls:
            self.logger.warning("urls are empty")
        else:
            for url in self.urls:
                if url is None:
                    continue
                stripped_url = url.replace('http://', '').replace('https://', '').replace('www.', '')
                organization_name = stripped_url.split('.')[0]
                organization_name_capitalized = organization_name.capitalize()
                self.__append_if_not_exists(lst=self.organizations_names_original, item=organization_name_capitalized)

    def __extract_first_name_from_email_address(self) -> None:
        if self.first_name_original:
            return
        if not self.email_addresses:
            self.logger.warning("email addresses are empty")
            return
        email_address = self.email_addresses[0]
        local_part = email_address.split('@')[0]

        for separator in ['.', '_']:
            if separator in local_part:
                first_name = local_part.split(separator)[0]
                break
        else:
            first_name = local_part
        self.first_name_original = first_name.capitalize()

    def normalize_names(self):
        first_name = self.first_name_original
        last_names = self.last_names_original
        if first_name:
            if len(first_name.split()) > 1 and len(last_names) == 0:
                first_name_parts = self.first_name_original.split()
                last_names = (first_name_parts[1:])
                first_name = first_name_parts[0]
        if first_name:
            self.normalized_first_name = remove_digits(first_name)
            self.normalized_first_name = self.normalized_first_name.split()[0]
        for last_name in last_names:
            normalized_last_name = remove_digits(last_name)
            normalized_last_name = normalized_last_name.split()[0]
            self.normalized_last_names.append(normalized_last_name)

    @staticmethod
    def split_first_name_field(first_name: str) -> dict:
        first_name_parts = first_name.split() if first_name else []
        first_name = first_name_parts[0] if first_name_parts else None
        last_name = ' '.join(first_name_parts[1:]) if len(first_name_parts) > 1 else None
        first_and_last_name = {'first_name': first_name, 'last_name': last_name}
        return first_and_last_name

    # TODO: move this to python-sdk-remote
    @staticmethod
    def __append_if_not_exists(lst: list, item: str) -> None:
        if item not in lst:
            lst.append(item)

    # TODO: Complete this method
    def get_people_id(self, *, people_entity_name: str, ids_dict: dict) -> int or None:
        if people_entity_name == "person":
            if ids_dict.get("contact_id"):
                contact_id = ids_dict.get("contact_id")
                person_id = self.__get_person_id_from_contact_details(
                    people_entity_name=people_entity_name, contact_id=contact_id)
                return person_id

    # TODO: Complete this method - people_entity_name not used
    def __get_person_id_from_contact_details(self, *, people_entity_name: str, contact_id: int) -> int:
        if people_entity_name == "person":
            # Try to get person_id from contact_person_view
            person_id = self.select_one_value_by_column_and_value(
                schema_name="contact_person",
                view_table_name="contact_person_view",
                select_clause_value="person_id",
                column_name="contact_id",   # Don't delete this, default_column_name can be wrong because of inheritance
                column_value=contact_id)
            if person_id is None:
                # Try to get 3 email_address_ids from contact_email_address_view
                email_address_ids = self.select_multi_value_by_column_and_value(
                    schema_name="contact_email_address",
                    view_table_name="contact_email_address_view",
                    select_clause_value="email_address_id",
                    column_name="contact_id",   # Don't delete this, default_column_name can be wrong because of inheritance
                    column_value=contact_id,
                    limit=3,
                    order_by="email_address_id DESC",
                    skip_null_values=True
                )
                # Try to get person_id from email_address_person_view
                for email_address_id in email_address_ids:
                    # TODO: insert to email_address_person_table when inserting a new contact (or/and person?)
                    person_id = self.select_one_value_by_column_and_value(
                        schema_name="email_address_person", view_table_name="email_address_person_view",
                        select_clause_value="person_id", column_name="email_address_id", column_value=email_address_id)
                    if person_id is None:
                        # Try to get person_id from person_view
                        person_id = self.select_one_value_by_column_and_value(
                            schema_name="person", view_table_name="person_view", select_clause_value="person_id",
                            column_name="main_email_person", column_value=email_address_id)
                    if person_id:
                        break
            if person_id is None:
                # Try to get 3 phone_ids from contact_phone_view
                phone_ids = self.select_multi_value_by_column_and_value(
                    schema_name="contact_phone", view_table_name="contact_phone_view",
                    select_clause_value="phone_id", column_name="contact_id",
                    column_value=contact_id, limit=3, order_by="phone_id DESC")
                # Try to get person_id from person_phone_view
                for phone_id in phone_ids:
                    # TODO: insert to person_phone_table when inserting a new contact
                    person_id = self.select_one_value_by_column_and_value(
                        schema_name="person_phone", view_table_name="person_phone_view",
                        select_clause_value="person_id", column_name="phone_id", column_value=phone_id)
                    if person_id:
                        break
            return person_id
        return None
