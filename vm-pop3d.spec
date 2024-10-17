%define oldname	gnu-pop3d

Name:		vm-pop3d
Version:	1.1.6
Release:	11
License:	GPLv2+
Group:		Networking/Other
Source0:	ftp://ftp.nodomainname.net/pub/gnu-pop3d/current/%{name}-%{version}.tar.bz2
Source1:	%{name}-xinetd.bz2
Patch0:		%{name}-popbsmtp.patch.bz2
Patch1:		%{name}-1.1.6-headerfix.patch.bz2
Patch2:		%{name}-pamd.patch
Patch3:		vm-pop3d-1.1.6-fix-buffer-overflow.patch
Summary:	Virtualmail-pop3d, fork of gnu-pop3d
URL:		https://www.reedmedia.net/software/virtualmail-pop3d/
Requires:	xinetd
Obsoletes:	ids-pop3d %{oldname}
Provides :	ids-pop3d %{oldname}
Requires(post):	rpm-helper
Requires(preun):rpm-helper
BuildRequires:	pam-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The GNU POP3 server, or GNU POP. This is a small, fast, efficient POP3 server.
It aims to be fully RFC compliant. Please read the file README.rpm in this
packages doc directory for more information.

%prep
%setup -q
%patch0 -p0 -b .popbsmtp~
%patch1 -p1 -b .headerfix~
%patch2 -p1 -b .pamd~
%patch3 -p1 -b .overflow~

%build
%configure	--enable-pam
%make CFLAGS="%{optflags}" LDFLAGS="%{ldflags}"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
install -D -m644 %{name}.pamd $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/%{name}
#install -D -m755 %{name}.init $RPM_BUILD_ROOT%{_initrddir}/%{name} 
bzcat %{SOURCE1} > %{name}-xinetd; install -D -m644 %{name}-xinetd $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
%doc README AUTHORS TODO INSTALL RFC*
%{_sbindir}/*
%{_mandir}/man8/*
#%config %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%config(noreplace) %{_sysconfdir}/pam.d/%{name}


%changelog
* Sun Dec 05 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.1.6-10mdv2011.0
+ Revision: 609582
- link with %%{ldflags}
- cosmetics
- fix buffer overflow (mdv#55653)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 1.1.6-8mdv2009.0
+ Revision: 255577
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Nov 21 2007 Nicolas Vigier <nvigier@mandriva.com> 1.1.6-6mdv2008.1
+ Revision: 111044
- fix prereq
- fix pamd config again
- fix pam config (#32317)
- import vm-pop3d


* Mon Aug 01 2005 Marcel Pol <mpol@mandriva.org> 1.1.6-4mdk
- P1: fix malformed Message-ID: header (bug #8971)

* Sat Oct 16 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.1.6-3mdk
- rebuild

* Mon Aug 04 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.1.6-2mdk
- rebuild
- drop /sbin/chkconfig from PreReq

* Sat Jan 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.1.6-1mdk
- gnu-pop3d is no longer maintaned, vm-pop3d is a fork of gnu-pop3d
- Use correct optimize flags
- Cleanups
- Updated Patch #0
- Run from xinetd instead of running as a daemon

* Fri Jan 17 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.9.8-7mdk
- rebuild

* Thu Feb 14 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.9.8-6mdk
- Patch to log IP for pop-before-smtp from Ryan (from Todd)

* Thu Jul 19 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.9.8-5mdk
- rebuild

* Wed Jan 10 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.9.8-4mdk
- rebuild

* Fri Sep 01 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.9.8-3mdk
- BM
- macros

* Thu Apr 27 2000 Lenny Cartier <lenny@mandrakesoft.com> 0.9.8-2mdk 
- fix group

* Wed Feb 16 2000 Lenny Cartier <lenny@mandrakesoft.com>
- v0.9.8
- used srpm provided by Geoffrey Lee <snailtalk@linux-mandrake.com>

* Wed Feb 04 2000 Geoffrey Lee <snailtalk@linux-mandrake.com>
- forgot to handle bz2 last time...
 
* Wed Feb 02 2000 Geoffrey Lee <snailtalk@linux-mandrake.com>
- Rebuilt for Mandrake
 
* Wed Mar 31 1999 Edgard Castro <castro@usmatrix.net>
- Added support to Linux PAM library
- Using a new init script
- Major revamp on spec file
- Discarding all symbols from the executable
- Changed CFLAGS to use $RPM_OPT_FLAGS
- Using chkconfig to create init entriess
- Added default attributes when installing files 
