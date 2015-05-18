from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import RegionInfo
from datetime import datetime
import time
import sys
import logging
from snaplib import get_resource_tags, set_resource_tags, date_compare
from config import config


date_suffix = datetime.today().strftime('%b')
# Counters
total_creates = 0
total_deletes = 0
count_errors = 0

# List with snapshots to delete
deletelist = []

message = ""
error_message = ""

count_success = 0
count_total = 0

# Setup logging
logging.basicConfig(filename=config['log_file'], level=logging.INFO)
start_message = 'Started taking snapshots at %(date)s' % {
    'date': datetime.today().strftime('%d-%m-%Y %H:%M:%S')
}

message += start_message + "\n\n"
logging.info(start_message)

# Get settings from config.py
aws_access_key = config['aws_access_key']
aws_secret_key = config['aws_secret_key']
ec2_region_name = config['ec2_region_name']
ec2_region_endpoint = config['ec2_region_endpoint']
keep = config['keep']

region = RegionInfo(name=ec2_region_name, endpoint=ec2_region_endpoint)
if aws_access_key:
        conn = EC2Connection(aws_access_key, aws_secret_key, region=region)

print 'Finding volumes that match the requested tag ({ "tag:%(tag_name)s": "%(tag_value)s" })' % config
vols = conn.get_all_volumes(filters={config['tag_name']: config['tag_value']})


for vol in vols:

    try:
        count_total += 1
        logging.info(vol)
        tags_volume = get_resource_tags(vol.id, conn)
        description = 'snapshot %(vol_id)s_%(date_suffix)s by snapshot script at %(date)s' % {
            'vol_id': vol.id,
            'date_suffix': date_suffix,
            'date': datetime.today().strftime('%d-%m-%Y %H:%M:%S')
        }
        try:
            current_snap = vol.create_snapshot(description)
            set_resource_tags(current_snap, tags_volume)
            suc_message = 'Snapshot created with description: %s and tags: %s' % (description, str(tags_volume))
            print '     ' + suc_message
            logging.info(suc_message)
            total_creates += 1
        except Exception, e:
            print "Unexpected error:", sys.exc_info()[0]
            logging.error(e)
            pass

        snapshots = vol.snapshots()
        deletelist = []
        for snap in snapshots:
            deletelist.append(snap)

        deletelist.sort(date_compare)

        delta = len(deletelist) - keep
        for i in range(delta):
            del_message = '     Deleting snapshot ' + deletelist[i].description
            logging.info(del_message)
            deletelist[i].delete()
            total_deletes += 1
        time.sleep(3)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        logging.error('Error in processing volume with id: ' + vol.id)
        error_message += 'Error in processing volume with id: ' + vol.id
        count_errors += 1
    else:
        count_success += 1

result = '\nFinished making snapshots at %(date)s with %(count_success)s snapshots of %(count_total)s possible.\n\n' % {
    'date': datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
    'count_success': count_success,
    'count_total': count_total
}

message += result
message += "\nTotal snapshots created: " + str(total_creates)
message += "\nTotal snapshots errors: " + str(count_errors)
message += "\nTotal snapshots deleted: " + str(total_deletes) + "\n"

print '\n' + message + '\n'
print result

logging.info(result)

