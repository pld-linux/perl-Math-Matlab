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
Summary(pl.UTF-8):	Math::Matlab - interfejs do uruchamiania programów Matlaba z poziomu Perla
Name:		perl-Math-Matlab
Version:	0.08
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	fcab9a197d49dd5453f9d82de0ca7382
%if %{with autodeps}
BuildRequires:	apache-mod_perl
BuildRequires:	perl-URI
BuildRequires:	perl-libapreq2
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
The MathWorks web-site at <http://www.mathworks.com/>.

%description -l pl.UTF-8
Pakiet Math::Matlab udostępnia interfejs do uruchamiania programów
Matlaba z poziomu Perla i przechwytywania wyjścia (tego, co programy
Matlaba wypisują na STDOUT) do łańcucha. Więcej informacji o Matlabie
można znaleźć na stronie MathWorks pod adresem
<http://www.mathworks.com/>.

%package Remote
Summary:	Math::Matlab::Remote - interface to a remote Matlab process
Summary(pl.UTF-8):	Math::Matlab::Remote - interfejs do zdalnego procesu Matlaba
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description Remote
Math::Matlab::Remote implements an interface to a remote Matlab server
(see Math::Matlab::Server). It uses the LWP package to access the
server via the HTTP protocol. The Remote object has the URI of the
server, a timeout value for the requests and a user name and password
used for basic authentication of the request.

%description Remote -l pl.UTF-8
Math::Matlab::Remote to implementacja interfejsu do zdalnego serwera
Matlaba (moduł Math::Matlab::Server). Używa pakietu LWP do dostępu do
serwera za pośrednictwem protokołu HTTP. Obiekt Remote zawiera URI do
serwera, wartość maksymalnego czasu oczekiwania dla żądań oraz nazwę
użytkownika i hasło do prostego uwierzytelniania żądania.

%package Server
Summary:	Math::Matlab::Server - a Matlab server as a mod_perl content handler
Summary(pl.UTF-8):	Math::Matlab::Server - serwer Matalaba jako obsługa treści dla mod_perla
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}

%description Server
Math::Matlab::Server implements a mod_perl content handler which takes
form input arguments named CODE, REL_MWD and RAW_OUTPUT, calls the
execute() method of the server's Math::Matlab object passing the CODE
and REL_MWD arguments, and sends back the results as a 'text/plain'
document. The results are the value returned by the object's
fetch_raw_result() or fetch_result() method, depending whether or not
the RAW_OUTPUT parameter is true.

%description Server -l pl.UTF-8
Math::Matlab::Server to implementacja funkcji obsługi generowania
treści dla mod_perla, przyjmująca z wejścia formularza argumenty o
nazwach CODE, REL_MWD i RAW_OUTPUT, wywołująca metodę execute()
obiektu Math::Matlab na serwerze przekazując argumenty CODE i REL_MWD,
a następnie odsyłająca wyniki jako dokument text/plain. Wyniki to
wartość zwrócona przez metodę fetch_raw_result() lub fetch_result()
obiektu, w zależności od wartości parametru RAW_OUTPUT.

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
