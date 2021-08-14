import meraki
import pprint
import getpass

print("This script is to get Wireless Serial from Meraki Dashboard")
org_name = input("Enter Your Org Name: ")
net_name = input("Enter Network Name: ")
api_key = getpass.getpass("Enter Your API_KEY: ")
url = 'https://api.meraki.com'

dashboard = meraki.DashboardAPI(
    api_key=api_key,
    base_url= url + '/api/v1/',
    output_log=False,
    print_console=False
)

org_list = dashboard.organizations.getOrganizations()
for org in org_list:
    if org['name'] == org_name:
        organization_id = org['id']

device_list = []

org_networks = dashboard.organizations.getOrganizationNetworks(organization_id, total_pages='all')

for i in org_networks:
    if i['name'] == net_name:
        network_id = (i['id'])

net_devices = dashboard.networks.getNetworkDevices(network_id)

for i in org_networks:
    if i['name'] == net_name:
        network_id = (i['id'])

net_devices = dashboard.networks.getNetworkDevices(network_id)

for i in net_devices:
    if i['model'].startswith('MR'):
        device_list.append(i['serial'])

if device_list == []:
    print('No wireless access point in this site.')
else:
    print(device_list)
    