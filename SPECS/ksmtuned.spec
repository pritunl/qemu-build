Name: ksmtuned
Version: 0.1.0
Release: 9%{?dist}

Summary: Kernel Samepage Merging services
License: GPLv2+
URL: https://github.com/ksmtuned/ksmtuned
Source0: https://github.com/ksmtuned/ksmtuned/archive/v%{version}/ksmtuned-%{version}.tar.gz

# Package was originally 'ksm' as a subpackage of 'qemu'
Obsoletes: ksm < 3.0.0-0.2

BuildRequires: gcc
BuildRequires: meson
%{?systemd_requires}
BuildRequires: systemd


%description
Kernel Samepage Merging (KSM) is a memory-saving de-duplication feature,
that merges anonymous (private) pages (not pagecache ones).

This package provides service files for disabling (ksm) and tuning
(ksmtuned)


%prep
%autosetup -p1


%build
%meson \
    -Dredhat-sysconfig=true
%meson_build


%install
%meson_install


%post
%systemd_post ksm.service
%systemd_post ksmtuned.service
%preun
%systemd_preun ksm.service
%systemd_preun ksmtuned.service
%postun
%systemd_postun_with_restart ksm.service
%systemd_postun_with_restart ksmtuned.service


%files
%license COPYING
%{_libexecdir}/ksmctl
%{_sbindir}/ksmtuned
%{_unitdir}/ksmtuned.service
%{_unitdir}/ksm.service
%config(noreplace) %{_sysconfdir}/ksmtuned.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ksm


%changelog
* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.1.0-7
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Cole Robinson <crobinso@redhat.com> - 0.1.0-1
- Initial package
