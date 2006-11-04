Summary:	SMTP "plugin" for MUAs
Summary(pl):	"Wtyczka" SMTP dla klientów pocztowych (MUA)
Name:		msmtp
Version:	1.4.7
Release:	2
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/msmtp/%{name}-%{version}.tar.bz2
# Source0-md5:	9c87a1f40e05dae4896622b56ec71b56
Patch0:		%{name}-home_etc.patch
Source1:	%{name}rc
URL:		http://msmtp.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gnutls-devel >= 1.2.0
BuildRequires:	gsasl-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
msmtp is a simple program that works as an "SMTP plugin" for Mutt and
probably other MUAs (mail user agents). It forwards mails to an SMTP
server (for example at a free mail provider) which does the delivery.
Features include:
- PLAIN, LOGIN, CRAM-MD5, GSSAPI, DIGEST-MD5 and NTLM authentications
- TLS encrypted connections
- Internationalized Domain Names (IDN) support
- IPv6 support
- robustness
- detailed error messages if something goes wrong (including the full
  answer of the SMTP server)
- sendmail compatible exit codes (which most MUAs understand).

Simply tell your MUA to call msmtp instead of /usr/sbin/sendmail (with
Mutt that's just one additional line in the config file).

%description -l pl
msmtp to prosty program dzia³aj±cy jako "wtyczka SMTP" dla Mutta i
innych klientów pocztowych (MUA - mail user agents). Przekierowuje
wiadomo¶ci do serwera SMTP (na przyk³ad providera darmowych kont
e-mail), który je dostarcza. Mo¿liwo¶ci obejmuj±:
- uwierzytelnianie PLAIN, LOGIN, CRAM-MD5, GSSAPI, DIGEST-MD5 i NTLM
- obs³ugê Internationalized Domain Names (IDN)
- szyfrowane po³±czenia TLS
- obs³ugê IPv6
- szczegó³owe komunikaty b³êdów w przypadku niepowodzenia (w³±cznie z
  pe³n± odpowiedzi± serwera SMTP)
- kody wyj¶cia kompatybilne z sendmailem (które rozumie wiêkszo¶æ
  MUA).

Wystarczy przekazaæ klientowi pocztowemu, aby wywo³ywa³ msmtp zamiast
/usr/sbin/sendmail (w Mutcie to po prostu dodatkowa linia w pliku
konfiguracyjnym).

%package sendmail
Summary:	msmtp sendmail compatible wrapper
Summary(pl):	msmtp - dowi±zania symboliczne do sendmaila
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}
Provides:	/usr/lib/sendmail
Obsoletes:	/usr/lib/sendmail

%description sendmail
msmtp sendmail compatible wrapper.

%description sendmail -l pl
Dowi±zania symboliczne msmtp do sendmaila.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal} -I gnulib/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/usr/lib,%{_sysconfdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/msmtprc
ln -s %{_bindir}/%{name} $RPM_BUILD_ROOT/usr/lib/sendmail
ln -s %{_bindir}/%{name} $RPM_BUILD_ROOT%{_sbindir}/sendmail

%find_lang %{name}

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README THANKS doc/msmtprc-{system,user}.example
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/msmtp*
%{_infodir}/msmtp*

%files sendmail
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_sbindir}/*
/usr/lib/sendmail
