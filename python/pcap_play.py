#!/usr/bin/env python

from gnuradio import gr;
import pmt, time, numpy, threading
from scapy.utils import PcapReader

class pcap_play(gr.sync_block):
    def __init__(self,f, time_scale=1.0):
        gr.sync_block.__init__(self,"pcap_play",[],[])
        self.message_port_register_out(pmt.intern("pdus"));
        self.f = f
        self.done = False
        self.lasttime = 0;
        self.time_scale = time_scale

    def run(self):
        while True:
            self.pcap = PcapReader(self.f)   
            self.lasttime = 0;
            for p in self.pcap:
                if(not (self.lasttime == 0)):
                    diff = (p.time - self.lasttime)
                    time.sleep(diff*self.time_scale);
                self.lasttime = p.time
                if(self.done):
                    return
                
                v = pmt.to_pmt(numpy.fromstring(str(p), dtype=numpy.uint8))
                meta = pmt.make_dict();
                self.message_port_pub(pmt.intern("pdus"), pmt.cons(meta, v));
        
    def start(self):
        self.thread = threading.Thread(target=self.run);
        self.thread.start()

    def stop(self):
        self.done = True;
        self.thread.join()
   
    def work(self, input_items, output_items):
        assert(False)


