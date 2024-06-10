import random
import string

from database_mysql_local.generic_mapping import GenericMapping
from logger_local.MetaLogger import MetaLogger
from phonenumbers import PhoneNumberFormat, format_number, parse
from user_context_remote.user_context import UserContext

from .phone_local_constans import code_object_init

user_context = UserContext()


# TODO Either PhonesLocal(GenericCrud) or PhoneXXXLocal(GenericMapping)
#   We use GenericMapping here with person_phone, contact_phone, phone_profile (see insert_mapping_if_not_exists)
#   So what should XXX be?
class PhonesLocal(GenericMapping, metaclass=MetaLogger, object=code_object_init):
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(default_schema_name="phone",
                         default_table_name="phone_table",
                         default_view_table_name="phone_view",
                         default_column_name="phone_id",
                         is_test_data=is_test_data)

    def get_phone_full_number_normalized_by_phone_id(self, phone_id: int) -> str:
        phone_number = self.select_one_value_by_column_and_value(
            select_clause_value="local_number_normalized", column_value=phone_id)
        # phone_number can start with 0
        return phone_number  # TODO: should we add area_code?

    # TODO: test
    def get_normalized_phone_number_by_phone_original_str(self, phone_original_str: str) -> str:
        phone_number = self.select_one_value_by_column_and_value(
            select_clause_value="local_number_normalized",
            column_name="number_original", column_value=phone_original_str)
        # phone_number can start with 0
        return phone_number

    def verify_phone_number(self, phone_number: int) -> None:
        self.update_by_column_and_value(column_value=phone_number,
                                        data_dict={"is_verified": 1})
        

    def is_verified(self, phone_number: int) -> bool or None:
        # TODO Why do we need this? Where is it used? - Please add comment
        # TODO Why not phone_id when searching the database? - I was expecting it to be part of the phone_dict
        # TODO Phone verified is per profile and per the phone itself, right? If someone else verified the phone it doesn't count.  so we should include the profile_id in this fuction
        """:return None if not found, True if verified, False if not verified."""
        is_verified = self.select_one_value_by_column_and_value(
            select_clause_value="is_verified", column_value=phone_number, column_name="number_original")
        return is_verified

    @staticmethod
    def normalize_phone_number(original_number: str, region: str) -> dict:
        """
        Normalize phone number to international format.
        :param original_number: Original phone number.
        :param region: Region of the phone number.
        :return: Dictionary with the normalized phone number and the international code.

        Example:
        original_number = "0549338666"
        region = "IL"
        result = {
            "international_code": 972,
            "full_number_normalized": "+972549338666"
        }
        """
        # TODO Where region is coming from?
        # TODO I think regions is GUSH-DAN in our terminology. I was expecting country_id or country_code or country_name.
        #   [region is the terminology of the external library phonenumbers, should ignore their terminology?]
        parsed_number = parse(original_number, region)
        international_code = parsed_number.country_code
        full_number_normalized = format_number(parsed_number, PhoneNumberFormat.E164)
        if full_number_normalized.startswith("+"):
            full_number_normalized = full_number_normalized[1:]
        # parsed_number example: original_number='0687473298' -> PhoneNumber(country_code=972, national_number=687473298, extension=None, italian_leading_zero=None, number_of_leading_zeros=None, country_code_source=0, preferred_domestic_carrier_code=None)
        # TODO: Shall we add area_code? what shall it be? How can we do it?
        # TODO Can we move number_info to data member in PhoneLocal class
        # TODO phone_number_dict
        number_info = {
             # TODO "number_original": number_original
            "number_original": original_number,
            "international_code": international_code,
            "full_number_normalized": full_number_normalized,
            "local_number_normalized": parsed_number.national_number,
            "extension": parsed_number.extension,
        }
        return number_info

    def get_country_iso_code(self, location_id: int = None, contact_id: int = None,  profile_id: int = None,
                             country_id: int = None) -> str:
        if not country_id:  # get country_id from location_id
            if not location_id:  # get location_id from contact_id or profile_id
                if contact_id and not profile_id:  # get profile_id from contact_id
                    profile_id = self.select_one_value_by_column_and_value(
                        schema_name="contact_profile",
                        view_table_name='contact_profile_view', select_clause_value='profile_id',
                        column_name='contact_id', column_value=contact_id)
                assert profile_id, "profile_id is required for getting location_id"
                location_id = self.select_one_value_by_column_and_value(
                    schema_name="location_profile",
                    view_table_name='location_profile_view', select_clause_value='location_id',
                    column_name='profile_id', column_value=profile_id)

            assert location_id, "location_id is required for getting country_id"
            country_id = self.select_one_value_by_column_and_value(
                schema_name="location", view_table_name='location_view', select_clause_value='country_id',
                column_name='location_id', column_value=location_id)

        country_iso_code = self.select_one_value_by_column_and_value(
            schema_name="location", view_table_name='country_ml_view', select_clause_value='iso',
            column_name='country_id', column_value=country_id)
        return country_iso_code

    # TODO: Is it really necessary to access the database for location?
    # I think it's possible to get the normalized phone number and the international code
    # from original_phone_number
    def process_phone(self, original_phone_number: str, country_iso_code: str = None, contact_id: int = None,
                      profile_id: int = None, person_id: int = None, location_id: int = None,
                      country_id: int = None, profiles_ids_list: list[int] = None) -> dict:
        """
        Process phone number and return normalized phone number.
        :return: Dictionary with the normalized phone number and the international code.
        """

        if location_id is not None or country_id is not None:
            country_iso_code = country_iso_code or self.get_country_iso_code(
                location_id=location_id, contact_id=contact_id, profile_id=profile_id, country_id=country_id
            )
        normalized_phone_number = self.normalize_phone_number(
            original_number=original_phone_number, region=country_iso_code)
        phone_dict = {
            'number_original': original_phone_number,
            'international_code': normalized_phone_number['international_code'],
            'full_number_normalized': normalized_phone_number['full_number_normalized'],
            'local_number_normalized': int(str(normalized_phone_number['full_number_normalized'])
                                           .replace(str(normalized_phone_number['international_code']), '')),
            'created_user_id': user_context.get_effective_user_id(),
        }
        phone_compare_data_dict = {
            "full_number_normalized": phone_dict.get("full_number_normalized"),
        }
        phone_id = self.upsert(data_dict=phone_dict, data_dict_compare=phone_compare_data_dict,
                               view_table_name="phone_view", table_name="phone_table",
                               compare_with_or=True)

        # link phone to profile
        phone_profiles_ids = []
        if profiles_ids_list is not None:
            for profile_id in profiles_ids_list:
                phone_profile_id = self.insert_mapping_if_not_exists(
                    schema_name='phone_profile',
                    entity_name1='phone', entity_name2='profile', entity_id1=phone_id, entity_id2=profile_id)
                phone_profiles_ids.append(phone_profile_id)
        elif profile_id is not None:  # left this for backward compatibility
            phone_profile_id = self.insert_mapping_if_not_exists(
                schema_name='phone_profile', entity_name1='phone', entity_name2='profile',
                entity_id1=phone_id, entity_id2=profile_id)
            phone_profiles_ids.append(phone_profile_id)
        else:
            phone_profile_id = None

        # link phone to contact
        if contact_id is not None:
            contact_phone_id = self.insert_mapping_if_not_exists(
                schema_name='contact_phone', entity_name1='contact', entity_name2='phone',
                entity_id1=contact_id, entity_id2=phone_id)
        else:
            contact_phone_id = None

        # link phone to person
        if person_id is not None:
            phone_person_id = self.insert_mapping_if_not_exists(
                schema_name='person_phone', entity_name1='person', entity_name2='phone',
                entity_id1=person_id, entity_id2=phone_id)
        else:
            phone_person_id = None

        result = {
            'phone_profiles_ids': phone_profiles_ids,
            'phone_id': phone_id,
            'normalized_phone_number': normalized_phone_number,
            'original_phone_number': original_phone_number,
            'contact_phone_id': contact_phone_id,
            'phone_person_id': phone_person_id,
        }

        return result

    def insert_phone(self, phone_data: dict) -> int:
        """
        Insert phone data into the phone table.
        :param phone_data: Dictionary with the phone data.
        :return: Phone id.
        """
        
        phone_id = self.insert(data_dict=phone_data)
        
        return phone_id

    def get_test_phone_id(self, number_original: str, international_code: int = 972) -> int:
        phone_data = {
            'number_original': number_original,
            'local_number_normalized': int(number_original[3:]),  # must be unique
            'full_number_normalized': f'+{international_code}{number_original[1:]}',
            'international_code': international_code,
            'area_code': int(number_original[1:3]),
            'extension': number_original[3],
        }
        test_phone_id = self.insert_phone(phone_data=phone_data)
        return test_phone_id

    @staticmethod
    # TODO Let's use International Dialing code 999, let's use area code 059 (or something else with is invalid)
    #  TODO generate_fake_phone_number_original(...)
    def generate_fake_phone_number(prefix: str = "05", length: int = 8) -> str:
        remaining_digits = ''.join(random.choices(string.digits, k=length))
        fake_phone_number = prefix + remaining_digits
        return fake_phone_number
