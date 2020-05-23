import json
import requests
import pprint
from datetime import datetime


def get_base_link():
    base_link = 'https://date.nager.at/Api/v2/'
    return base_link


class Info:

    def __init__(self):
        self.country = {}
        self.country_abb = ''
        self.country_info = ''

    def loads_specific_data(self, add_link: str):
        """
        method loads specific data and stores it in class variable
        :param add_link: string to add to the basic url
        :return: json formatted object
        """
        response = requests.get(get_base_link() + add_link)
        json_response = json.loads(response.text)
        return json_response

    def get_country_abbreviation(self, country: str) -> list:
        self.countries = self.loads_specific_data('AvailableCountries')

        # find country in list and return abbreviation
        for piece in self.countries:
            for key, value in piece.items():
                if value == country:
                    return piece['key']

    def get_country_info(self, cntry_abb: str = None):
        """
        get the abbreviation for the country from the user input
        :param cntry_abb: Shortcut of the country
        :return: list of all info concerning the country
        """""
        response = requests.get(
            get_base_link() + 'CountryInfo?countryCode={country_abb}'.format(country_abb=cntry_abb))
        self.country_info = json.loads(response.text)
        return self.country_info

    def get_common_name(self):
        for piece in self.country_info:
            return piece


class Calender:

    def __init__(self, yr=datetime.year, country_code=''):
        self.year = yr
        self.country_code = country_code
        self.dict = {}
        self.public_holidays = []

        if country_code == '':
            raise Exception("No country selected")
        # TODO: abhandeln ohne Programm zu beenden?

        response = requests.get('https://date.nager.at/api/v2/PublicHolidays/{Year}/{CountryCode}'.
                                format(Year=self.year,
                                       CountryCode=self.country_code))
        self.data = response.text

    def get_public_holidays(self):
        return self.public_holidays

    def get_dict(self):
        self.dict = {
            'CountryCode': self.country_code,
            'commonName': info.get_common_name(),
            'currentTime': '',
            'publicHolidays': ''
        }
        return dict


info = Info()
user_country = input("Which Country?")
# pprint.pprint(info.get_country_info(info.get_country_abbreviation(user_country)))
if user_country != '':
    person1 = Calender(country_code=info.get_country_abbreviation(user_country))
else:
    person1 = Calender()
