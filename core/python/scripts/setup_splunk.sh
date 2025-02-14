#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status
set -x  # Print commands and their arguments as they are executed

# Variables
SPLUNK_PACKAGE_URL=${1:-"https://download.splunk.com/products/splunk/releases/9.0.4/linux/splunk-9.0.4-linux-x86_64.tgz"}
SPLUNK_HOME="/opt/splunk"
SPLUNK_USER="splunk"
SPLUNK_GROUP="splunk"

# Functions
log_message() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1"
}

# Step 1: Update System and Install Dependencies
log_message "Updating system and installing dependencies..."
yum update -y
yum install -y wget tar

# Step 2: Create Splunk User and Group
log_message "Creating Splunk user and group..."
if ! id -u $SPLUNK_USER &>/dev/null; then
    groupadd $SPLUNK_GROUP
    useradd -m -g $SPLUNK_GROUP $SPLUNK_USER
    log_message "Splunk user and group created."
else
    log_message "Splunk user and group already exist."
fi

# Step 3: Download Splunk
log_message "Downloading Splunk from $SPLUNK_PACKAGE_URL..."
wget -O /tmp/splunk.tgz $SPLUNK_PACKAGE_URL

# Step 4: Extract and Install Splunk
log_message "Installing Splunk to $SPLUNK_HOME..."
mkdir -p $SPLUNK_HOME
tar -xzf /tmp/splunk.tgz -C $SPLUNK_HOME --strip-components=1
chown -R $SPLUNK_USER:$SPLUNK_GROUP $SPLUNK_HOME

# Step 5: Enable Splunk as a Service
log_message "Setting up Splunk as a systemd service..."
$SPLUNK_HOME/bin/splunk enable boot-start --accept-license --answer-yes --no-prompt -user $SPLUNK_USER

# Step 6: Start Splunk
log_message "Starting Splunk service..."
systemctl start Splunkd.service
systemctl enable Splunkd.service

# Step 7: Configure Splunk (Optional)
log_message "Performing initial configuration for Splunk..."
cat <<EOF > $SPLUNK_HOME/etc/system/local/user-seed.conf
[users]
admin = changeme
EOF

# Step 8: Verify Installation
log_message "Verifying Splunk installation..."
if $SPLUNK_HOME/bin/splunk status | grep "splunkd is running"; then
    log_message "Splunk is successfully installed and running."
else
    log_message "Splunk installation failed. Check logs for details."
    exit 1
fi

# Clean Up
log_message "Cleaning up temporary files..."
rm -f /tmp/splunk.tgz

log_message "Splunk setup is complete!"
