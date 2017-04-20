@echo off 

set planBatchId=1_20161211104357
set batchId=all

set eparchyCode=0471

if not "%1"=="" (java -classpath serverlib\ver_report.jar;serverlib\commons-collections-3.2.jar;serverlib\commons-configuration-1.5.jar;serverlib\commons-dbcp-1.2.2.jar;serverlib\commons-io-1.3.2.jar;serverlib\commons-jxpath-1.2.jar;serverlib\commons-lang-2.4.jar;serverlib\commons-logging-1.1.1.jar;serverlib\commons-pool-1.3.jar;serverlib\ibatis-2.3.4.726.jar;serverlib\log4j-1.2.12.jar;serverlib\mysql-connector-java-5.1.21-bin.jar;serverlib\ojdbc14.jar com.ailk.cuc.autotestbg.bootstrap.Bootstrap client %1 %2 %3) else (java -classpath serverlib\ver_report.jar;serverlib\commons-collections-3.2.jar;serverlib\commons-configuration-1.5.jar;serverlib\commons-dbcp-1.2.2.jar;serverlib\commons-io-1.3.2.jar;serverlib\commons-jxpath-1.2.jar;serverlib\commons-lang-2.4.jar;serverlib\commons-logging-1.1.1.jar;serverlib\commons-pool-1.3.jar;serverlib\ibatis-2.3.4.726.jar;serverlib\log4j-1.2.12.jar;serverlib\mysql-connector-java-5.1.21-bin.jar;serverlib\ojdbc14.jar com.ailk.cuc.autotestbg.bootstrap.Bootstrap client %planBatchId% %batchId% %eparchyCode%)

echo off
