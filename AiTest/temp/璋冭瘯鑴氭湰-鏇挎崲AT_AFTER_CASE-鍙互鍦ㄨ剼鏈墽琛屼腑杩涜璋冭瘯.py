#-*-coding:utf-8-*-
while True:
    str = raw_input("Debug Script:")
    if str == 'exit':
        break
    else:
        print "Script is : ", str
    try:
        exec(str)
    except Exception,e:
        print e
    finally:
        print '>>>>>'
    
    
    
