Logstash RPMs for RedHat Enterprise.

Repackage the monolithic jar into separate RPM packages:

    logstash-common  - contains .jar and shared dirs, etc.
    logstash-shipper - daemon to ship logs
    logstash-indexer - daemon to receive & process logs
    logstash-web     - web interface

Includes:

* spec file
* log4j configuration as separate file (no need to patch jar)
* init script

Simply dump the contents of the SOURCES and SPECS dirs in your build environment, grab the monolithic jar file [1] and put it in your SOURCES dir too and build like any other RPM.

[1] http://semicomplete.com/files/logstash/logstash-1.1.0.1-monolithic.jar
