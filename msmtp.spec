Summary:	SMTP "plugin" for MUAs
Summary(pl):	"Wtyczka" SMTP dla klient�w pocztowych (MUA)
Name:		msmtp
Version:	1.4.2
Release:	0.1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/msmtp/%{name}-%{version}.tar.bz2
# Source0-md5:	3db095102259103e4eb48fc0c7d21618
Patch0:		%{name}-home_etc.patch
URL:		http://msmtp.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pkgconfig
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
- sendmail compatible exit codes (which most MUAs understand).

Simply tell your MUA to call msmtp instead of /usr/sbin/sendmail (with
Mutt that's just one additional line in the config file).

%description -l pl
msmtp to prosty program dzia�aj�cy jako "wtyczka SMTP" dla Mutta i
prawdopodobnie innych klient�w pocztowych (MUA - mail user agents).
Przekierowuje wiadomo�ci do serwera SMTP (na przyk�ad providera
darmowych kont e-mail), kt�ry je dostarcza. Mo�liwo�ci obejmuj�:
- obs�ug� SMTP AUTH - metod PLAIN, LOGIN i CRAM-MD5
- szyfrowane po��czenia TLS
- obs�ug� IPv6
- szczeg�owe komunikaty b��d�w w przypadku niepowodzenia (w��cznie z
  pe�n� odpowiedzi� serwera SMTP)
- kody wyj�cia kompatybilne z sendmailem (kt�re rozumie wi�kszo��
  MUA).

Wystarczy przekaza� klientowi pocztowemu, aby wywo�ywa� msmtp zamiast
/usr/sbin/sendmail (w Mutcie to po prostu dodatkowa linia w pliku
konfiguracyjnym).

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal} -I gnulib/m4
%{__autoconf}
%{__autoheader}
%{__automake}
# could use gnutls instead (but is not ready for current libgcrypt)
# disable gsasl for now (see README.gsasl)
%configure \
	--with-ssl=openssl \
	--disable-gsasl
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README THANKS doc/msmtprc-{system,user}.example
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/msmtp*
#%lang(pl) %{_mandir}/pl/man1/msmtp*
%{_infodir}/msmtp*
%{_datadir}/info/dir*
