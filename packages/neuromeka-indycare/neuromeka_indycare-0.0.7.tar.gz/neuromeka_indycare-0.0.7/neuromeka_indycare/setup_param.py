import argparse
import subprocess
import os
import yaml
from collections import OrderedDict

package_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(package_dir, 'indycare_utils', 'config.yml')
ngrok_file_path = os.path.join(package_dir, 'setup', 'ngrok-v3-stable-linux-386.tgz')
ngrok_executable_path = '/usr/bin/ngrok'
install_script_path = os.path.join(package_dir, 'daliworks_software', 'install.sh')
create_service_path = os.path.join(package_dir, 'create_service.sh')


class CustomDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(CustomDumper, self).increase_indent(flow, indentless)

    def represent_list(self, data):
        if len(data) == 1:
            return self.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)
        return super(CustomDumper, self).represent_list(data)

    def represent_scalar(self, tag, value, style=None):
        if tag == 'tag:yaml.org,2002:str' and ':' in value:
            style = '"'
        return super(CustomDumper, self).represent_scalar(tag, value, style)


CustomDumper.add_representer(list, CustomDumper.represent_list)


def run_command(command, description=""):
    print(f"Running: {description}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(f"Error message: {result.stderr}")
    else:
        print(f"Success: {description}")
    return result.returncode == 0


def create_ngrok_config(ngrok_token, config_file):
    config_content = f"authtoken: {ngrok_token}\nversion: \"2\"\n"
    with open(config_file, 'w') as file:
        file.write(config_content)
    print(f"ngrok configuration written to {config_file}")


def main():
    parser = argparse.ArgumentParser(description="Configure IndyCare settings.")
    parser.add_argument('--passwd', required=True, help='Password for sudo commands')
    parser.add_argument('--device_id', required=True, help='Device ID registered with Daliworks')
    parser.add_argument('--ngrok_token', required=True, help='Ngrok token')

    args = parser.parse_args()

    passwd = args.passwd
    device_id = args.device_id
    ngrok_token = args.ngrok_token

    robot_sn = input("Enter robot_sn: ")
    camera_choice = input("Enter Camera options (1: None/USB Camera, 2: C200/C200E, 3: C300): ")

    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)

    config['mqtt_device_id'] = device_id
    config['robot_sn'] = robot_sn

    if camera_choice == "1":  # None or USB Camera
        config['rtsp'] = False
        config['rtsp_url'] = "rtsp://admin:nrmk2013@192.168.20.5/stream1"
        config['rtsp_streaming_fps'] = 20
    elif camera_choice == "2":  # C200 or C200E
        config['rtsp'] = True
        rtsp_id = input("Enter RTSP ID: ")
        rtsp_pw = input("Enter RTSP Password: ")
        rtsp_ip = input("Enter RTSP IP: ")
        config['rtsp_url'] = f"rtsp://{rtsp_id}:{rtsp_pw}@{rtsp_ip}/stream1"
        config['rtsp_streaming_fps'] = 20
    elif camera_choice == "3":  # C300
        config['rtsp'] = True
        rtsp_pw = input("Enter RTSP Password: ")
        rtsp_ip = input("Enter RTSP IP: ")
        config['rtsp_url'] = f"rtsp://admin:{rtsp_pw}@{rtsp_ip}/stream1"
        config['rtsp_streaming_fps'] = 10
    else:
        print("Invalid camera choice.")
        return

    with open(config_file_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False, sort_keys=False, Dumper=CustomDumper)

    # Disable lsb_release if exists
    file = '/usr/bin/lsb_release'
    if os.path.exists(file):
        run_command(f'sed -i "s/^#!/##!/" {file}', "Disable lsb_release")

    # Disable old IndyCare gstream
    files_to_backup = [
        '/usr/sbin/nrmkscm.sh',
        '/usr/sbin/nrmkbox',
        '/usr/sbin/gstvideo',
        '/usr/bin/nrmkscm.sh',
        '/usr/bin/nrmkbox',
        '/usr/bin/gstvideo'
    ]

    for file in files_to_backup:
        if os.path.exists(file):
            run_command(f'echo {passwd} | sudo -S -k mv {file} {file}.bk', f"Backup {file}")
        else:
            print(f"File not found, skipping: {file}")

    # Remove existing ngrok if exists
    if os.path.exists(ngrok_executable_path):
        run_command(f'echo {passwd} | sudo -S -k rm {ngrok_executable_path}', "Remove existing ngrok")

    ngrok_config_dir = "/root/.config/ngrok"
    ngrok_config_file = f"{ngrok_config_dir}/ngrok.yml"

    # Install ngrok
    run_command(f'echo {passwd} | sudo -S -k tar xvzf {ngrok_file_path} -C /usr/bin', "Extract ngrok")
    run_command(f'echo {passwd} | sudo -S -k chmod +x /usr/bin/ngrok', "Change permissions for ngrok")

    run_command(f'echo {passwd} | sudo -S -k mkdir -p {ngrok_config_dir}', "Create ngrok config directory")

    create_ngrok_config(ngrok_token, ngrok_config_file)

    run_command(f'echo {passwd} | sudo -S -k NGROK_CONFIG={ngrok_config_file} /usr/bin/ngrok authtoken {ngrok_token}',
                "Set ngrok authtoken")
    # run_command(f'echo {passwd} | sudo -S -k /usr/bin/ngrok authtoken {ngrok_token}', "Set ngrok authtoken")


    # Convert config to unix file
    run_command(f'echo {passwd} | sudo -S -k apt-get install dos2unix', "Install dos2unix")
    run_command(f'echo {passwd} | sudo -S -k dos2unix {config_file_path}', "Convert config.yml to Unix format")

    # Install Daliworks software
    daliworks_files = [
        'lt',
        'mjpg_streamer',
        'auth.sh',
        'ffmpeg',
        'domain.on.sh',
        'service.on.sh',
        'service_cam.on.sh',
        'service_cam_rtsp.on.sh',
        'kill_process.sh',
        'install.sh'
    ]

    for file in daliworks_files:
        file_path = os.path.join(package_dir, 'daliworks_software', file)
        if os.path.exists(file_path):
            run_command(f'echo {passwd} | sudo -S -k chmod +x {file_path}', f"Set execute permission for {file_path}")
        else:
            print(f"File not found, skipping: {file_path}")

    if os.path.exists(install_script_path):
        run_command(f'echo {passwd} | sudo -S -k chmod +x {install_script_path}',
                    "Set execute permission for install script")
        run_command(f'echo {passwd} | sudo -S -k dos2unix {install_script_path}', "Convert install.sh to Unix format")
        run_command(f'echo {passwd} | sudo -S -k {install_script_path}', "Run Daliworks install script")
    else:
        print(f"Install script not found: {install_script_path}")


    print('Registering Service')

    if os.path.exists(create_service_path):
        run_command(f'echo {passwd} | sudo -S -k chmod +x {create_service_path}',
                    "Set execute permission for create_service.sh")
        run_command(f'echo {passwd} | sudo -S -k dos2unix {create_service_path}', "Convert create_service.sh to Unix format")
        run_command(f'echo {passwd} | sudo -S -k {create_service_path}', "Register IndyCARE Service")
    else:
        print(f"create_service.sh not found at {create_service_path}")


    print('Installation completed. Please reboot the computer.')


if __name__ == "__main__":
    main()
