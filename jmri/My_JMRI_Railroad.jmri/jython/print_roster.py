import jmri
import jmri.jmrit.roster

import json

# get a list of matched roster entries;
# the list of None's means match everything
roster_list = jmri.jmrit.roster.Roster.getDefault().matchingList(None, None, None, None, None, None, None)

# now loop through the matched entries, printing things
for entry in roster_list.toArray():
    roster_entry = {}
    roster_entry['id'] = entry.getId()
    roster_entry['display_name'] = entry.getDisplayName()
    roster_entry['comment'] = entry.getComment()
    roster_entry['decoder_comment'] = entry.getDecoderComment()
    roster_entry['decoder_family'] = entry.getDecoderFamily()
    roster_entry['decoder_model'] = entry.getDecoderModel()
    roster_entry['date_modified'] = entry.getDateUpdated()
    roster_entry['dcc_address'] = entry.getDccAddress()
    roster_entry['road_name'] = entry.getRoadName()
    roster_entry['road_number'] = entry.getRoadNumber()
    roster_entry['filename'] = entry.getFileName()
    roster_entry['icon_path'] = entry.getIconPath()
    roster_entry['image_path'] = entry.getImagePath()
    roster_entry['max_function_num'] = entry.getMAXFNNUM()
    roster_entry['max_speed_percent'] = entry.getMaxSpeedPCT()
    roster_entry['manufacturer'] = entry.getMfg()
    roster_entry['model'] = entry.getModel()
    roster_entry['owner'] = entry.getOwner()
    roster_entry['path_name'] = entry.getPathName()
    roster_entry['protocol'] = entry.getProtocolAsString()
    roster_entry['shunting_function'] = entry.getShuntingFunction()
    roster_entry['url'] = entry.getURL()
    roster_entry['is_long_address'] = entry.isLongAddress()
    roster_entry['is_open'] = entry.isOpen()

    json_output = json.dumps(roster_entry)

    id_string = str(roster_entry['id'])
    clean_id_string = sanitize_id(id_string)

    attributes_string = get_roster_attributes_path(id_string)
    publish(attributes_string, str(json_output), 0, True)

    state_string = get_roster_state_path(id_string)
    discovery_string = get_discovery_sensor_path(id_string)

    discovery_entry = {}

    discovery_entry['name'] = id_string
    discovery_entry['unique_id'] = clean_id_string
    discovery_entry['state_topic'] = state_string
    discovery_entry['json_attributes_topic'] = attributes_string
    discovery_entry['unit_of_measurement'] = "Throttle"

    json_output = json.dumps(discovery_entry)
    publish(discovery_string, str(json_output), 0, True)

