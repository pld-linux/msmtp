Summary:	SMTP "plugin" for MUAs
Name:		msmtp
Version:	0.3.0
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	08d74918c252a540a640c27729e0cd9c
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
msmtp is a simple program that works as an "SMTP plugin" for Mutt and
probably other MUAs (mail user agents). It forwards mails to an SMTP
server (for example at a free mail provider) which does the delivery.
Features include:
- SMTP AUTH methods PLAIN, LOGIN and CRAM-MD5
- TLS encrypted connections
- IPv6 support
- robustness
- detailed error messages if something goes wrong (including the full
  answer of the SMTP server)
- sendmail compatible exit codes (which most MUAs understand). Simply
  tell your MUA to call msmtp instead of /usr/sbin/sendmail (with Mutt
  that's just one additional line in the config file).

%prep
%setup -q

%build
%{__make} \
        CC="%{__cc}" \
        CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

install msmtp $RPM_BUILD_ROOT%{_bindir}/msmtp
install msmtp.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README THANKS
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/msmtp*
