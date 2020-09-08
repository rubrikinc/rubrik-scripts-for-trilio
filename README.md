# Rubrik and TrilioVault Scripts

This repository contains scripts that can be used to orchestrate the activity between TrilioVault and Rubrik.  Currently there is only a single script within the repo (`rbk-tvault_rhv_backup.py`) and the below instructions will reflect the usage of this single script.  The README will be updated once multiple scripts get uploaded.

## :wrench:Usage and Requirements for `rbk-tvault_thv_backup.py`

This script is designed to interact with the TrilioVault RHV product to orchestrate an on-demand backup from TrilioVault that is back-ended by a Rubrik Managed Volume.

You must have a working Python 3 environment with the Rubrik SDK for Python properly installed and configured.  Additional instructions for installing and configuring the Rubrik SDK for Python can be found [here](https://github.com/rubrikinc/rubrik-sdk-for-python/blob/master/docs/quick-start.md)


The following environment variables must be present:

```bash
export TVAULT_URL='triliovault.my.lab'
export TVAULT_USER='admin@internal'
export TVAULT_PASS='myTvaultPassword'
```

As this project uses the Rubrik SDK for Python it also requires one of the following sets of environment variables:

1 - username/password:

```bash
export rubrik_cdm_node_ip=192.168.0.1
export rubrik_cdm_username='admin'
export rubrik_cdm_password='MyPassword123!'
```

2 - API token:

```bash
export rubrik_cdm_node_ip=192.168.0.1
export rubrik_cdm_token='1234abcd-2345-67ef-a12b-1234abcd5678'
```
Once these are present, the script can be called with the below syntax:

```
usage: rbk-tvault_rhv_backup.py [-h] [--mvname MVNAME] [--sla SLA] [--workload WORKLOAD]

optional arguments:
  -h, --help           show this help message and exit
  --mvname MVNAME      The Name of the Rubrik Managed Volume.
  --sla SLA            Rubrik SLA Domain to snapshot the managed volume into.
  --workload WORKLOAD  The Name of the TrilioVault workload to backup.
```
## :mag: Example

The below is a quick example of calling the script with output that follows a successful backup:
```
python3 rbk-tvault_rhv_backups.py --mvname TVAULT_REPO --sla Gold --workload rhel-rbk-test1

Making Rubrik Managed Volume TVAULT_REPO writable in preparation for Triliovault Snapshot.
{'snapshotId': '27a340bb-457d-49f6-a2fc-9dd0703f3092'}
Workload status: locked    Snapshot Progress: 0    Status: starting
Workload status: locked    Snapshot Progress: 0    Status: Executing backup:[VMSnapshot]
Workload status: locked    Snapshot Progress: 0    Status: Executing backup:[VMSnapshot]
Workload status: locked    Snapshot Progress: 0    Status: Executing backup:[Transport]
Workload status: locked    Snapshot Progress: 0    Status: RemoveOldSnapshots
Workload status: locked    Snapshot Progress: 0    Status: RemoveOldSnapshots
Workload status: locked    Snapshot Progress: 0    Status: RemoveOldSnapshots
Workload status: locked    Snapshot Progress: 0    Status: RemoveOldSnapshots
Workload status: locked    Snapshot Progress: 0    Status: RemoveOldSnapshots
Workload status: locked    Snapshot Progress: 0    Status: RemoveOldSnapshots
Workload status: available    Snapshot Progress: 100    Status: available
Triliovault Snapshot Completed !!!
Taking Snapshot of Rubrik Managed Volume TVAULT_REPO and converting it back to Read-Only.
{'id': '27a340bb-457d-49f6-a2fc-9dd0703f3092', 'date': '2020-09-08T12:29:13.000Z',
 'sourceObjectType': 'ManagedVolume', 'isOnDemandSnapshot': True, 'isCustomRetentionApplied': False,
 'cloudState': 0, 'indexState': 0, 'replicationLocationIds': [], 'archivalLocationIds': [],
 'slaId': '4101153d-d8b4-4914-afec-78094292f41f', 'slaName': 'Gold', 'isRetainedByRetentionLockSla': False, 'isPlacedOnLegalHold': False,
 'links': {'self': {'href': 'https://192.168.0.1/api/internal/managed_volume/snapshot/27a340bb-457d-49f6-a2fc-9dd0703f3092', 'rel': 'self'}},
 'isQueuedSnapshot': True}
DONE
```


## :blue_book: Documentation

Here are some resources to get you started! If you find any challenges from this project are not properly documented or are unclear, please raise an issueand let us know! This is a fun, safe environment - don't worry if you're a GitHub newbie! :heart:

* Quick Start Guide
* [Rubrik API Documentation](https://github.com/rubrikinc/api-documentation)

## :muscle: How You Can Help

We glady welcome contributions from the community. From updating the documentation to adding more functions for Python, all ideas are welcome. Thank you in advance for all of your issues, pull requests, and comments! :star:

* [Contributing Guide](CONTRIBUTING.md)
* [Code of Conduct](CODE_OF_CONDUCT.md)

## :pushpin: License

* [MIT License](LICENSE)

## :point_right: About Rubrik Build

We encourage all contributors to become members. We aim to grow an active, healthy community of contributors, reviewers, and code owners. Learn more in our [Welcome to the Rubrik Build Community](https://github.com/rubrikinc/welcome-to-rubrik-build) page.

We'd  love to hear from you! Email us: build@rubrik.com :love_letter:
