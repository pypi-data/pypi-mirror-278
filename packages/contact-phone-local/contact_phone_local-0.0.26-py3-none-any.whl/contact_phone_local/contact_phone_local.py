from database_mysql_local.generic_mapping import GenericMapping
from logger_local.MetaLogger import MetaLogger
from phones_local.phones_local import PhonesLocal

from .contact_phone_local_constants import CONTACT_PHONE_PYTHON_PACKAGE_CODE_LOGGER_OBJECT

DEFAULT_SCHEMA_NAME = 'contact_phone'
DEFAULT_ENTITY_NAME1 = 'contact'
DEFAULT_ENTITY_NAME2 = 'phone'
DEFAULT_ID_COLUMN_NAME = 'contact_phone_id'
DEFAULT_TABLE_NAME = 'contact_phone_table'
DEFAULT_VIEW_TABLE_NAME = 'contact_phone_view'


class ContactPhoneLocal(GenericMapping, metaclass=MetaLogger, object=CONTACT_PHONE_PYTHON_PACKAGE_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data: bool = False):

        GenericMapping.__init__(self, default_schema_name=DEFAULT_SCHEMA_NAME,
                                default_entity_name1=DEFAULT_ENTITY_NAME1,
                                default_entity_name2=DEFAULT_ENTITY_NAME2, default_column_name=DEFAULT_ID_COLUMN_NAME,
                                default_table_name=DEFAULT_TABLE_NAME, default_view_table_name=DEFAULT_VIEW_TABLE_NAME,
                                is_test_data=is_test_data)

    # UPSERT
    # TODO Why do we have region as a parameter? - Should be able to extract it from the phone or contact_id
    # TODO Expected phone_number is original_phone_number of processed_phone_number?
    # TODO: contact_dict not used
    def insert_contact_and_link_to_existing_or_new_phone(
            self, *, contact_dict: dict, phone_number_original: str, contact_id: int = None, profile_id: int = None,
            person_id: int = None, location_id: int = None, country_id: int = None, region: str = None) -> dict:
        """
        Insert contact and link to existing or new phone
        :param contact_dict: contact dict
        :param phone_number: phone number
        :param contact_id: contact id
        :param region: region (For example, 'US' stands for the United States, 'GB' for the United Kingdom)
        :return: contact_phone_id
        """
        # We prefer to get contact_id from contact_dict, but for backward compatibility we also accept contact_id argument
        contact_id = contact_dict.get("contact_id") or contact_id
        # We prefer to get person_id from contact_dict, but for backward compatibility we also accept person_id argument
        person_id = contact_dict.get("person_id") or person_id
        # We prefer to get location_id from contact_dict, but for backward compatibility we also accept location_id argument
        location_id = contact_dict.get("location_id") or location_id
        # We prefer to get country_id from contact_dict, but for backward compatibility we also accept country_id argument
        country_id = contact_dict.get("country_id") or country_id
        profiles_ids_list = contact_dict.get("profiles_ids_list")
        phones_local = PhonesLocal(is_test_data=self.is_test_data)
        process_phone_result_dict: dict = phones_local.process_phone(
            original_phone_number=phone_number_original,
            contact_id=contact_id,
            profiles_ids_list=profiles_ids_list,
            person_id=person_id,
            location_id=location_id,
            country_id=country_id,
        )
        '''
        # Old version
        # TODO = PhoneLocal. (without s)
        proccessed_phone_number = PhonesLocal.normalize_phone_number(original_number=phone_number, region=region)
        full_number_normalized = proccessed_phone_number.get("full_number_normalized")
        local_number_normalized = proccessed_phone_number.get("local_number_normalized")
        if not full_number_normalized or not local_number_normalized:
            raise Exception(f"Invalid phone number: {phone_number}")

        # Add the people(person/contact/profile/user) to the Country Group based on their phone internationa_dialing_code
        # TODO call process_people_phone_number( entity_name='Contact', phone) from phone-local-python-package

        # I would recommend moving this code to the PhoneLocal class and calling it in the Phone constructor
        # TODO Can we replace this by UPSERT?
        phone_id_tuple = self.phones_local.select_one_tuple_by_where(
            select_clause_value="phone_id",
            where="number_original = %s OR full_number_normalized = %s OR local_number_normalized = %s",
            params=(phone_number, full_number_normalized, local_number_normalized)
        )

        if not phone_id_tuple:
            # create new phone and add it to phone_table
            self.logger.info("phone_id is None, adding new phone")
            phone_compare_data_dict = {
                "number_original": proccessed_phone_number.get("number_original"),
                "full_number_normalized": proccessed_phone_number.get("full_number_normalized"),
                "local_number_normalized": proccessed_phone_number.get("local_number_normalized"),
            }
            phone_id = self.phones_local.upsert(data_dict=proccessed_phone_number,
                                                data_dict_compare=phone_compare_data_dict,
                                                view_table_name="phone_view", table_name="phone_table",
                                                compare_with_or=True)
            contact_phone_id = self.insert_mapping(entity_name1=self.default_entity_name1,
                                                   entity_name2=self.default_entity_name2,
                                                   entity_id1=contact_id, entity_id2=phone_id,
                                                   ignore_duplicate=True)
        else:
            # link to existing phone
            self.logger.info("phone_id is not None, linking to existing phone")
            phone_id = phone_id_tuple[0]
            mapping_tuple = self.select_multi_mapping_tuple_by_id(entity_name1=self.default_entity_name1,
                                                                  entity_name2=self.default_entity_name2,
                                                                  entity_id1=contact_id, entity_id2=phone_id)
            if not mapping_tuple:
                self.logger.info("mapping_tuple is None, creating new mapping")
                contact_phone_id = self.insert_mapping(entity_name1=self.default_entity_name1,
                                                       entity_name2=self.default_entity_name2,
                                                       entity_id1=contact_id, entity_id2=phone_id,
                                                       ignore_duplicate=True)
            else:
                self.logger.info("mapping_tuple is not None")
                contact_phone_id = mapping_tuple[0][0]
        '''

        return process_phone_result_dict
