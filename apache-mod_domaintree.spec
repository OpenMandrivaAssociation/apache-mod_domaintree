#Module-Specific definitions
%define mod_name mod_domaintree
%define mod_conf A60_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mass virtual hosting module mapping host names to a directory tree
Name:		apache-%{mod_name}
Version:	1.6
Release:	%mkrel 8
Group:		System/Servers
License:	Apache License
URL:		http://dev.iworks.at/mod_domaintree/
Source0:	http://dev.iworks.at/mod_domaintree/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.4
Requires(pre):	apache >= 2.2.4
Requires:	apache-conf >= 2.2.4
Requires:	apache >= 2.2.4
BuildRequires:  apache-devel >= 2.2.4
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mass virtual hosting module mapping host names to a directory tree.

%prep

%setup -q -n %{mod_name}

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type d -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

cp %{SOURCE1} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_sbindir}/apxs -c mod_domaintree.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}/var/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}/var/www/html/addon-modules/%{name}-%{version}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog LICENSE.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
/var/www/html/addon-modules/*
