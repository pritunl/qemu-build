Name:           libslirp
Version:        4.0.0
Release:        3%{?dist}
Summary:        A general purpose TCP-IP emulator

# check the SPDX tags in source files for details
License:        BSD and MIT
URL:            https://gitlab.freedesktop.org/slirp/%{name}
Source0:        %{url}/-/archive/v%{version}/%{name}-v%{version}.tar.gz

Patch0001:      0001-Fix-heap-overflow-in-ip_reass-on-big-packet-input.patch
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
%autosetup -S git_am -n %{name}-v%{version}

%build
%meson
%meson_build


%install
%meson_install


%files
%license COPYRIGHT
%doc README.md
%{_libdir}/%{name}.so.0*

%files devel
%dir %{_includedir}/slirp/
%{_includedir}/slirp/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/slirp.pc


%changelog
* Fri Aug  2 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.0.0-3
- Fix CVE-2019-14378, rhbz#1735654

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 22 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.0.0-1
- Initial package, rhbz#1712980
