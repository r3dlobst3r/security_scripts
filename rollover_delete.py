### Delete all rollover scans
from tenable.sc import TenableSC
with TenableSC('IP', username='USER', password='PASS') as sc:
    for scan in sc.scans.list(fields=['status', 'name', 'type', 'schedule'])['usable']:
        if scan['schedule']['type'] == 'rollover':
            sc.scans.delete(scan['id'])
            print('Removed {}'.format(scan['name']))
