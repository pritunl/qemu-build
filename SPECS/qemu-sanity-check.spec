%global debug_package %{nil}

# Architectures where the tests should pass.
#
# 2020-09: Fails on power64 because qemu TCG does not support all the
#   features required to boot Fedora.
#
# 2020-09: armv7 failed with:
# ./qemu-sanity-check: cannot find a Linux kernel in /boot
%global test_arches aarch64 %{s390x} x86_64

Name:           qemu-sanity-check
Version:        1.1.6
Release:        6%{?dist}
Summary:        Simple qemu and Linux kernel sanity checker
License:        GPLv2+

ExclusiveArch:  %{kernel_arches}

URL:            http://people.redhat.com/~rjones/qemu-sanity-check
Source0:        http://people.redhat.com/~rjones/qemu-sanity-check/files/%{name}-%{version}.tar.gz
Source1:        http://people.redhat.com/~rjones/qemu-sanity-check/files/%{name}-%{version}.tar.gz.sig
# Keyring used to verify tarball signature.
Source2:        libguestfs.keyring

# Patches (all upstream).
Patch1:         0001-tests-run-qemu-sanity-check-Add-v-flag-for-verbose-m.patch
Patch2:         0002-Add-cpu-option.patch
Patch3:         0003-Set-RAM-to-something-larger-than-qemu-default.patch
Patch4:         0004-Set-console-on-ARM-and-s390.patch

# To verify the tarball signature.
BuildRequires:  gnupg2

BuildRequires:  make
BuildRequires:  gcc

# For building manual pages.
BuildRequires:   /usr/bin/perldoc

# For building the initramfs.
BuildRequires:  cpio
BuildRequires:  glibc-static

# For testing.
BuildRequires:  kernel

# For complicated reasons, this is required so that
# /bin/kernel-install puts the kernel directly into /boot, instead of
# into a /boot/<machine-id> subdirectory (in Fedora >= 23).  Read the
# kernel-install script to understand why.
BuildRequires:  grubby

%ifarch %{ix86} x86_64
Requires:       qemu-system-x86
%global qemu    %{_bindir}/qemu-system-x86_64
%endif
%ifarch armv7hl
Requires:       qemu-system-arm
%global qemu    %{_bindir}/qemu-system-arm
%endif
%ifarch aarch64
Requires:       qemu-system-aarch64
%global qemu    %{_bindir}/qemu-system-aarch64
%endif
%ifarch %{power64}
Requires:       qemu-system-ppc
%global qemu    %{_bindir}/qemu-system-ppc64
%endif
%ifarch %{s390x}
Requires:       qemu-system-s390x
%global qemu    %{_bindir}/qemu-system-s390x
%endif

Requires:       kernel

# Require the -nodeps subpackage.
Requires:       %{name}-nodeps = %{version}-%{release}


%description
Qemu-sanity-check is a short shell script that test-boots a Linux
kernel under qemu, making sure it boots up to userspace.  The idea is
to test the Linux kernel and/or qemu to make sure they are working.

Most users should install the %{name} package.

If you are testing qemu or the kernel in those packages and you want
to avoid a circular dependency on qemu or kernel, you should use
'BuildRequires: %{name}-nodeps' instead.


%package nodeps
Summary:         Simple qemu and Linux kernel sanity checker (no dependencies)
License:         GPLv2+


%description nodeps
This is the no-depedencies version of %{name}.  It is exactly the same
as %{name} except that this package does not depend on qemu or kernel.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1


%build
# NB: canonical_arch is a variable in the final script, so it
# has to be escaped here.
%configure \
%if 0%{?qemu:1}
    --with-qemu-list="%{qemu}" \
%else
    --with-qemu-list="qemu-system-\$canonical_arch" \
%endif
|| {
  cat config.log
  exit 1
}
make %{?_smp_mflags}


%install
make DESTDIR=$RPM_BUILD_ROOT install


%files
%doc COPYING


%files nodeps
%doc COPYING README
%{_bindir}/qemu-sanity-check
%{_libdir}/qemu-sanity-check
%{_mandir}/man1/qemu-sanity-check.1*


%changelog
* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-5
- Rebuild for fixed qemu metapackage.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 25 2020 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-2
- Add some upstream patches to fix aarch64 tests.
- Enable tests on aarch64.

* Thu Sep 10 2020 Richard W.M. Jones <rjones@redhat.com> - 1.1.6-1
- New upstream version 1.1.6.
- Remove all patches.
- Run the tests on some more arches.
- Require qemu-system-<arch>.
- Enable hardened build.
- Enable signed tarball.

* Wed Aug 19 2020 Merlin Mathesius <mmathesi@redhat.com> - 1.1.5-16
- Use ExclusiveArch: %%{kernel_arches}

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-16
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Richard W.M. Jones <rjones@redhat.com> - 1.1.5-13
- Disable on i686 because no kernel package.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Richard W.M. Jones <rjones@redhat.com> - 1.1.5-11
- Add upstream patch to remove deprecated -nodefconfig option.
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Richard W.M. Jones <rjones@redhat.com> - 1.1.5-4
- +BR grubby.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 02 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.5-1
- New upstream version 1.1.5.
- Adds --accel option to select qemu acceleration mode.
- Remove upstream patch.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 28 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.4-2
- New upstream version 1.1.4.
- Remove 3 x patches which are now upstream.
- This version can handle debug kernels (RHBZ#1002189).

* Thu Aug 22 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.3-4
- +BR autoconf, automake.
- Run autoreconf after patching.

* Thu Aug 22 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.3-2
- Fedora kernels don't respond properly to panic=1 parameter (appears
  to be related to having debug enabled).  Add some upstream and one
  non-upstream patches to work around this.

* Thu Aug 22 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.3-1
- Initial release (RHBZ#999108).
