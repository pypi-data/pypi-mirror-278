#!/bin/bash

ServiceName="indycare_service"
permissions=""
provider="Neuromeka-STEP-PC"
desc="$ServiceName service."

base_dir="/home/user/release/IndyDeployment/IndyCAREReport"
service_dir="$base_dir/$ServiceName"

# > Installing screen command < #
echo ":: screen command check ::"
found_screen=$(which screen)

if [ -z "$found_screen" ] ;
then
    echo "Not found screen command. Now trying to install screen package."
    sudo apt install screen -y
else
    echo "Found screen command."
fi

mkdir -p $service_dir
cd $service_dir

# > Register < #
echo '#!/bin/bash
ServiceName='"$ServiceName"'

# Assuming script is run with sudo, no password prompt
sudo touch /etc/sudoers.d/user
'"$permissions"'

sudo cp '$service_dir'/'$ServiceName\_script' /etc/
sudo cp '$service_dir'/'$ServiceName' /etc/init.d/
sudo chmod 775 /etc/init.d/$ServiceName
sudo chmod 775 /etc/$ServiceName\_script

sudo update-rc.d -f $ServiceName remove
sudo update-rc.d $ServiceName defaults
sudo service $ServiceName restart

echo -e '"\n"'
' > $service_dir/register_service.sh


# > Deregister < #
echo '#!/bin/bash
ServiceName='"$ServiceName"'

# Assuming script is run with sudo, no password prompt
sudo service $ServiceName stop
sudo update-rc.d -f $ServiceName remove
sudo rm /etc/$ServiceName\_script
sudo rm /etc/init.d/$ServiceName
echo -e '"\n"'
' > $service_dir/deregister_service.sh

# > Service < #
echo '#!/bin/bash

### BEGIN INIT INFO
# Provides: '"$provider"'
# Required-Start: $network
# Required-Stop: $network
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: '"$desc"'
### END INIT INFO

ServiceName='"$ServiceName"'

status() {
	ps -ef | grep "/bin/bash /etc/$ServiceName\_script"
	tail -f /tmp/$ServiceName.log
}

start() {
	echo "Started $ServiceName\_script service"
	/usr/bin/screen -dmS $ServiceName bash -c "sudo /etc/$ServiceName\_script > /tmp/$ServiceName.log 2>&1"
	echo -e '"\n"'
}

stop() {
	ps -ef | grep "/bin/bash /etc/$ServiceName\_script" | awk '"'"'{print $2}'"'"' | sudo xargs kill -9
	echo "Stopped $ServiceName\_script service"
	echo -e '"\n"'
}

case $1 in
	start)
		start;;
	stop)
		stop;;
	restart)
		stop
		start;;
	status)
		status;;
esac
exit 0
' > $service_dir/$ServiceName


# > Service Script < #
echo '#!/bin/bash

python3 /home/user/release/IndyDeployment/IndyCAREReport/IndyCAREReport.py
' > $service_dir/$ServiceName\_script

chmod -R 775 $service_dir/*

chmod +x $service_dir/register_service.sh
$service_dir/register_service.sh

echo Finish.
