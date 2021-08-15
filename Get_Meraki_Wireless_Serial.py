import meraki
import pprint
import getpass

print("This script is to get Wireless Serial from Meraki Dashboard")
org_name = input("Enter Your Org Name: ")
net_name = input("Enter Network Name: ")
api_key = getpass.getpass("Enter Your API_KEY: ")
url_location = input("""
Which Meraki URL you want to access: 
1) https://api.meraki.com
2) https://api.meraki.cn

""")
if url_location == '1':
    url = 'https://api.meraki.com'
elif url_location == '2':
    url = 'https://api.meraki.cn'

print(url)

device_list = []

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

org_networks = dashboard.organizations.getOrganizationNetworks(organization_id, total_pages='all')

for i in org_networks:
    if i['name'] == net_name:
        network_id = (i['id'])

net_devices = dashboard.networks.getNetworkDevices(network_id)

for i in net_devices:
    if i['model'].startswith('MR'):
        device_list.append(i)
        

if device_list == []:
    print('No wireless access point in this site.')
else:
    for i in device_list:
        print("{} {} ".format(i['model'],i['serial']))