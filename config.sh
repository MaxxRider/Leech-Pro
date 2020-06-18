#!/bin/bash

if [[ -n $RCLONE_CONFIG && -n $DESTINATION_FOLDER ]]; then
	echo "Rclone config detected"
	echo -e "[DRIVE]\n$RCLONE_CONFIG" > rclone.conf
fi
