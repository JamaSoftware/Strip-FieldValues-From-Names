
from jamaconfig import JamaConfig
from core.itemType import ItemType
from jamaclient import JamaClient

import re


class PostProcess:
    def __init__(self):
        self.jama_client = JamaClient()
        self.items = []
        self.jama_config = JamaConfig()
        self.projectId = 0
        self.itemTypeId = 0
        self.itemType = None
        self.LOG_FILENAME = "failures.json"
        self.success = 0
        self.failure = 0

    def process(self):
        try:
            self.itemTypeId = self.jama_config.itemType
            self.projectId = self.jama_config.projectId
            if(self.itemTypeId != 0):
                self.retrieve_items()
                self.jama_config.logger.info("Retrieved [" + str(self.items.__len__()) + "] items of itemType [" + str(self.itemTypeId) + "]")
                self.process_items()
                self.jama_config.logger.info("Successfully processed [" + str(self.success) + "] items")
                self.jama_config.logger.error("Failed to process [" + str(self.failure) + "] items")

        except AttributeError:
            self.jama_config.logger.critical("itemType is not set in jamaconfig.py")
        print "Finished..."


    def retrieve_items(self):
        self.itemType = ItemType(self.itemTypeId)
        if(self.itemType != None):
            self.jama_config.logger.info("Retrieving all items of itemType [" + str(self.itemTypeId) + "]...")
            self.items = self.jama_client.get_all("abstractitems?project=" + str(self.projectId) + "&itemType=" + str(self.itemTypeId))
        else:
            self.jama_config.logger.error("Something went wrong when retrieving itemType [" + str(self.itemTypeId) + "]")
            exit(1)


    def process_items(self):
        for item in self.items:
            attribute_key_values = self.name_contains_attributes(item)
            if attribute_key_values != None:
                self.jama_config.logger.info("Found an item [" + str(item["id"]) +"] with attributes embedded in name...")
                self.extract_and_patch(item, attribute_key_values)
                self.jama_config.logger.info("Patched item [" + str(item["id"]) + "]")
            else:
                self.jama_config.logger.warning("Item [" + str(item["id"]) + "] does not have attributes embedded in name - SKIPPING")



    def name_contains_attributes(self, item):
        name = item["fields"]["name"]
        pattern = "##.*#"
        found = re.search(pattern=pattern, string=name)
        if(found):
            print "Found!"
            return found.group()
        print "No found :("
        return None


    def extract_and_patch(self, item, attribute_key_values):
        attributes = attribute_key_values.replace("##", "").split(",")
        key_value_array = []
        for key_value_pair in attributes:
            assembled_key_value_pair = self.assemble_patch_op(key_value_pair)
            if assembled_key_value_pair != None:
                key_value_array.append(assembled_key_value_pair)
        if key_value_array.__len__() > 0:
            updated_name_op = self.assemble_updated_name(item, attribute_key_values)
            key_value_array.append(updated_name_op)
            response = self.jama_client.patch_item(item["id"], key_value_array)
            if response.status_code == 200:
                self.jama_config.logger.info("Successfully updated item [" + str(item["id"]) + "]")
                self.success = self.success + 1
            else:
                self.jama_config.logger.error("Failed to update item [" + str(item["id"]) + "]")
                self.failure = self.failure + 1



    def assemble_patch_op(self, key_value_pair):
        to_return = {}
        elements = key_value_pair.split(":")
        if elements.__len__() < 2:
            return None
        if(str(elements[1]) == " ") == True:
            return None
        # if(elements[0].lstrip(" ").rstrip(" ") == "UniqueID"):
        #     field = self.itemType.get_field("dbid")
        # else:
        field = self.itemType.get_field(elements[0].lstrip(" ").rstrip(" "))
        field_name = None
        field_value = None
        if field != None:
            field_name = field.get("name")
            if(field.get("isPicklist") == True):
                field_value = field.get("options").get(elements[1].lstrip(" ").rstrip(" "))
            else:
                field_value = elements[1]
        else:
            self.jama_config.logger.warning("Field not found for [" + str(key_value_pair) + "] - skipping")

        if field_value != None and field_name != None:
            to_return.__setitem__("op", "add")
            to_return.__setitem__("path", "/fields/" + field_name)
            to_return.__setitem__("value", field_value)
            return to_return
        else:
            return None


    def assemble_updated_name(self, item, attribute_value_pair):
        name = item.get("fields").get("name").replace(attribute_value_pair, "")
        object = {}
        object.__setitem__("op", "add")
        object.__setitem__("path", "/fields/name")
        object.__setitem__("value", name)
        return object
