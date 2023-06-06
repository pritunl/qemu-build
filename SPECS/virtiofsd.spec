Name:           virtiofsd
Version:        1.5.1
Release:        1%{?dist}
Summary:        Virtio-fs vhost-user device daemon (Rust version)

# Upstream license specification: Apache-2.0 AND BSD-3-Clause
License:        ASL 2.0 and BSD
URL:            https://gitlab.com/virtio-fs/virtiofsd
Source:         %{crates_source}
Patch:          virtiofsd-relax-env_logger-dep.diff

ExclusiveArch:  %{rust_arches}
# Some of our deps (i.e. vm-memory) are not available on 32 bits targets.
ExcludeArch:    i686

BuildRequires:  rust-packaging >= 21
BuildRequires:  libcap-ng-devel
BuildRequires:  libseccomp-devel
Requires:       qemu-common
Provides:       vhostuser-backend(fs)
Conflicts:      qemu-virtiofsd

%description
%{summary}.

%prep
%autosetup -n %{name}-%{version_no_tilde} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
mkdir -p %{buildroot}%{_libexecdir}
install -D -p -m 0755 target/release/virtiofsd %{buildroot}%{_libexecdir}/virtiofsd
install -D -p -m 0644 50-qemu-virtiofsd.json %{buildroot}%{_datadir}/qemu/vhost-user/50-qemu-virtiofsd.json

%files
%license LICENSE-APACHE LICENSE-BSD-3-Clause
%doc README.md
%{_libexecdir}/virtiofsd
%{_datadir}/qemu/vhost-user/50-qemu-virtiofsd.json

%changelog
* Thu Feb 09 2023 Sergio Lopez <slp@redhat.com> - 1.5.1-1
- Update to version 1.5.1

* Sun Feb 05 2023 Fabio Valentini <decathorpe@gmail.com> - 1.4.0-3
- Rebuild for fixed frame pointer compiler flags in Rust RPM macros.

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jul 26 2022 Sergio Lopez <slp@redhat.com> - 1.4.0-1
- Update to version 1.4.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 06 2022 Sergio Lopez <slp@redhat.com> - 1.3.0-1
- Update to version 1.3.0
- Build on all rust arches except i686 (32-bit targets are not supported)

* Mon May 16 2022 Sergio Lopez <slp@redhat.com> - 1.2.0-1
- Initial package

