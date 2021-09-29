import veryfi
import pprint

client_id = "vrfLWsFjUAO3OnyAjOsFXHAdRXclPtApst1tUvO"
client_secret = "g1Z0XzlXOuBVUAOzDp7IVyWfV1trboXJ2ZUIrCIyKBYEL2GpJlwszFjY3DcWgfy3o6t7N4V5mlXAu0EzgMp0xJ4ZsB0rdKNlCCAmNDOr2LCPJUjL411efoGfkAkWbC1i"
username = "lsyuan1029"
api_key = "9e9a239893ff64c881780da0d85f9d69"

client = veryfi.Client(client_id, client_secret, username, api_key)

categories = ["Travel", "Airfare", "Lodging", "Job Supplies and Materials", "Grocery"."insurance claim"]
result = client.process_document("assets/invoice2.png", categories)
pprint.pprint(result)
print(result["total"])
# parsed = json.loads(result)
# print(json.dumps(parsed, indent=4, sort_keys=True));