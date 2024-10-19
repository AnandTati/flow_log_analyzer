from collections import defaultdict
import csv
import os


class LogParser:

    @staticmethod
    def analyze(flow_log_file_name, lookup_file_name, protocol_map_file_name):

        # Validating map file existence
        if not os.path.exists(lookup_file_name):
            raise FileNotFoundError('Lookup map file missing')

        if not os.path.exists(protocol_map_file_name):
            raise FileNotFoundError('Protocol map file missing')

        print('Reading lookup and protocol map files')

        # Read the lookup file.
        # The file contains the tag name for the port/protocol combination
        # port,protocol,tagname
        with open(lookup_file_name) as csvfile:
            reader = csv.reader(csvfile)
            lookup_data = list(reader)[1:] # Ignore first line (column headers)
            lookup_map = {}
            for port, protocol, tagname in lookup_data:
                if port not in lookup_map:
                    lookup_map[port] = {}

                lookup_map[port][protocol] = tagname

        # Read the protocol file.
        # ref: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
        # The file contains the protocol number to keyword text mapping.
        # protocol,keyword
        with open(protocol_map_file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            protocol_map = {}
            for row in reader:
                # Protocol number maybe mentioned as range (e.g. 1-10)
                if '-' in row['Protocol']:
                    ranges = row['Protocol'].split('-')
                    for i in range(int(ranges[0]), int(ranges[1])+1):
                        protocol_map[i] = row['Keyword']
                    continue
                protocol_map[int(row['Protocol'])] = row['Keyword']

        print('Parsing Flow Log file')

        # Count of matches for each tag
        tag_count_map = defaultdict(int)
        # Count of matches for each port/protocol combination
        port_count_map = defaultdict()

        # Now read each line from the flow log file and update the count.
        with open(flow_log_file_name) as logfile:
            untagged = 0
            for line in logfile:
                # Split the line as per the format
                # Ref: https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
                parts = line.split(' ')

                port = parts[6] # dst port
                protocol_num = int(parts[7]) # protocol number
                if protocol_num not in protocol_map:
                    # @INVALID_PROTOCOL
                    # Based on situation, here either
                    # - can raise exception, investigate NOW
                    # - can log a line and continue, investigate LATER via log files
                    # - capture as INVALID and continue, investigate LATER via log and count map
                    # For now, here the third option is chosen
                    protocol = 'INVALID_PROTOCOL'
                else:
                    protocol = protocol_map[protocol_num] # protocol number to keyword string

                # If the port in the log is in lookup then update numbers,
                # else update the 'untagged'
                if port in lookup_map:
                    # Get the tagname from the lookup.
                    protocol_tag_map = lookup_map[port]
                    if protocol in protocol_tag_map:
                        tag_name = protocol_tag_map[protocol]
                        tag_count_map[tag_name] += 1
                    # This case depends on the 'INVALID_PROTOCOL' option selection. Look for '@INVALID_PROTOCOL' above.
                    else:
                        tag_count_map[protocol] += 1

                    # Init port_count dictionary with port
                    if port not in port_count_map:
                        port_count_map[port] = {}
                    # Init protocol name in the sub dictionary
                    if protocol not in port_count_map[port]:
                        port_count_map[port][protocol] = 0    

                    port_count_map[port][protocol] += 1
                else:
                    untagged += 1

            # Keeping untagged counter at the end.
            if untagged > 0:
                tag_count_map['Untagged'] = untagged

        print('Completed parsing Flow Log file')
        return tag_count_map, port_count_map    
    
def write_to_file(tag_count_map, port_count_map):
    if not os.path.exists('./out'):
        os.makedirs('./out')

    with open('./out/tag_count.csv', 'w') as f:
        f.write('Tag,Count\n')
        for tag, count in tag_count_map.items():
            f.write(f"{tag},{count}\n")

    with open('./out/port_count.csv', 'w') as f:
        f.write('Port,Protocol,Count\n')
        for port, proto_count in port_count_map.items():
            for protocol, count in proto_count.items():
                f.write(f"{port},{protocol},{count}\n")

def main():
    protocol_map_file_name = './src/data/protocol.csv'

    # Pass the flow log file to analyzer
    lookup_file_name = './src/data/lookup.csv'
    flow_log_file_name = './src/data/flow.log'
    tag_count_map, port_count_map = LogParser.analyze(flow_log_file_name, lookup_file_name, protocol_map_file_name)
    write_to_file(tag_count_map, port_count_map)

if __name__ == '__main__':
    main()