
# Version
* The schematic was originally created in KiCad 9.0.7, on 2026-04-26
* At the time, KiCad 10.0.0 was having issues

# Project Library
* All symbols are kept in the project library

# Workflow for KiCad

## Method One uses *sshfs*
* Use a temporary mountpoint on the Debian desktop computer
<br>to mount the remote project directory
```bash
REMOTE="cygnus:prgms/Python/jumpack-01"
MNTPOINT="~/Projects/jumpack"
mkdir -p "$MNTPOINT"
sshfs "$REMOTE" "$MNTPOINT"
```
* Edit the schematic in KiCad on Debian
* Unmount and remove the temporary mountpoint
```bash
# umount usually works, and fuermount3 -u always works
umount "$MNTPOINT"  ||  fusermount3 -u $MNTPOINT"
```

## Method Two uses *git*
* Clone the whole project repo to the Debian desktop computer
* Edit the KiCad schematic
* Commit and push the changes to github

