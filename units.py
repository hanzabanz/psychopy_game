__author__ = 'hannah'
def pos_conv(window, a):
    return (window/4)*a

def unit_conv(window_size, size):
    return window_size/(2*(1/size))

def pix_conv(window_w, window_h, w, h, a, b):
    a_sign = a/abs(a)
    b_sign = b/abs(b)
    left = (pos_conv(window_w, a) - unit_conv(window_w, w)) * -a_sign
    right = (pos_conv(window_w, a) + unit_conv(window_w, w)) * a_sign
    top = (pos_conv(window_h, b) + unit_conv(window_h, h)) * b_sign
    bottom = (pos_conv(window_h, b) - unit_conv(window_h, h)) * -b_sign
    print "Window %d %d   Width %d    Height %d    A %d   B %d" %(window_w, window_h, w, h, a, b)
    print "Left %d   Right %d   Top %d   Bottom %d" %(left, right, top, bottom)
    return (left, right, top, bottom)