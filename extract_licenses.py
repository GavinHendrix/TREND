import json

# Replace 'SBOM.json' with the path to your actual SBOM file
with open("SBOM.json") as fp:
    data = json.load(fp)

licenses = set()

# Navigate through the SBOM structure to extract licenses
for component in data.get('components', []):
    for license_info in component.get('licenses', []):
        license = license_info.get('license')
        if 'id' in license:
            licenses.add(license['id'])  # Add license IDs
        #elif 'name' in license:
        #   licenses.add(license['name'])  # Add license names (fallback)

print(licenses)
