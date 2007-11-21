%define oldname	gnu-pop3d
%define name	vm-pop3d
%define version	1.1.6
%define release %mkrel 6

Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		Networking/Other
Source0:	ftp://ftp.nodomainname.net/pub/gnu-pop3d/current/%{name}-%{version}.tar.bz2
Source1:	%{name}-xinetd.bz2
Patch0:		%{name}-popbsmtp.patch.bz2
Patch1:		%{name}-1.1.6-headerfix.patch.bz2
Patch2:		%{name}-pamd.patch
Summary:	Virtualmail-pop3d, fork of gnu-pop3d
URL:		http://www.reedmedia.net/software/virtualmail-pop3d/
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
%patch -p0 -b .popbsmtp
%patch1 -p1 -b .headerfix
%patch2 -p1

%build
%configure	--enable-pam
%make CFLAGS="$RPM_OPT_FLAGS"

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

