#
# Conditional build:
%bcond_without	autodeps	# don't require packages only for autodeps generation
%bcond_with	tests		# perform "make test" (requires Matlab installation)
# matlab			# command to execute matlab
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Math
%define		pnam	Matlab
Summary:	Math::Matlab - interface for running Matlab programs from Perl
Summary(pl):	Math::Matlab - interfejs do uruchamiania program�w Matlaba z poziomu Perla
Name:		perl-Math-Matlab
Version:	0.02
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	5fd505c6195eeb24e9e3c39bdd6a1fe2
%if %{with autodeps}
BuildRequires:	apache-mod_perl
BuildRequires:	perl-URI
BuildRequires:	perl-libapreq
BuildRequires:	perl-libwww
%endif
%if %{with tests}
BuildRequires:	perl-Test-Simple >= 0.01
%endif
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
#Requires:	matlab
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%{!?matlab:%define	matlab	/usr/local/bin/matlab -nodisplay -nojvm}

%description
The Math::Matlab package provides an interface for running Matlab
programs from Perl and capturing the output (what the Matlab program
prints to STDOUT) into a string. For more information on Matlab see
The MathWorks web-site at http://www.mathworks.com/ .

%description -l pl
Pakiet Math::Matlab udost�pnia interfejs do uruchamiania program�w
Matlaba z poziomu Perla i przechwytywania wyj�cia (tego, co programy
Matlaba wypisuj� na STDOUT) do �a�cucha. Wi�cej informacji o Matlabie
mo�na znale�� na stronie MathWorks pod adresem
http://www.mathworks.com/ .

%package Remote
Summary:	Math::Matlab::Remote - interface to a remote Matlab process
Summary(pl):	Math::Matlab::Remote - interfejs do zdalnego procesu Matlaba
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}

%description Remote
Math::Matlab::Remote implements an interface to a remote Matlab server
(see Math::Matlab::Server). It uses the LWP package to access the
server via the HTTP protocol. The Remote object has the URI of the
server, a timeout value for the requests and a user name and password
used for basic authentication of the request.

%description Remote -l pl
Math::Matlab::Remote to implementacja interfejsu do zdalnego serwera
Matlaba (modu� Math::Matlab::Server). U�ywa pakietu LWP do dost�pu do
serwera za po�rednictwem protoko�u HTTP. Obiekt Remote zawiera URI do
serwera, warto�� maksymalnego czasu oczekiwania dla ��da� oraz nazw�
u�ytkownika i has�o do prostego uwierzytelniania ��dania.

%package Server
Summary:	Math::Matlab::Server - a Matlab server as a mod_perl content handler
Summary(pl):	Math::Matlab::Server - serwer Matalaba jako obs�uga tre�ci dla mod_perla
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}

%description Server
Math::Matlab::Server implements a mod_perl content handler which takes
form input arguments named CODE, REL_MWD and RAW_OUTPUT, calls the
execute() method of the server's Math::Matlab object passing the CODE
and REL_MWD arguments, and sends back the results as a 'text/plain'
document. The results are the value returned by the object's
fetch_raw_result() or fetch_result() method, depending whether or not
the RAW_OUTPUT parameter is true.

%description Server -l pl
Math::Matlab::Server to implementacja funkcji obs�ugi generowania
tre�ci dla mod_perla, przyjmuj�ca z wej�cia formularza argumenty o
nazwach CODE, REL_MWD i RAW_OUTPUT, wywo�uj�ca metod� execute()
obiektu Math::Matlab na serwerze przekazuj�c argumenty CODE i REL_MWD,
a nast�pnie odsy�aj�ca wyniki jako dokument text/plain. Wyniki to
warto�� zwr�cona przez metod� fetch_raw_result() lub fetch_result()
obiektu, w zale�no�ci od warto�ci parametru RAW_OUTPUT.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
echo "%{matlab}" | \
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}/Math/Matlab.pm
%dir %{perl_vendorlib}/Math/Matlab
%{perl_vendorlib}/Math/Matlab/Local.pm
%{perl_vendorlib}/Math/Matlab/Pool.pm
%{_mandir}/man3/*

%files Remote
%defattr(644,root,root,755)
%{perl_vendorlib}/Math/Matlab/Remote.pm

%files Server
%defattr(644,root,root,755)
%doc INSTALL server.config
%{perl_vendorlib}/Math/Matlab/Server.pm
