%define debug_package %{nil}

Name:           logstash
Version:        1.1.0.1
Release:        5%{?dist}
Summary:        logstash is a tool for managing events and logs.

Group:          System Environment/Daemons
License:        Apache 2.0
URL:            http://logstash.net
Source0:        http://semicomplete.com/files/logstash/%{name}-%{version}-monolithic.jar
Source1:        logstash-shipper.init
Source2:        logstash-shipper.conf
Source3:        log4j.properties
Source4:        logstash-shipper.sbin

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       java-openjdk
# Requires:       grok
# Requires:       java

Requires:       chkconfig initscripts

# disable jar repackaging
%define __os_install_post %{nil}

%description
logstash is a tool for managing events and logs. You can use it to collect logs, parse them, and store them for later use (like, for searching).

%package common
Summary: files common to all logstash daemons
Group:          System Environment/Daemons
%description common
Files common to all logstash dameons

%package indexer
Summary: Logstash indexer
Group: System Environment/Daemons
Requires: logstash-common
%description indexer
The logstash indexer service

%package shipper
Summary: Logstash shipper
Group: System Environment/Daemons
Requires: logstash-common
%description shipper
The logstash shipper service

%package web
Summary: Logstash web
Group: System Environment/Daemons
Requires: logstash-common
%description web
The logstash web interface

%install
rm -rf "${RPM_BUILD_ROOT}"

# /usr/share/logstash
%{__mkdir_p} "${RPM_BUILD_ROOT}/%{_datadir}/%{name}"

%define jarfile %{name}-%{version}-monolithic.jar

# the jar file
%{__install} -Dp -m0644 %{SOURCE0} "${RPM_BUILD_ROOT}%{_datadir}/%{name}/%{jarfile}"

# symlink to the jar file
ln -s %{jarfile} "${RPM_BUILD_ROOT}%{_datadir}/%{name}/%{name}.jar"

# the shipper init script
%{__install} -Dp -m0755 %{SOURCE1} ${RPM_BUILD_ROOT}%{_initrddir}/%{name}-shipper

# the shipper config file
%{__install} -Dp -m0644 %{SOURCE2} "${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/shipper.conf"

# the log4j config
%{__install} -Dp -m0644 %{SOURCE3} "${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/"

# /var/lib/logstash/shipper/tmp
%{__mkdir_p} "${RPM_BUILD_ROOT}/%{_var}/lib/%{name}/shipper/tmp"

# /var/lib/logstash/indexer/tmp
%{__mkdir_p} "${RPM_BUILD_ROOT}/%{_var}/lib/%{name}/indexer/tmp"

# /var/log/logstash
%{__mkdir_p} "${RPM_BUILD_ROOT}/%{_var}/log/%{name}"

# wrapper to launch jar file
%{__install} -Dp -m0755 %{SOURCE4} "${RPM_BUILD_ROOT}%{_sbindir}/%{name}-shipper"

%clean
rm -rf %{buildroot}

%pre common
LOGSTASH_SHELL=/sbin/nologin
/usr/sbin/groupadd -r logstash 2>/dev/null || :
/usr/sbin/useradd -c Logstash -r -s $LOGSTASH_SHELL -d /usr/share/%{name} -g logstash logstash 2>/dev/null || :

%post shipper
[ -x /sbin/chkconfig ] && chkconfig --add %{name}-shipper || :

%preun shipper
# remove service
if [ "$1" = 0 ]; then
  # on erase
  %{_sysconfdir}/init.d/%{name}-shipper stop > /dev/null 2>&1 || :
  [ -x /sbin/chkconfig ] && chkconfig --del %{name}-shipper
fi

%files common
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}
%{_datadir}/%{name}/*.jar
%dir %{_var}/lib/%{name}
%dir %attr(0755,logstash,logstash) %{_var}/log/%{name}

%files indexer
%attr(0755,logstash,logstash) %{_var}/lib/%{name}/indexer

%files shipper
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/shipper.conf
%config(noreplace) %{_sysconfdir}/%{name}/log4j.properties
%{_initrddir}/%{name}-shipper
%{_sbindir}/%{name}-shipper
%attr(0755,logstash,logstash) %{_var}/lib/%{name}/shipper

%files web

%changelog
* Tue Apr 17 2012 Robin Bowes <robin.bowes@yo61.com> 1.1.0.1-5
- use different tmp dirs for indexer + shippper packages
* Mon Apr 16 2012 Robin Bowes <robin.bowes@yo61.com> 1.1.0.1-4
- Set tmpdir to /var/lib/logstash to work with /tmp mounted noexec
* Fri Apr 13 2012 Robin Bowes <robin.bowes@yo61.com> 1.1.0.1-3
- Fix up init script and wrapper to daemonise correctly
* Thu Apr 12 2012 Robin Bowes <robin.bowes@yo61.com> 1.1.0.1-2
- Complete re-work into separate packages
* Thu Apr 05 2012 Robin Bowes <robin.bowes@yo61.com> 1.1.0.1-1
- Bump to v1.1.0.1
