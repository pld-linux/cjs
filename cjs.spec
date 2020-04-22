#
# Conditional build:
%bcond_without	systemtap	# systemtap/dtrace trace support
%bcond_with	tests		# JS tests (upstream failed to update them, e.g. tests for version < 4.0.0; some require $DISPLAY)

Summary:	Javascript Bindings for Cinnamon
Summary(pl.UTF-8):	Wiązania JavaScriptu dla środowiska Cinnamon
Name:		cjs
Version:	4.4.0
Release:	1
Group:		Libraries
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
License:	MIT and (MPL v1.1 or GPL v2+ or LGPL v2+)
#Source0Download: https://github.com/linuxmint/cjs/releases
Source0:	https://github.com/linuxmint/cjs/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d01c0355343b0278082b24cceed682e3
URL:		https://github.com/linuxmint/Cinnamon
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	cairo-gobject-devel
BuildRequires:	glib2-devel >= 1:2.42.0
BuildRequires:	gobject-introspection-devel >= 1.46.0
BuildRequires:	gtk+3-devel >= 3.14.0
BuildRequires:	libffi-devel >= 3.0
BuildRequires:	libtool >= 2:2.2.0
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	mozjs52-devel >= 52
BuildRequires:	pkgconfig >= 1:0.14.0
BuildRequires:	readline-devel
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
Requires:	glib2 >= 1:2.42.0
Requires:	gobject-introspection >= 1.46.0
Requires:	gtk+3 >= 3.14.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cjs allows using Cinnamon libraries from Javascript. It's based on the
Spidermonkey Javascript engine from Mozilla and the GObject
introspection framework.

%package devel
Summary:	Development package for cjs
Summary(pl.UTF-8):	Pakiet programistyczny cjs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cairo-gobject-devel
Requires:	glib2-devel >= 1:2.42.0
Requires:	gobject-introspection-devel >= 1.46.0
Requires:	gtk+3-devel >= 3.14.0
Requires:	libffi-devel >= 3.0
Requires:	mozjs52-devel >= 52

%description devel
Files for development with cjs.

%description devel -l pl.UTF-8
Pliki do tworzenia oprogramowania z użyciem cjs

%package tests
Summary:	Tests for the cjs package
Summary(pl.UTF-8):	Testy dla pakietu cjs
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description tests
The cjs-tests package contains tests that can be used to verify the
functionality of the installed cjs package.

%description tests -l pl.UTF-8
Ten pakiet zawiera testy, których można użyć do sprawdzenia
funkcjonalności zainstalowanego pakietu cjs.

%package -n systemtap-cjs
Summary:	systemtap/dtrace probes for cjs
Summary(pl.UTF-8):	Sondy systemtap/dtrace dla cjs
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	systemtap-client

%description -n systemtap-cjs
systemtap/dtrace probes for cjs.

%description -n systemtap-cjs -l pl.UTF-8
Sondy systemtap/dtrace dla cjs.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-installed-tests \
	--disable-silent-rules \
	%{?with_systemtap:--enable-systemtap}

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcjs.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cjs/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README.md
%attr(755,root,root) %{_bindir}/cjs
%attr(755,root,root) %{_bindir}/cjs-console
%attr(755,root,root) %{_libdir}/libcjs.so.*.*.*
%ghost %{_libdir}/libcjs.so.0
%dir %{_libdir}/cjs
%dir %{_libdir}/cjs/girepository-1.0
%{_libdir}/cjs/girepository-1.0/CjsPrivate-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcjs.so
%{_includedir}/cjs-1.0
%{_pkgconfigdir}/cjs-1.0.pc
%{_examplesdir}/%{name}-%{version}

%files tests
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/cjs/libgimarshallingtests.so
%attr(755,root,root) %{_libdir}/cjs/libregress.so
%attr(755,root,root) %{_libdir}/cjs/libwarnlib.so
%dir %{_libexecdir}/cjs
%{_libexecdir}/cjs/installed-tests
# FIXME: this is common dir for installed-tests, move to common package (or don't package installed-tests at all)
%dir %{_datadir}/installed-tests
%{_datadir}/installed-tests/cjs

%if %{with systemtap}
%files -n systemtap-cjs
%defattr(644,root,root,755)
%{_datadir}/systemtap/tapset/cjs.stp
%endif
