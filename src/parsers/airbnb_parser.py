import json
from bs4 import BeautifulSoup
from src.parsers.parser import NOT_FOUND, Parser
import re


class AirBnBParser(Parser):
    def get_property_attributes(self, html):
        if not html:
            raise Exception("HTML is empty")

        site_json = self._get_site_json(html)

        return {
            "name": self._get_property_name(site_json),
            "type": self._get_property_type(site_json),
            "num_bedrooms": self._get_num_bedrooms(site_json),
            "num_bathrooms": self._get_num_bathrooms(site_json),
            "amenities": self._get_amenities_list(site_json),
        }

    def _get_property_name(self, site_json):
        name = self._get_json_value(site_json, "listingTitle")

        return name if name else NOT_FOUND

    def _get_property_type(self, site_json):
        type = self._get_json_value(site_json, "propertyType")

        return type if type else NOT_FOUND

    def _get_num_bathrooms(self, site_json):
        title = self._get_json_value(site_json, "ogTitle")
        num_bathrooms = (
            int(re.split(r"bathroom", title)[0].split()[-1])
            if title
            else NOT_FOUND
        )

        return num_bathrooms

    def _get_num_bedrooms(self, site_json):
        title = self._get_json_value(site_json, "ogTitle")
        num_bedrooms = (
            int(re.split(r"bedroom", title)[0].split()[-1])
            if title
            else NOT_FOUND
        )

        return num_bedrooms

    def _get_amenities_list(self, site_json):
        all_amenities = self._get_json_value(site_json, "seeAllAmenitiesGroups")

        if not all_amenities:
            return NOT_FOUND

        included_amenities = [
            a["amenities"] for a in all_amenities if a["title"] != "Not included"
        ]

        return [a["title"] for amenity in included_amenities for a in amenity]

    def _get_json_value(self, json_input, lookup_key):
        if isinstance(json_input, dict):
            for k, v in json_input.items():
                if k == lookup_key:
                    return v
                else:
                    result = self._get_json_value(v, lookup_key)
                    if result:
                        return result
        elif isinstance(json_input, list):
            for item in json_input:
                result = self._get_json_value(item, lookup_key)
                if result:
                    return result

    def _get_site_json(self, html):
        soup = BeautifulSoup(html, "html.parser")

        json_el = soup.find("script", {"id": "data-injector-instances"})

        if not json_el:
            return {}

        return json.loads(json_el.contents[0])