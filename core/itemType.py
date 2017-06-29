import json

from jamaclient import JamaClient
from jamaconfig import JamaConfig

class ItemType:
    def __init__(self, itemTypeId):
        self.jama_client = JamaClient()
        self.jama_config = JamaConfig()
        self.itemTypeId = itemTypeId
        self.itemType = json.loads(self.jama_client.get(self.jama_config.rest_url + "itemtypes/" + str(itemTypeId)).text)["data"]
        self.field_map = {}
        self.assemble_itemType()

    def assemble_itemType(self):
        fields = self.itemType.get("fields")
        for field in fields:
            self.assemble_and_add_to_field_map(field)


    def assemble_and_add_to_field_map(self, field):
        if field.get("readOnly") == True:
            return
        object = {}
        object.__setitem__("name", field.get("name"))
        if field.get("pickList") != None:
            isPicklist = True
        else:
            isPicklist = False
        object.__setitem__("isPicklist", isPicklist)
        if isPicklist == True:
            options = {}
            list_of_options = json.loads(self.jama_client.get(self.jama_config.rest_url + "picklists/" + str(field.get("pickList")) + "/options").text)["data"]
            for option in list_of_options:
                options.__setitem__(option.get("name"), option.get("id"))
            object.__setitem__("options", options)

        if field.get("label") == "DbID":
            self.field_map.__setitem__("UniqueID", object)
        else:
            self.field_map.__setitem__(field.get("label"), object)


    def get_field(self, field_label):
        return self.field_map.get(field_label)
