from datetime import datetime
import os
import socket
import subprocess
import sys
import Queue
import threading

NUM_WORKERS = 8

SERVER_IP = socket.gethostbyname(socket.gethostname())
VLC_CMD = """
cd ../vlc && mm-link %s %s -- \
    ./vlc http://{}:%s/Manifest.mpd vlc://quit \
      --sout=file/ps:go.mpg 2>&1
""".format(SERVER_IP)

TRACE_DIRS = ['fcc-traces', 'hsdpa-traces', 'synthetic-traces']

remaining_work = Queue.Queue()

def worker_thread():
    while True:
        work = remaining_work.get()
        if isinstance(work, str) and work == "done":
            break
        trace, output, port = work 
        cmd = VLC_CMD % (trace, trace, port)
        with open(output, "w") as out: 
            print 'Starting', trace
            succ = subprocess.call(cmd, shell=True, stdout=out)
            if succ != 0:
                print "Test failed."
                return


def runTest(output_root):
    port = 0
    for dirname in TRACE_DIRS:
        output_dir = os.path.join(output_root, "output-" + dirname)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        count = 0
        for filename in os.listdir(dirname):
            count += 1
            trace = os.path.join("~", "experiments", dirname, filename)
            output = os.path.join(output_dir, filename + ".out")
            if not os.path.isfile(output):
                port = (port + 1) % 3
                remaining_work.put((trace, output, 8000 + port))
    
    for i in range(NUM_WORKERS):
        remaining_work.put("done")
    
    threads = [threading.Thread(target=worker_thread, name="worker-%s" % i) 
            for i in range(NUM_WORKERS)]
    for t in threads: t.start()
    for t in threads: t.join()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: python experiment.py output-dir"
    else:
        runTest(sys.argv[1])

