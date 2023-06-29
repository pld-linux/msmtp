Summary:	SMTP "plugin" for MUAs
Summary(pl.UTF-8):	"Wtyczka" SMTP dla klientów pocztowych (MUA)
Name:		msmtp
Version:	1.8.24
Release:	1
License:	GPL v3+
Group:		Networking/Utilities
#Source0Download: https://marlam.de/msmtp/download/
Source0:	https://marlam.de/msmtp/releases/%{name}-%{version}.tar.xz
# Source0-md5:	1291538d45aeb5e0b818400aa045dc7b
Patch0:		%{name}-home_etc.patch
Patch1:		%{name}-info.patch
Source1:	%{name}rc
URL:		https://marlam.de/msmtp/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	gettext-tools
# with AI_IDN support (or libidn2-devel)
BuildRequires:	glibc-devel >= 6:2.4
BuildRequires:	gnutls-devel >= 3.4
BuildRequires:	gsasl-devel
BuildRequires:	libsecret-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo
BuildRequires:	xz
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

%description -l pl.UTF-8
msmtp to prosty program działający jako "wtyczka SMTP" dla Mutta i
innych klientów pocztowych (MUA - mail user agents). Przekierowuje
wiadomości do serwera SMTP (na przykład providera darmowych kont
e-mail), który je dostarcza. Możliwości obejmują:
- uwierzytelnianie PLAIN, LOGIN, CRAM-MD5, GSSAPI, DIGEST-MD5 i NTLM
- obsługę Internationalized Domain Names (IDN)
- szyfrowane połączenia TLS
- obsługę IPv6
- szczegółowe komunikaty błędów w przypadku niepowodzenia (włącznie z
  pełną odpowiedzią serwera SMTP)
- kody wyjścia kompatybilne z sendmailem (które rozumie większość
  MUA).

Wystarczy przekazać klientowi pocztowemu, aby wywoływał msmtp zamiast
/usr/sbin/sendmail (w Mutcie to po prostu dodatkowa linia w pliku
konfiguracyjnym).

%package sendmail
Summary:	msmtp sendmail compatible wrapper
Summary(pl.UTF-8):	msmtp - dowiązania symboliczne do sendmaila
Group:		Networking/Daemons
Requires:	%{name} = %{version}-%{release}

%description sendmail
msmtp sendmail compatible wrapper.

%description sendmail -l pl.UTF-8
Dowiązania symboliczne msmtp do sendmaila.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__gettextize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-silent-rules \
	--with-libgsasl \
	--with-libidn \
	--with-libsecret \
	--with-tls=gnutls
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
rm -f scripts/Makefile*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS doc/msmtprc-{system,user}.example scripts
%attr(755,root,root) %{_bindir}/msmtp
%attr(755,root,root) %{_bindir}/msmtpd
%{_mandir}/man1/msmtp.1*
%{_mandir}/man1/msmtpd.1*
%{_infodir}/msmtp.info*

%files sendmail
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/msmtprc
%attr(755,root,root) %{_sbindir}/sendmail
/usr/lib/sendmail
