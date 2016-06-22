#!/usr/bin/env python

from gnuradio import gr;
from scapy.utils import PcapWriter
from scapy.layers import l2
import pmt

class pcap_write(gr.sync_block):
    def __init__(self,f,append=True):
        gr.sync_block.__init__(self,"pcap_write",[],[])
        self.message_port_register_in(pmt.intern("pdus"));
        self.set_msg_handler(pmt.intern("pdus"), self.handler);
        self.f = f
        self.append = append

    def start(self):
        self.pcap = PcapWriter(self.f, append=self.append, sync=True)   

    def stop(self):
        pass
   
    def handler(self, pdu):
        meta = pmt.to_python(pmt.car(pdu))
        x = pmt.to_python(pmt.cdr(pdu))
        z = l2.Raw(x.tostring())
        if(meta.has_key("timestamp")):
            z.time = meta["timestamp"]
        self.pcap.write(z);
    
    def work(self, input_items, output_items):
        pass



