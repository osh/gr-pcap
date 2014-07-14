#!/usr/bin/env python

from gnuradio import gr;
import pmt, sys, bitarray, array, scapy
from scapy.utils import PcapWriter

class pcap_writer(gr.sync_block):
    def __init__(self,f):
        gr.sync_block.__init__(self,"pcap_writer",[],[])
        self.message_port_register_in(pmt.intern("pdus"));
        self.set_msg_handler(pmt.intern("pdus"), self.handler);
        self.f = f

    def start(self):
        self.pcap = PcapWriter(self.f, append=True, sync=True)   

    def stop(self):
        pass
   
    def handler(self, msg):
        ba = bitarray.bitarray();          
        s = array.array('B', pmt.u8vector_elements(pmt.cdr(msg))).tostring()
        z = scapy.layers.l2.Ether(s)
        self.pcap.write(z);
    
    def work(self, input_items, output_items):
        pass



