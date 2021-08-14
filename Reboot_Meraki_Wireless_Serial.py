import meraki
import pprint
import getpass

print("This script is to reboot Meraki AP ~")
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

for i in net_devices:
    if i['model'].startswith('MR'):
        device_list.append(i)

print('#'* 40)

if device_list == []:
    print('No wireless access point in this site.')
else:
    for i in device_list:
        print("{} {} ".format(i['model'],i['serial']))
    
#Reboot AP

for i in device_list:
    response = dashboard.devices.rebootDevice(i['serial'])
    print(response)
    if response['success'] == True:
        print("{} is rebooting ...".format(i['serial']))
    else:
        print("{} isn't online".format(i['serial']))
