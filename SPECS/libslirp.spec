Name:           libslirp
Version:        4.4.0
Release:        7%{?dist}
Summary:        A general purpose TCP-IP emulator

# check the SPDX tags in source files for details
License:        BSD and MIT
URL:            https://gitlab.freedesktop.org/slirp/%{name}
Source0:        %{url}/-/archive/v%{version}/%{name}-%{version}.tar.xz
Patch0001: 0001-Add-mtod_check.patch
Patch0002: 0002-bootp-limit-vendor-specific-area-to-input-packet-mem.patch
Patch0003: 0003-bootp-check-bootp_input-buffer-size.patch
Patch0004: 0004-upd6-check-udp6_input-buffer-size.patch
Patch0005: 0005-tftp-check-tftp_input-buffer-size.patch
Patch0006: 0006-tftp-introduce-a-header-structure.patch
Patch0007: 0007-udp-check-upd_input-buffer-size.patch
Patch0008: 0001-Fix-DHCP-broken-in-libslirp-v4.6.0.patch
Patch0009: 0001-New-utility-slirp_ether_ntoa.patch
Patch00010: 0002-Replace-inet_ntoa-with-safer-inet_ntop.patch


BuildRequires:  git-core
BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  glib2-devel

%description
A general purpose TCP-IP emulator used by virtual machine hypervisors
to provide virtual networking services.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -S git_am

%build
%meson
%meson_build


%install
%meson_install


%files
%license COPYRIGHT
%doc README.md CHANGELOG.md
%{_libdir}/%{name}.so.0*

%files devel
%dir %{_includedir}/slirp/
%{_includedir}/slirp/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/slirp.pc


%changelog
* Fri Feb 11 2022 Jindrich Novy <jnovy@redhat.com> - 4.4.0-7
- fix also socket.c, thanks to Marc-André Lureau
- Related: #2000051

* Fri Feb 11 2022 Jindrich Novy <jnovy@redhat.com> - 4.4.0-6
- add patches fixing gating tests from Marc-André Lureau
- Related: #2000051

* Wed Feb 09 2022 Jindrich Novy <jnovy@redhat.com> - 4.4.0-5
- add gating.yaml
- Related: #2000051

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 4.4.0-4
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Jun 18 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.4.0-3
- Fix CVE-2021-3592 CVE-2021-3593 CVE-2021-3594 CVE-2021-3595 out-of-bounds access
  Resolves: rhbz#1970826 rhbz#1970839 rhbz#1970857 rhbz#1970847

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 4.4.0-2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Dec  2 18:19:30 +04 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.4.0-1
- new version

* Fri Nov 27 20:10:28 +04 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.3.1-3
- Fix CVE-2020-29129 CVE-2020-29130 out-of-bounds access while processing ARP/NCSI packets
  rhbz#1902232

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.3.1-1
- New v4.3.1 release

* Thu Apr 23 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.3.0-1
- New v4.3.0 release

* Mon Apr 20 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.2.0-2
- CVE-2020-1983 fix

* Tue Mar 17 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.2.0-1
- New v4.2.0 release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.1.0-1
- New v4.1.0 release

* Fri Aug  2 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.0.0-3
- Fix CVE-2019-14378, rhbz#1735654

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 22 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.0.0-1
- Initial package, rhbz#1712980
