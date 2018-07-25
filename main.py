import other_file

try:
    import requests
except Exception:
    print("requests not found")
    
try:
    from botocore.vendored import requests
except Exception:
    print("botocore not found")
    
try:
    import boto3
except Exception:
    print("boto3 not found")
    
    


def my_func():
    other_file.good_func()
  
if __name__ == '__main__':
    my_func()
    tdhdfgh
    
    #comment
    #comment
    #comment
