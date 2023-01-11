Name:           libcacard
Version:        2.7.0
Release:        2%{?dist}
Summary:        CAC (Common Access Card) library
License:        LGPLv2+
URL:            http://www.spice-space.org/page/Libcacard
Source0:        http://www.spice-space.org/download/libcacard/%{name}-%{version}.tar.xz
Source1:        http://www.spice-space.org/download/libcacard/%{name}-%{version}.tar.xz.asc
Source2:        gpgkey-15B5C33D.gpg
# https://gitlab.freedesktop.org/spice/libcacard/merge_requests/5
Patch0:         %{name}-2.7.0-caching-keys.patch
Epoch:          3

BuildRequires:  glib2-devel
BuildRequires:  nss-devel
BuildRequires:  softhsm
BuildRequires:  opensc
BuildRequires:  gnutls-utils
BuildRequires:  nss-tools
BuildRequires:  openssl
BuildRequires:  gnupg2
Conflicts:      qemu-common < 2:2.5.0

%description
This library provides emulation of smart cards to a virtual card
reader running in a guest virtual machine.

It implements DoD CAC standard with separate pki containers
(compatible coolkey), using certificates read from NSS.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%setup -q
%patch0 -p1 -b .caching

%build
%configure --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}

%check
# Do not run the tests on s390x, which fails
%ifnarch s390x
sed -i "s!/usr/lib64/!%{_libdir}/!" tests/setup-softhsm2.sh
make check
%endif

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc NEWS
%{_libdir}/libcacard.so.*

%files devel
%{_includedir}/cacard
%{_libdir}/libcacard.so
%{_libdir}/pkgconfig/libcacard.pc

%changelog
* Mon Sep 16 2019 Jakub Jelen <jjelen@redhat.com> - 2.7.0-2
- Remove key caching capabilities since to avoid invalid handle reuse (#1746883)

* Tue Jul 23 2019 Jakub Jelen <jjelen@redhat.com> - 2.7.0-1
- Update to libcacard 2.7.0 to improve Windows compatibility (#1615840)

* Mon Dec 17 2018 Christophe Fergeau <cfergeau@redhat.com> - 2.6.1-1
- Update to libcacard 2.6.1
  Resolves: rhbz#1620129

* Mon Aug 13 2018 Troy Dawson <tdawson@redhat.com> - 3:2.5.3-5
- Release Bumped for el8 Mass Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 01 2017 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.5.3-1
- new upstream release 2.5.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec  8 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.5.2-1
- Update to latest libcacard's release (2.5.2)

* Wed Nov 25 2015 Fabiano Fidêncio <fidencio@redhat.com> - 3:2.5.1-1
- Update to latest libcacard's release (2.5.1)

* Wed Sep 23 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 3:2.5.0-1
- Initial standalone libcacard package.
