#!/usr/bin/env python

from gnuradio import gr;
import pmt, time, numpy
from scapy.utils import PcapReader

class pcap_range_source(gr.sync_block):
    def __init__(self,f,fs):
        gr.sync_block.__init__(self,"pcap_range_source",[],[])
        self.message_port_register_in(pmt.intern("pdus"));
        self.message_port_register_out(pmt.intern("pdus"));
        self.set_msg_handler(pmt.intern("pdus"), self.handler);
        self.f = f
        self.fs = fs

    def set_fs(self,fs):
        self.fs = fs


    def handler(self,msg):
        meta = pmt.car(msg)
        metapy = pmt.to_python(meta)
        t_start = metapy['start']/self.fs
        t_stop  = metapy['end']  /self.fs
        tag_times = []
        #print [t_start, t_stop]
        #print type(t_start)
        self.pcap = PcapReader(self.f)
        for i,p in enumerate(self.pcap):
            if p.time > t_start:
                if p.time > t_stop:
                    break;
                else:
                    samp_offset = int(self.fs*(p.time-t_start) )
                    k = "packet_id"
                    v = "%d"%(i)
                    tag_times.append( (samp_offset, k, v) )
        tags = pmt.to_pmt(tag_times)       
        meta = pmt.dict_add(meta, pmt.intern("tags"), tags)
        #print "tag times: ", tag_times
        self.message_port_pub(pmt.intern("pdus"), pmt.cons(meta, pmt.cdr(msg)));

    def work(self, input_items, output_items):
        assert(False)


