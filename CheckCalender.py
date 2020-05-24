import json
import requests
import pprint
from datetime import datetime


def get_base_link():
    base_link = 'https://date.nager.at/Api/v2/'
    return base_link


class Info:

    def __init__(self, year=2020, country='Germany', free_on=''):
        self.country = country
        self.country_abb = ''
        self.year = year
        self.public_holidays = []

        if type(free_on) is list:
            self.free_on = free_on
        else:
            raise Excepetion('No list given')

        self.country_code = self.get_country_abbreviation(self.country)

    def set_free_on(self, list):
        self.free_on = list

    def get_free_on(self):
        return self.free_on

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
        country_info = json.loads(response.text)
        return self.country_info

    def get_public_holidays(self):
        response = requests.get('https://date.nager.at/api/v2/PublicHolidays/{Year}/{CountryCode}'.
                                format(Year=self.year,
                                       CountryCode=self.country_code))
        # print(self.year, self.country_code)
        self.data = json.loads(response.text)

        for name in self.data:
            print(name['localName'])
            self.public_holidays.append(name['localName'])
        return self.public_holidays


def compare(info_list, info2_list):
    if type(info_list) is list and type(info2_list) is list:
        if info_list == info2_list:
            print('Congrats, you found your date ({info_list})'.format(info_list=info_list))
        else:
            for hd in info_list:
                for hd2 in info2_list:
                    if hd == hd2:
                        print(hd)


info = Info(free_on=['Pfingsten', 'Karfreitag', 'Buß- und Bettag', 'Weihnachten'])
info2 = Info(free_on=['Neujahr', 'Karfreitag', 'Weihnachten'])

user_country = 'Germany'
# pprint.pprint(info.get_country_info(info.get_country_abbreviation(user_country)))

compare(info.get_free_on(), info2.get_free_on())
