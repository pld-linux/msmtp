Summary:	SMTP "plugin" for MUAs
Summary(pl):	"Wtyczka" SMTP dla klientów pocztowych (MUA)
Name:		msmtp
Version:	0.6.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	9cbe03c8f63d793fae9c3d79a20a4a25
URL:		http://msmtp.sourceforge.net/
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
%doc AUTHORS ChangeLog README THANKS
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/msmtp*
