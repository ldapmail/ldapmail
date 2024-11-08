#!/bin/bash
# Script to apply all ACL configuration files on container startup

if [ -d /tmp/acl ]; then
  for file in /tmp/acl/*.ldif; do
    if [ -f "$file" ]; then
      echo "Applying ACL configuration from $file..."
      ldapmodify -Y EXTERNAL -H ldapi:/// -f "$file"
      echo "ACL configuration from $file applied successfully."
    else
      echo "No .ldif files found in /tmp/acl."
    fi
  done
else
  echo "/tmp/acl directory not found."
fi