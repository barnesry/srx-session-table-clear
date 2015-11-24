#!/usr/bin/python

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.factory import loadyaml
from pprint import pprint as pp

# constants
t1 = 'add-global-address-book-template.j2'

# load our globals
globals().update( loadyaml('flowsession.yml'))

dev = Device('192.168.56.107', user='root',password='junos123')

# bind the config to the Device
dev.bind( cu=Config, sessions=SessionTable )

# and open a connection to the device
dev.open()

# and get our session table
dev.sessions.get()

pp(dev.sessions.items())

# now we'll look for a specific flow in the flow table
for s in dev.sessions:
    if dev.sessions.keys():
        if s.session_direction == "Out" and s.destination_address == '192.168.56.254' and s.session_protocol == 'udp':
            block_src = {'Address': s.source_address}

            # and clear the offending flow
            print("Clearing offending flow : Dst:{} Src:{} Dst_Port:{} Prot:{}".format(s.destination_address, s.source_address, s.destination_port, s.session_protocol))
            clearflow = dev.rpc.clear_flow_session(destination_prefix=s.destination_address, source_prefix=s.source_address, destination_port=s.destination_port, protocol=s.session_protocol)
            # load the Jinja template
            rsp = dev.cu.load( template_path=t1, template_vars=block_src, format="text")

            # load the diff
            print "Diffs..."
            print dev.cu.diff()

            # commit the config
            print "Committing now..."
            try :
                dev.cu.commit()
            except:
                print "Commit Failed"




# disconnect
dev.close()
