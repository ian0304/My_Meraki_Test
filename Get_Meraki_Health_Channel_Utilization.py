import meraki
import pprint
import getpass
from matplotlib import pyplot as plt

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

org_networks = dashboard.organizations.getOrganizationNetworks(organization_id, total_pages='all')

for i in org_networks:
    if i['name'] == net_name:
        network_id = (i['id'])

channel_utili = dashboard.networks.getNetworkNetworkHealthChannelUtilization(network_id, total_pages='all')

for i in channel_utili:
    time_stamp = []
    utilization = []
    wifi24G_utili = channel_utili[0]['wifi0']
    for xy in wifi24G_utili:
        time_stamp.append(xy['start_ts'][11:16])
        utilization.append(xy['utilization'])
    plt.figure(figsize=(15, 8))
    plt.plot(time_stamp[-12:],utilization[-12:]) 
    plt.title('{} 2.4G WIFI Utilization'.format(i['serial']))
    plt.ylabel('2.4GWIFI Utilization')
    plt.xlabel('Time')
    plt.show()
    
    
    
    time_stamp = []
    utilization = []
    wifi5G_utili = channel_utili[0]['wifi1']
    for xy in wifi5G_utili:
        time_stamp.append(xy['start_ts'][11:16])
        utilization.append(xy['utilization'])
    plt.figure(figsize=(15, 8))
    plt.plot(time_stamp[-12:],utilization[-12:]) 
    plt.title('{} 5G WIFI Utilization'.format(i['serial']))
    plt.ylabel('5GWIFI Utilization')
    plt.xlabel('Time')
    plt.show()