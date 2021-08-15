import meraki
import pprint
import getpass
from matplotlib import pyplot as plt

print("This script is to get Wireless Serial from Meraki Dashboard")
url_location = input("""
Which Meraki URL you want to access: 
1) https://api.meraki.com
2) https://api.meraki.cn

""")
if url_location == '1':
    url = 'https://api.meraki.com'
elif url_location == '2':
    url = 'https://api.meraki.cn'
print("Accessing {} ...".format(url))

org_name = input("Enter Your Org Name: ")
net_name = input("Enter Network Name: ")
api_key = getpass.getpass("Enter Your API_KEY: ")
time_range = 0-int(input("Last 1, 2 or 3 hours' Channel Utilization you want to check: "))*6

wifi_channel = input("""
Which wifi channel you want to check: 
1) 2.4G
2) 5G

""")
if wifi_channel == '1':
    wifi_channel = 'wifi0'
    wifi_signal = '2.4G'
elif wifi_channel == '2':
    wifi_channel = 'wifi1'
    wifi_signal = '5G'

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
    wifi24G_utili = channel_utili[0][wifi_channel]
    for xy in wifi24G_utili:
        time_stamp.append(xy['start_ts'][11:16])
        utilization.append(xy['utilization'])
    plt.figure(figsize=(15, 8))
    plt.plot(time_stamp[time_range:],utilization[time_range:]) 
    plt.title('{} {} WIFI Utilization'.format(i['serial'],wifi_signal))
    plt.ylabel('{} WIFI Utilization'.format(wifi_signal))
    plt.xlabel('Time')
    plt.show()
    
