import time

from jamaconfig import JamaConfig
import requests
import json
import warnings
from requests import HTTPError


class JamaClient:
    def __init__(self):
        self.jama_config = JamaConfig()
        self.id_map = {}
        self.delete_list = []
        self.auth = self.jama_config.auth
        self.verify = self.jama_config.verify_ssl
        self.seconds = 2

    def get(self, url):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return requests.get(url, auth=self.auth, verify=self.verify)


    def get_all(self, resource):
        all_results = []
        results_remaining = True
        current_start_index = 0
        delim = '&' if '?' in resource else '?'
        while results_remaining:
            start_at = delim + "startAt={}".format(current_start_index)
            url = self.jama_config.rest_url + resource + start_at
            print url
            response = self.get(url)
            json_response = json.loads(response.text)
            if "pageInfo" not in json_response["meta"]:
                print json_response
                return [json_response["data"]]
            result_count = json_response["meta"]["pageInfo"]["resultCount"]
            total_results = json_response["meta"]["pageInfo"]["totalResults"]
            results_remaining = current_start_index + result_count != total_results
            current_start_index += 20
            all_results.extend(json_response["data"])

        return all_results

    def patch_item(self, id, patch_values):
        url = self.jama_config.rest_url + "items/" + str(id)
        try:
            response = requests.patch(url, auth=self.auth, verify=self.verify, json=patch_values)
            return response
        except HTTPError as e:
            print "Unable to patch item [" + str(id) + "] due to [" + e + "]"


    def clean_up(self):
        delete_url = self.jama_config.rest_url + "items/{}"
        for url in [delete_url.format(url) for url in self.delete_list]:
            self.delay()
            requests.delete(url, auth=self.auth, verify=self.verify)

    def delay(self):
        time.sleep(self.seconds)


