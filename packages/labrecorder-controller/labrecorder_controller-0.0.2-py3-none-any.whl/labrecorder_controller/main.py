import socket
import logging
import sys

logger = logging.getLogger()

class labrecrcs():
    def __init__(self,
                 ip = "localhost",
                 port = 22345):
        logger.debug("ip: %s, port: %s"%(str(ip), str(port)))
        self.s = socket.create_connection((ip, port))

    def send(self, cmd):
        self.s.sendall(cmd)
    
    def select_all(self):
        self.s.sendall(b"select all\n")
        logger.debug("'select all' was sent.")

    def select_none(self):
        self.s.sendall(b"select none\n")
        logger.debug("'select none' was sent.")
    
    def start(self):
        self.s.sendall(b"start\n")
        logger.debug("'start' was sent.")
        
    def stop(self):
        self.s.sendall(b"stop\n")
        logger.debug("'stop' was sent.")
        
    def update(self):
        self.s.sendall(b"update\n")
        logger.debug("'update' was sent.")
    
    def filename(self,
                 root = None,
                 template = None,
                 task = None,
                 run = None,
                 participant = None,
                 session = None,
                 acquisition = None,
                 modality = None):
        cmd = "filename"
        
        if root is not None:
            cmd += " {root:%s}"%root
        
        if template is not None:
            cmd += " {template:%s}"%template

        if task is not None:
            cmd += " {task:%s}"%task
            
        if run is not None:
            if type(run) != int:
                raise ValueError("value for 'run' should have type of int")
            cmd += " {run:%d}"%run
            
        if participant is not None:
            cmd += " {participant:%s}"%participant
        
        if session is not None:
            cmd += " {session:%s}"%session
            
        if acquisition is not None:
            cmd += " {acquisition:%s}"%acquisition
            
        if modality is not None:
            cmd += " {modality:%s}"%modality
        
        self.s.sendall(bytes(cmd + "\n", encoding='utf-8'))
        logger.debug("'%s' was sent."%str(cmd))


if __name__ == "__main__":

    format = '%(asctime)s [%(levelname)s] %(module)s.%(funcName)s %(message)s'

    stdout_handler = logging.StreamHandler(stream = sys.stdout)
    stdout_handler.setFormatter(logging.Formatter(format))
    stdout_handler.setLevel(logging.DEBUG)

    root_logger = logging.getLogger(None)
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stdout_handler)

    rcs = labrecrcs(ip = "172.20.99.40")
    rcs.update()
    rcs.select_all()
    rcs.filename(root = "root",
                 template="sub-%p\ses-%s\%m\sub-%p_ses-%s_task-%b_run-%n_%m.xdf",
                 task = "task",
                 run = 2,
                 participant = "participant",
                 session = "session",
                 acquisition = "acquisition",
                 modality = "modality")
