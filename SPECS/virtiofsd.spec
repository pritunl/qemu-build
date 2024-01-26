Name:           virtiofsd
Version:        1.7.2
Release:        1%{?dist}
Summary:        Virtio-fs vhost-user device daemon (Rust version)

# Upstream license specification: Apache-2.0 AND BSD-3-Clause
License:        Apache-2.0 AND BSD-3-Clause
URL:            https://gitlab.com/virtio-fs/virtiofsd
Source0:        %{crates_source}
Source1:        %{name}-%{version}-vendor.tar.gz

ExclusiveArch:  x86_64 aarch64 s390x
BuildRequires:  rust-toolset
BuildRequires:  libcap-ng-devel
BuildRequires:  libseccomp-devel
Provides: virtiofsd
Obsoletes: qemu-virtiofsd = 17:6.2.0
# Both qemu-virtiofsd and virtiofsd ship the same binary
Conflicts: qemu-virtiofsd = 17:6.2.0

%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%cargo_prep -V 1

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
* Tue Jul 18 2023 German Maglione <gmaglione@redhat.com> - 1.7.2-1
- Update to upstream version 1.7.2 [bz#2233498]

* Tue Jul 18 2023 German Maglione <gmaglione@redhat.com> - 1.7.0-1
- Update to upstream version 1.7.0 [bz#2222221]

* Thu Dec 22 2022 German Maglione <gmaglione@redhat.com> - 1.5.0-1
- Update to upstream version 1.5.0 [bz#2123070]

* Wed Jul 27 2022 Sergio Lopez <slp@redhat.com> - 1.4.0-1
- Update to upstream version 1.4.0 [bz#2111356]

* Mon Jun 27 2022 Sergio Lopez <slp@redhat.com> - 1.3.0-1
- Update to upstream version 1.3.0 [bz#2077854]

* Fri Feb 18 2022 Sergio Lopez <slp@redhat.com> - 1.1.0-3
- Restore "Provides: virtiofsd", despite rpmdeplint complains, to
  satisfy qemu-kvm dependencies

* Fri Jan 28 2022 Sergio Lopez <slp@redhat.com> - 1.1.0-2
- Explicitly declare the conflict with qemu-virtiofsd
- Remove explicit library dependencies
- Remove useless "Provides: virtiosfd"
- Remove Windows binaries from vendor tarball

* Thu Jan 27 2022 Sergio Lopez <slp@redhat.com> - 1.1.0-1
- Initial package

