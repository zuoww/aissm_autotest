#-*-coding:utf-8-*-
#run before each case
print '...run before case begin...'
#trim code switch  trim=0  hold=1
SectorControlRunWeb=1
SectorControlRunData=0

#code start
##print getConfig('path')
##list1=[getConfig('path')]
##print list1
#执行用例前获取执行参数并记录到DataResult

tempPath=getConfig('path')+'temp\\'+getConfig('curCaseFile')
if SectorControlRunWeb==0 or SectorControlRunData==0:
    print 'run trim code'
    f=open(tempPath,'rb')
    FileDataList=f.readlines()
    f.close()
    NewFileData=''
    if SectorControlRunWeb==0:
        cnt=0
        for i in range(0,len(FileDataList)):
            if '#--RunWeb--#' in FileDataList[i]:
                cnt+=1
            if cnt==1:
                FileDataList[i]=''
    if SectorControlRunData==0:
        cnt=0
        for i in range(0,len(FileDataList)):
            if '#--RunData--#' in FileDataList[i]:
                cnt+=1
            if cnt==1:
                FileDataList[i]=''
    f=open(tempPath,'wb')
    f.write(''.join(FileDataList))
    f.close()

print '...run  before case end...'




