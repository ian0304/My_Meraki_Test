def login_info ():
    print("This script is to get serial information from Meraki Dashboard")
    url = input("""
    Which Meraki URL you want to access - 1 or 2: 
    1) https://api.meraki.com
    2) https://api.meraki.cn
    
    """)
    if url == '1':
        url = 'https://api.meraki.com'
    elif url == '2':
        url = 'https://api.meraki.cn'
    print("Accessing {} ...".format(url))
    org_name = input("\nEnter Your Org Name: ")
    net_name = input("\nEnter Network Name: ")
    api_key = getpass.getpass("\nEnter Your API_KEY: ")
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

    return dashboard, network_id, organization_id


def device_serial(dashboard, network_id):
    device_list = []
    device_serial_list = []
    net_devices = dashboard.networks.getNetworkDevices(network_id)
    device_type = input("""
        Which type of device's serials - 1, 2 or 3: 
        1) MX Firewall
        2) MS Switch
        3) MR Wireless Access Pionts
        
        """)
    if device_type == '1':
        device_type = 'MX'
        device_type_name = 'Firewall'
    elif device_type == '2':
        device_type = 'MS'
        device_type_name = 'Switch'
    elif device_type == '3':
        device_type = 'MR'
        device_type_name = 'Wireless Access Point'
    
    for i in net_devices:
        if i['model'].startswith(device_type):
            device_serial_list.append({i['model']:i['serial']})
            
    return device_serial_list


import meraki
import pprint
import getpass

dashboard, network_id, organization_id = login_info()
response = device_serial(dashboard, network_id)
for i in response:
    pprint.pprint(i)