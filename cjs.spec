#
# Conditional build:
%bcond_without	sysprof		# sysprof profiling support
%bcond_without	systemtap	# systemtap/dtrace trace support
%bcond_with	tests		# JS tests (upstream failed to update them, e.g. tests for version < 4.0.0; some require $DISPLAY)

Summary:	Javascript Bindings for Cinnamon
Summary(pl.UTF-8):	Wiązania JavaScriptu dla środowiska Cinnamon
Name:		cjs
Version:	5.0.0
Release:	1
Group:		Libraries
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
License:	MIT and (MPL v1.1 or GPL v2+ or LGPL v2+)
#Source0Download: https://github.com/linuxmint/cjs/releases
Source0:	https://github.com/linuxmint/cjs/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	df2ac23311ef24b788386a0e021ef133
URL:		https://github.com/linuxmint/Cinnamon
BuildRequires:	cairo-gobject-devel
BuildRequires:	glib2-devel >= 1:2.58.0
BuildRequires:	gobject-introspection-devel >= 1.58.3
BuildRequires:	gtk4-devel >= 4.0
BuildRequires:	libffi-devel >= 3.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	meson >= 0.49.2
BuildRequires:	mozjs78-devel >= 78
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.14.0
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
%{?with_sysprof:BuildRequires:	sysprof-devel >= 3.38}
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
Requires:	glib2 >= 1:2.58.0
Requires:	gobject-introspection >= 1.58.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Requires:	glib2-devel >= 1:2.58.0
Requires:	gobject-introspection-devel >= 1.58.3
Requires:	libffi-devel >= 3.0
Requires:	mozjs78-devel >= 78

%description devel
Files for development with cjs.

%description devel -l pl.UTF-8
Pliki do tworzenia oprogramowania z użyciem cjs

%package tests
Summary:	Tests for the cjs package
Summary(pl.UTF-8):	Testy dla pakietu cjs
Group:		Development/Libraries
Requires(post,postun):	glib2-devel >= 1:2.58.0
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
%meson build \
	%{?with_systemtap:-Ddtrace=true} \
	%{!?with_sysprof:-Dprofiler=disabled} \
	%{?with_systemtap:-Dsystemtap=true}

%ninja_build -C build

%if %{with tests}
%ninja_test -C build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

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
%attr(755,root,root) %{_libdir}/libcjs.so.*.*.*
%ghost %{_libdir}/libcjs.so.0
%dir %{_libdir}/cjs
%dir %{_libdir}/cjs/girepository-1.0
%{_libdir}/cjs/girepository-1.0/CjsPrivate-1.0.typelib
%{_datadir}/cjs-1.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcjs.so
%{_includedir}/cjs-1.0
%{_pkgconfigdir}/cjs-1.0.pc
%{_examplesdir}/%{name}-%{version}

%files tests
%defattr(644,root,root,755)
# TODO: move system-side installed-tests dirs somewhere (filesystem?)
%dir %{_libexecdir}/installed-tests
%dir %{_libexecdir}/installed-tests/cjs
%attr(755,root,root) %{_libexecdir}/installed-tests/cjs/debugger-test.sh
%attr(755,root,root) %{_libexecdir}/installed-tests/cjs/minijasmine
%attr(755,root,root) %{_libexecdir}/installed-tests/cjs/lib*.so
%{_libexecdir}/installed-tests/cjs/*.typelib
%{_libexecdir}/installed-tests/cjs/debugger
%{_libexecdir}/installed-tests/cjs/js
%dir %{_libexecdir}/installed-tests/cjs/scripts
%attr(755,root,root) %{_libexecdir}/installed-tests/cjs/scripts/test*.sh
%{_datadir}/glib-2.0/schemas/org.cinnamon.CjsTest.gschema.xml
%dir %{_datadir}/installed-tests
%{_datadir}/installed-tests/cjs

%if %{with systemtap}
%files -n systemtap-cjs
%defattr(644,root,root,755)
%{_datadir}/systemtap/tapset/cjs.stp
%endif
