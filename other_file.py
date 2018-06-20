def good_func():
    print "good func called correctly"
    return True
    
def bad_func():
    raise RuntimeException("bad func called")
