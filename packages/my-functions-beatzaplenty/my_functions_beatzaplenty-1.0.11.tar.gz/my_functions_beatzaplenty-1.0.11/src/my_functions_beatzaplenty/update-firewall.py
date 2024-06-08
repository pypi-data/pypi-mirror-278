# Function to get the current IP address
def get_current_ip(hostname):
    import socket
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

# Function to read the last IP address from the INI file
def get_last_ip(default_config):
    try:
        return default_config.get("last_ip")
    except:
        return None

#Function to update config file with new values
def update_config(config_file, ip_address, tzinfo, tz_string_format):
    import configparser, datetime
    edit = configparser.ConfigParser()
    edit.read(config_file)
    config_items = edit["firewall"]
    config_items["last_ip"] = ip_address
    config_items["last_change"] = datetime.now(tzinfo).strftime(tz_string_format)
    with open(config_file, "w") as config:
        edit.write(config)

# Function to update firewall rules
def update_firewall_rules(current_ip, last_ip, default_config, rules_config, LOG_FILE, tzinfo, tz_string_format, parent_dir):
    import datetime, subprocess
    with open(LOG_FILE, "w") as log_file:
        log_file.write("Run time: " + str(datetime.datetime.now(tzinfo).strftime(tz_string_format)) + "\n")
        log_file.write("Last Change: " + str(default_config.get("last_change")) + "\n")

        if current_ip != last_ip:
            log_file.write("Last IP address: " + str(last_ip) + "\n")
            log_file.write("Current IP address: " + str(current_ip) + "\n")

            for key in rules_config:
                protocol, port = rules_config[key].split(':')
                del_cmd = f"sudo ufw delete allow proto {protocol} from {last_ip} to any port {port}"
                add_cmd = f"sudo ufw allow proto {protocol} from {current_ip} to any port {port}"

                log_file.write(f"Deleting rule: {del_cmd}\n")
                subprocess.run(del_cmd, shell=True, executable="/bin/bash", stdout=log_file)

                log_file.write(f"Adding rule: {add_cmd}\n")
                subprocess.run(add_cmd, shell=True, executable="/bin/bash", stdout=log_file)
            
            update_config(f'{parent_dir}/config.ini', current_ip, tzinfo, tz_string_format)
        else:
            log_file.write(f"IP address {current_ip} is correct. No firewall changes needed\n")
        log_file.flush()

def update_before_rules(current_ip, config_file):
    import re, subprocess, configparser
    
    # Read the config file
    config = configparser.ConfigParser()
    config.read(config_file)
    before_rules_config = config['before_rules']
    
    # Define the path to the before.rules file
    before_rules_path = before_rules_config.get("file_path")

    # Read the before.rules file content
    with open(before_rules_path, "r") as file:
        lines = file.readlines()

    # Define the new IP with /32
    new_ip_with_cidr = f"{current_ip}/32"

    # Get the lines to update from the config
    input_line_identifier = before_rules_config.get("input_line")
    forward_line_identifier = before_rules_config.get("forward_line")

    # Initialize flags to track if lines were updated
    input_line_updated = False
    forward_line_updated = False

    # Update the specific lines with the new IP address
    updated_lines = []
    for line in lines:
        if input_line_identifier in line:
            updated_line = re.sub(r"-s\s+\d{1,3}(\.\d{1,3}){3}/32", f"-s {new_ip_with_cidr}", line)
            updated_lines.append(updated_line)
            input_line_updated = True
        elif forward_line_identifier in line:
            updated_line = re.sub(r"-s\s+\d{1,3}(\.\d{1,3}){3}/32", f"-s {new_ip_with_cidr}", line)
            updated_lines.append(updated_line)
            forward_line_updated = True
        else:
            updated_lines.append(line)

    # Write the updated lines back to the before.rules file
    with open(before_rules_path, "w") as file:
        file.writelines(updated_lines)

    # Restart the ufw service to apply the changes
    subprocess.run(["sudo", "ufw", "reload"], check=True)
    
    # Log the updates
    print(f"Updated before.rules with IP {current_ip}/32.")
    if input_line_updated:
        print(f"Updated input line: {input_line_identifier} -s {new_ip_with_cidr}")
    if forward_line_updated:
        print(f"Updated forward line: {forward_line_identifier} -s {new_ip_with_cidr}")


def main():
    import os, configparser
    from datetime import timezone, timedelta

    # Get script parent dir
    parent_dir = os.path.dirname(os.path.abspath(__file__))

    # Timezone settings
    timezone_offset = +10.0  # Pacific Standard Time (UTC−08:00)
    tzinfo = timezone(timedelta(hours=timezone_offset))
    tz_string_format = "%a %b %d at %H:%M"

    # Init configparser
    config = configparser.ConfigParser()
    config.read(f'{parent_dir}/config.ini')
    default_config = config['firewall']

    LOG_FILE = default_config.get("log_file")
    current_ip = get_current_ip("lan.ddnsgeek.com")
    last_ip = get_last_ip(default_config)

    update_firewall_rules(current_ip, last_ip, default_config, LOG_FILE, tzinfo, tz_string_format, parent_dir)

    # Call the new function to update before.rules
    update_before_rules(current_ip, f'{parent_dir}/config.ini')
    
if __name__ == "__main__":
    main()
