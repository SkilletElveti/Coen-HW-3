# Copyright 2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()



class Tutorial (object):
 
  def __init__ (self, connection):
    # Keep track of the connection
    self.connection = connection
    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Use this table to keep track of ethernet address
    self.mac_to_port = {}


  def resend_packet (self, packet_in, out_port):
    msg = of.ofp_packet_out()
    msg.data = packet_in
    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)
    # Send message to switch
    self.connection.send(msg)
    
  def act_like_hub (self, packet, packet_in):
    # Output to all ports
    self.resend_packet(packet_in, of.OFPP_ALL)


  def act_like_switch (self, packet, packet_in):
    if packet.src not in self.mac_to_port:
        self.mac_to_port[packet.src] = packet_in.in_port

    if packet.dst in self.mac_to_port:
        self.resend_packet(packet_in, self.mac_to_port[packet.dst])
    else:
        self.resend_packet(packet_in, of.OFPP_ALL)

  def _handle_PacketIn (self, event):
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp
    self.act_like_switch(packet, packet_in)


def launch ():
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Tutorial(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
