import rubrik_cdm
import datetime
import os, json, sys, time
import requests
import argparse


requests.packages.urllib3.disable_warnings()

#Insert ARGS Here
parser = argparse.ArgumentParser()
parser.add_argument('--mvname', help='The Name of the Rubrik Managed Volume.')
parser.add_argument('--sla', help='Rubrik SLA Domain to snapshot the managed volume into.')
parser.add_argument('--workload', help='The Name of the TrilioVault workload to backup.')
args_list = parser.parse_args()

tvault_mv_name = args_list.mvname

tvault_workload_name = args_list.workload
tvault_user = os.environ.get("TVAULT_USER")
tvault_pass = os.environ.get("TVAULT_PASS")
tvault_url = os.environ.get("TVAULT_URL")

#Triliovault Functions

def tvault_get_token(ip, user, password):
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    body={}
    body['username'] = user
    body['password'] = password
    response = requests.post('https://' + ip + ':8780/v1/admin/ovirt-engine/sso/oauth/token', data=json.dumps(body), headers=headers, verify=False)
    response = response.json()
    return response['access_token']

def tvault_get_workload_id(ip, ovirt_token, workload_name):
    headers = {"accept": "application/json", "Content-Type": "application/json", "x-ovirtauth-token": ovirt_token}
    response = requests.get('https://' + ip + ':8780/v1/admin/workloads/detail', headers=headers, verify=False)
    response = response.json()
    for workload in response['workloads']:
        if workload['name'] == workload_name:
            return workload['id']
    sys.exit("Workload " + workload_name + "not found in Triliovault Configuration!.  Exiting.")

def tvault_take_snapshot(ip, ovirt_token, workload_id, snapshot_name, snapshot_desc):
    headers = {"accept": "application/json", "Content-Type": "application/json", "x-ovirtauth-token": ovirt_token}
    body={}
    body['snapshot'] = {}
    body['snapshot']['name'] = snapshot_name
    body['snapshot']['description'] = snapshot_desc
    response = requests.post('https://' + ip + ':8780/v1/admin/workloads/' + workload_id + '?full=0', data=json.dumps(body), headers=headers, verify=False)
    response = response.json()
    return response

def tvault_get_workload_status(ip, ovirt_token, workload_id):
    headers = {"accept": "application/json", "Content-Type": "application/json", "x-ovirtauth-token": ovirt_token}
    response = requests.get('https://' + ip + ':8780/v1/admin/workloads/' + workload_id, data={}, headers=headers, verify=False)
    response = response.json()
    return response['workload']['status']

def tvault_get_snapshot_details(ip, ovirt_token, workload_id, snapshot_id):
    headers = {"accept": "application/json", "Content-Type": "application/json", "x-ovirtauth-token": ovirt_token}
    response = requests.get('https://' + ip + ':8780/v1/admin/snapshots?workload_id=' + workload_id, headers=headers, verify=False)
    response = response.json()
    for snapshot in response['snapshots']:
        if snapshot['id'] == snapshot_id:
            return snapshot
    sys.exit("Snapshot " + snapshot_id + "not found in Triliovault Configuration!.  Exiting.")

#Connect to Rubrik Cluster
rubrik = rubrik_cdm.Connect()

#Begin MV Snapshot (Make Writable)
print("Making Rubrik Managed Volume " + tvault_mv_name + " writable in preparation for Triliovault Snapshot.")
begin_snapshot = rubrik.begin_managed_volume_snapshot(tvault_mv_name)
print(begin_snapshot)

#Begin Triliovault Snapshot on Workload
tvault_token = tvault_get_token(tvault_url, tvault_user, tvault_pass)
workload_id = tvault_get_workload_id(tvault_url, tvault_token, tvault_workload_name)

snapshot_status = tvault_take_snapshot(tvault_url, tvault_token, workload_id, snapshot_name="rbk-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"), snapshot_desc="rbk-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

#Check Progress of Triliovault Snapshot - Sleep Loop until done
while True:
    workload_status = tvault_get_workload_status(tvault_url, tvault_token, workload_id)
    snapshot_details = tvault_get_snapshot_details(tvault_url, tvault_token, workload_id, snapshot_status['snapshot']['id'])
    print("Workload status: " + workload_status + "    Snapshot Progress: " + str(snapshot_details['progress_percent']) + "    Status: " + snapshot_details['status'])
    if workload_status == 'available' and snapshot_details['progress_percent'] == 100:
        print("Triliovault Snapshot Completed !!!")
        break
    else:
        time.sleep(20)

#End MV Snapshot (Read-Only)
print("Taking Snapshot of Rubrik Managed Volume " + tvault_mv_name + " and converting it back to Read-Only.")
end_snapshot = rubrik.end_managed_volume_snapshot(tvault_mv_name, sla_name=args_list.sla)
print(end_snapshot)

print("DONE")
