#!/usr/bin/env python

from gnuradio import gr;
from scapy.utils import PcapWriter
from scapy.layers import l2
import pmt, sys, bitarray, array

class pcap_write(gr.sync_block):
    def __init__(self,f):
        gr.sync_block.__init__(self,"pcap_write",[],[])
        self.message_port_register_in(pmt.intern("pdus"));
        self.set_msg_handler(pmt.intern("pdus"), self.handler);
        self.f = f

    def start(self):
        self.pcap = PcapWriter(self.f, append=True, sync=True)   

    def stop(self):
        pass
   
    def handler(self, pdu):
        ba = bitarray.bitarray();
        meta = pmt.car(pdu)
        x = pmt.to_python(pmt.cdr(pdu))
        z = l2.Ether(x.tostring())
        self.pcap.write(z);
    
    def work(self, input_items, output_items):
        pass



