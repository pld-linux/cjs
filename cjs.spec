#
# Conditional build:
%bcond_without	sysprof		# sysprof profiling support
%bcond_without	systemtap	# systemtap/dtrace trace support
%bcond_with	installed_tests	# tests package
%bcond_with	tests		# JS tests (one API tests fail)

Summary:	Javascript Bindings for Cinnamon
Summary(pl.UTF-8):	Wiązania JavaScriptu dla środowiska Cinnamon
Name:		cjs
Version:	128.1
Release:	1
Group:		Libraries
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
License:	MIT and (MPL v1.1 or GPL v2+ or LGPL v2+)
#Source0Download: https://github.com/linuxmint/cjs/tags
Source0:	https://github.com/linuxmint/cjs/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	3b8a136df8dbad6196598f098db72dea
URL:		https://github.com/linuxmint/Cinnamon
BuildRequires:	cairo-gobject-devel
BuildRequires:	glib2-devel >= 1:2.66.0
BuildRequires:	gobject-introspection-devel >= 1.71.0
BuildRequires:	gtk4-devel >= 4.0
BuildRequires:	libffi-devel >= 3.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	meson >= 0.62.0
BuildRequires:	mozjs128-devel >= 128
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.14.0
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
%{?with_sysprof:BuildRequires:	sysprof-devel >= 3.38}
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
Requires:	glib2 >= 1:2.66.0
Requires:	gobject-introspection >= 1.71.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# dtrace script expects CPP to be cpp, not "gcc -E", so force it regardless of rpm version
# (autotools-based rpm<4.19 used to have "gcc -E", cmake builds for 4.19+ switched to cpp)
%define		__cpp	cpp

%description
Cjs allows using Cinnamon libraries from JavaScript. It's based on the
SpiderMonkey JavaScript engine from Mozilla and the GObject
introspection framework.

%description -l pl.UTF-8
Cjs pozwala na używanie bibliotek Cinnamona z poziomu JavaScriptu.
Jest oparty na silniku JavaScriptu SpiderMonkey z projektu Mozilla
oraz szkielecie GObject Introspection.

%package devel
Summary:	Development package for cjs
Summary(pl.UTF-8):	Pakiet programistyczny cjs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cairo-gobject-devel
Requires:	glib2-devel >= 1:2.66.0
Requires:	gobject-introspection-devel >= 1.71.0
Requires:	libffi-devel >= 3.0
Requires:	mozjs128-devel >= 128
%if %{without installed_tests}
Obsoletes:	cjs-tests < %{version}-%{release}
%endif

%description devel
Files for development with cjs.

%description devel -l pl.UTF-8
Pliki do tworzenia oprogramowania z użyciem cjs

%package tests
Summary:	Tests for the cjs package
Summary(pl.UTF-8):	Testy dla pakietu cjs
Group:		Development/Libraries
Requires(post,postun):	glib2-devel >= 1:2.66.0
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

%{__sed} -i -e 's/ library(/ shared_library(/' installed-tests/js/meson.build

%build
%meson \
	%{?with_systemtap:-Ddtrace=true} \
	%{!?with_installed_tests:-Dinstalled_tests=false} \
	-Dprofiler=%{__enabled_disabled sysprof} \
	-Dreadline=enabled \
	-Dskip_dbus_tests=true \
	-Dskip_gtk_tests=true \
	%{?with_systemtap:-Dsystemtap=true}

%meson_build

%if %{with tests}
%ninja_test -C build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post tests
%glib_compile_schemas

%postun tests
%glib_compile_schemas

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README.md debian/changelog
%attr(755,root,root) %{_bindir}/cjs
%attr(755,root,root) %{_bindir}/cjs-console
%{_libdir}/libcjs.so.*.*.*
%ghost %{_libdir}/libcjs.so.0
%dir %{_libdir}/cjs
%dir %{_libdir}/cjs/girepository-1.0
%{_libdir}/cjs/girepository-1.0/CjsPrivate-1.0.typelib
%{_datadir}/cjs-1.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcjs.so
%{_includedir}/cjs-1.0
%{_pkgconfigdir}/cjs-1.0.pc
%{_examplesdir}/%{name}-%{version}

%if %{with installed_tests}
%files tests
%defattr(644,root,root,755)
# TODO: move system-side installed-tests dirs somewhere (filesystem?)
%dir %{_libexecdir}/installed-tests
%dir %{_libexecdir}/installed-tests/cjs
%attr(755,root,root) %{_libexecdir}/installed-tests/cjs/debugger-test.sh
%attr(755,root,root) %{_libexecdir}/installed-tests/cjs/minijasmine
%{_libexecdir}/installed-tests/cjs/lib*.so
%{_libexecdir}/installed-tests/cjs/*.typelib
%{_libexecdir}/installed-tests/cjs/debugger
%{_libexecdir}/installed-tests/cjs/js
%dir %{_libexecdir}/installed-tests/cjs/scripts
%attr(755,root,root) %{_libexecdir}/installed-tests/cjs/scripts/test*.sh
%{_datadir}/glib-2.0/schemas/org.cinnamon.CjsTest.gschema.xml
%dir %{_datadir}/installed-tests
%{_datadir}/installed-tests/cjs
%endif

%if %{with systemtap}
%files -n systemtap-cjs
%defattr(644,root,root,755)
%{_datadir}/systemtap/tapset/cjs.stp
%endif
