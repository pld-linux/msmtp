Summary:	SMTP "plugin" for MUAs
Summary(pl):	"Wtyczka" SMTP dla klientów pocztowych (MUA)
Name:		msmtp
Version:	1.3.9
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# Source0-md5:	8e941785730c1ea1ee7fc9a65da41339
Patch0:		%{name}-home_etc.patch
URL:		http://msmtp.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	openssl-devel >= 0.9.7d
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
msmtp to prosty program dzia³aj±cy jako "wtyczka SMTP" dla Mutta i
prawdopodobnie innych klientów pocztowych (MUA - mail user agents).
Przekierowuje wiadomo¶ci do serwera SMTP (na przyk³ad providera
darmowych kont e-mail), który je dostarcza. Mo¿liwo¶ci obejmuj±:
- obs³ugê SMTP AUTH - metod PLAIN, LOGIN i CRAM-MD5
- szyfrowane po³±czenia TLS
- obs³ugê IPv6
- szczegó³owe komunikaty b³êdów w przypadku niepowodzenia (w³±cznie z
  pe³n± odpowiedzi± serwera SMTP)
- kody wyj¶cia kompatybilne z sendmailem (które rozumie wiêkszo¶æ
  MUA).

Wystarczy przekazaæ klientowi pocztowemu, aby wywo³ywa³ msmtp zamiast
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

%{__make} \
	install\
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README THANKS doc/msmtprc-{system,user}.example
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/msmtp*
%{_infodir}/msmtp*
