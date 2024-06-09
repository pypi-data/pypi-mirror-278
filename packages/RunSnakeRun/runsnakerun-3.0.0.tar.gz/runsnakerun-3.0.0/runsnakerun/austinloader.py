"""Loader for Austin Profiler

https://github.com/P403n1x87/austin

apt install austin
austin --help

"""

def parse_line(line: bytes):
    """Parse an incoming line from austin

    Unfortunately, Austin being GPL means we need to
    implement our own format parser for the output
    rather than just using the stats classes it 
    has already implemented...
    
    Format(s):


    
    
    """
