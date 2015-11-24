Automation Training

Takes static files as input, binds a Config and SessionTable object to an srx Device.
Queries the associated session table looking for specific flows

If matching flow, clear the session table, and insert an address entry to block source.

Tested against vSRX on Macbook Pro running in VirtualBox with a local address of 192.168.56.107.
