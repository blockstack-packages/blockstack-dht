#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Blockstack
    ~~~~~
    copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
    copyright: (c) 2016 by Blockstack.org

    This file is part of Blockstack

    Blockstack is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Blockstack is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Blockstack. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
from ConfigParser import SafeConfigParser


# DHT
from twisted.internet import reactor
from kademlia.network import Server
from storage import BlockStorage, hostname_to_ip, STORAGE_TTL, DHT_SERVER_PORT, DEFAULT_DHT_SERVERS
from kademlia import log

DEFAULT_CONFIG_FILE = os.path.expanduser("~/.blockstack-server/dht.conf")

def parse_dht_servers( servers ):
   """
   Parse the serialized list of DHT servers
   raise on error
   """
   parsed_servers = []
   server_list = servers.split(",")
   for server in server_list:
      server_host, server_port = server.split(":")
      server_port = int(server_port)

      parsed_servers.append( (server_host, server_port) )

   return parsed_servers


def get_dht_opts( config_file=DEFAULT_CONFIG_FILE ):
   """
   Get our default DHT options from the config file.
   """

   global DHT_SERVER_PORT, DEFAULT_DHT_SERVERS

   defaults = {
      'port': str(DHT_SERVER_PORT),
      'servers': ",".join( ["%s:%s" % (host, port) for (host, port) in DEFAULT_DHT_SERVERS] )
   }

   parser = SafeConfigParser( defaults )
   parser.read( config_file )

   if parser.has_section('dht'):

      port = parser.get('dht', 'port')
      servers = parser.get('dht', 'servers')     # expect comma-separated list of host:port

      if disable is None:
         disable = True

      if port is None:
         port = DHT_SERVER_PORT

      if servers is None:
         servers = DEFAULT_DHT_SERVERS

      try:
         port = int(port)
      except:
         raise Exception("Invalid field value for dht.port: expected int")

      parsed_servers = []
      try:
         if type(servers) in [str, unicode]:
             parsed_servers = parse_dht_servers( servers )
         else:
             parsed_servers = servers

      except Exception, e:
         raise Exception("Invalid field value for dht.servers: expected 'HOST:PORT[,HOST:PORT...]'")

      dht_opts = {
         'port': port,
         'servers': ",".join( ["%s:%s" % (s[0], s[1]) for s in parsed_servers] )
      }

      return dht_opts

   else:

      # use defaults
      dht_opts = {
         'port': DHT_SERVER_PORT,
         'servers': ",".join( ["%s:%s" % (host, port) for (host, port) in DEFAULT_DHT_SERVERS] )
      }

      return dht_opts


def dht_run(config_file=DEFAULT_CONFIG_FILE):
    """
    Run the blockstackd RPC server, optionally in the foreground.
    """
    # start DHT server
    observer = log.FileLogObserver(sys.stdout, log.INFO)
    observer.start()

    dht_opts = get_dht_opts(config_file)
    dht_servers_str = dht_opts['servers']
    dht_port = dht_opts['port']
    dht_servers = parse_dht_servers( dht_servers_str )

    dht_server = Server(storage=BlockStorage())
    bootstrap_servers = hostname_to_ip(dht_servers)
    dht_server.bootstrap(bootstrap_servers)

    reactor.listenUDP( dht_port, dht_server.protocol )
    reactor.run()


