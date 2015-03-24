#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Javascript Bindings for Cinnamon
Name:		cjs
Version:	2.4.1
Release:	1
Group:		Libraries
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
License:	MIT and (MPLv1.1 or GPLv2+ or LGPLv2+)
Source0:	https://github.com/linuxmint/cjs/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	846940e9cf97b15a5b3940cf5c7b2591
URL:		http://cinnamon.linuxmint.com/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1.7.2
BuildRequires:	cairo-gobject-devel
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 1.38.0
BuildRequires:	gtk+3-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	mozjs24-devel
BuildRequires:	pkgconfig >= 0.14.0
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Cjs allows using Cinnamon libraries from Javascript. It's based on the
Spidermonkey Javascript engine from Mozilla and the GObject
introspection framework.

%package devel
Summary:	Development package for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Files for development with %{name}.

%package tests
Summary:	Tests for the cjs package
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description tests
The cjs-tests package contains tests that can be used to verify the
functionality of the installed cjs package.

%prep
%setup -q
sed -i -e 's@{ACLOCAL_FLAGS}@{ACLOCAL_FLAGS} -I m4@g' Makefile.am
echo "AC_CONFIG_MACRO_DIR([m4])" >> configure.ac

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-silent-rules \
	--disable-static \
	--enable-installed-tests \

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcjs.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/cjs/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING COPYING.LGPL NEWS README
%attr(755,root,root) %{_bindir}/cjs
%attr(755,root,root) %{_bindir}/cjs-console
%attr(755,root,root) %{_libdir}/libcjs.so.*.*.*
%ghost %{_libdir}/libcjs.so.0
%dir %{_libdir}/cjs
%dir %{_libdir}/cjs/girepository-1.0
%{_libdir}/cjs/girepository-1.0/CjsPrivate-1.0.typelib

%files devel
%defattr(644,root,root,755)
%doc examples/*
%{_includedir}/cjs-1.0
%{_libdir}/libcjs.so
%{_pkgconfigdir}/cjs-1.0.pc
%{_pkgconfigdir}/cjs-internals-1.0.pc
%attr(755,root,root) %{_libdir}/cjs/libgimarshallingtests.so
%attr(755,root,root) %{_libdir}/cjs/libregress.so
%attr(755,root,root) %{_libdir}/cjs/libwarnlib.so

%files tests
%defattr(644,root,root,755)
%{_libdir}/cjs/installed-tests
%{_datadir}/installed-tests
