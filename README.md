# Strip Field Values from Names of Items

# Jama Software
Jama Software is the definitive system of record and action for product development. The company’s modern requirements and test management solution helps enterprises accelerate development time, mitigate risk, slash complexity and verify regulatory compliance. More than 600 product-centric organizations, including NASA, Boeing and Caterpillar use Jama to modernize their process for bringing complex products to market. The venture-backed company is headquartered in Portland, Oregon. For more information, visit [jamasoftware.com](http://jamasoftware.com).

Please visit [dev.jamasoftware.com](http://dev.jamasoftware.com) for additional resources and join the discussion in our community [community.jamasoftware.com](http://community.jamasoftware.com).

## How it Works
This script is designed to extract fields from items' names in Jama. It was created to help facilitate ReqPro migrations that use documents to store rich text content. Fields and their values will be parsed from items' names, fields will be populated with the correct values, and names will be updated to not include field values. 
In order to parse out field values, item names must be set up in the following manner:
 
```name##FieldName1:FieldValue2,FieldName2:FieldValue2##```
* The start and ending ## is what the script uses to determine where the fields and their values being and end.
* The field names should match the field's label within the itemType in Jama
* Field values that are of picklist/multiselect options must be spelled exactly as it exists in Jama
* A colon (:) should separate field names and the associating value
* A comma (,) should be used to separate one field from the next
* No spaces should be included between the starting and ending ##

Please note that this script is distributed as-is as an example and will likely require modification to work for your specific use-case.  This example omits error checking. Jama Support will not assist with the use or modification of the script.

### Before you begin
- Install Python 2.7 or higher and the requests library.  [Python](https://www.python.org/) and [Requests](http://docs.python-requests.org/en/latest/)

### Setup
1. As always, set up a test environment and project to test the script.

2. Fill out the jamaconfig.py section of the script.  The necessary fields are:
  - ```username```
  - ```password```
  - ```base_url```  
  - ```itemType```   - itemType API ID
  - ```projectId```

