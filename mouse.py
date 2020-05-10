import struct, os
 
file = open( "/dev/input/mice", "rb" );
 
point_x = 0;
point_y = 0;
 
class Point:
    x = 0.0
    y = 0.0
 
def getMouseEvent():
    buf = file.read(3); 
    x,y = struct.unpack( "bb", buf[1:] );
    dis = Point();
    dis.x = x;
    dis.y = y;
    return dis;
 
while( 1 ):
    dis = getMouseEvent();
    point_x = point_x + dis.x;
    point_y = point_y + dis.y;
    print ("%d  %d" % (point_x, point_y));
file.close();