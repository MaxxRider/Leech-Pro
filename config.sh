#!/bin/bash

if [[ -n $RCLONE_CONFIG && -n $RCLONE_DESTINATION ]]; then
	echo "Rclone config detected"
	echo -e "[DRIVE]\n$RCLONE_CONFIG" > rclone.conf
