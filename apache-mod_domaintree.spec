#Module-Specific definitions
%define mod_name mod_domaintree
%define mod_conf A60_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mass virtual hosting module mapping host names to a directory tree
Name:		apache-%{mod_name}
Version:	1.6
Release:	12
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

%{_bindir}/apxs -c mod_domaintree.c

%install

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

%files
%doc ChangeLog LICENSE.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
/var/www/html/addon-modules/*


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.6-11mdv2012.0
+ Revision: 772622
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.6-10
+ Revision: 678308
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.6-9mdv2011.0
+ Revision: 587966
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.6-8mdv2010.1
+ Revision: 516094
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.6-7mdv2010.0
+ Revision: 406578
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1.6-6mdv2009.1
+ Revision: 325696
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.6-5mdv2009.0
+ Revision: 234940
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.6-4mdv2009.0
+ Revision: 215573
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1.6-3mdv2008.1
+ Revision: 181721
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.6-2mdv2008.0
+ Revision: 82564
- rebuild

* Mon May 07 2007 Oden Eriksson <oeriksson@mandriva.com> 1.6-1mdv2008.0
+ Revision: 24256
- 1.6


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.5-2mdv2007.1
+ Revision: 140670
- rebuild

* Sun Dec 10 2006 Oden Eriksson <oeriksson@mandriva.com> 1.5-1mdv2007.1
+ Revision: 94497
- 1.5
- bunzipped and fixed the config file

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4-2mdv2007.0
+ Revision: 79412
- Import apache-mod_domaintree

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4-2mdv2007.0
- rebuild

* Mon Apr 24 2006 Oden Eriksson <oeriksson@mandriva.com> 1.4-1mdk
- initial Mandriva package

