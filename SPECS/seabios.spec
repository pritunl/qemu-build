Name:           seabios
Version:        1.16.0
Release:        3%{?dist}
Summary:        Open-source legacy BIOS implementation

Group:          Applications/Emulators
License:        LGPLv3
URL:            https://www.coreboot.org/SeaBIOS

Source0:        https://code.coreboot.org/p/seabios/downloads/get/seabios-1.16.0.tar.gz

Source10:       config.vga.cirrus
Source11:       config.vga.qxl
Source12:       config.vga.stdvga
Source13:       config.vga.virtio
Source14:       config.vga.ramfb
Source15:       config.vga.bochs-display

Source20:       config.seabios-128k
Source21:       config.seabios-256k

Patch0002: 0002-allow-1TB-of-RAM.patch
Patch0003: 0003-smbios-set-bios-vendor-version-fields-to-Seabios-0.5.patch
Patch0004: 0004-Workaround-for-a-win8.1-32-S4-resume-bug.patch
# For bz#2073012 - Guest whose os is installed multiple disks but boot partition is installed on single disk can't boot into OS on RHEL 8 [rhel-8.7.0]
Patch5: seabios-shortcut-skip-unbootable-disks-optimitation.patch
# For bz#2083884 - qemu reboot problem with seabios 1.16.0
Patch6: seabios-pci-refactor-the-pci_config_-functions.patch
# For bz#2083884 - qemu reboot problem with seabios 1.16.0
Patch7: seabios-reset-force-standard-PCI-configuration-access.patch
# For bz#2101787 - [rhel.8.7] Loading a kernel/initrd is sometimes very slow
Patch8: seabios-virtio-blk-use-larger-default-request-size.patch

BuildRequires: python3 iasl
ExclusiveArch: x86_64 %{power64}

Requires: %{name}-bin = %{version}-%{release}
Requires: seavgabios-bin = %{version}-%{release}

# Seabios is noarch, but required on architectures which cannot build it.
# Disable debuginfo because it is of no use to us.
%global debug_package %{nil}

# Similarly, tell RPM to not complain about x86 roms being shipped noarch
%global _binaries_in_noarch_packages_terminate_build   0

# You can build a debugging version of the BIOS by setting this to a
# value > 1.  See src/config.h for possible values, but setting it to
# a number like 99 will enable all possible debugging.  Note that
# debugging goes to a special qemu port that you have to enable.  See
# the SeaBIOS top-level README file for the magic qemu invocation to
# enable this.
%global debug_level 1


%description
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.


%package bin
Summary: Seabios for x86
Buildarch: noarch


%description bin
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.


%package -n seavgabios-bin
Summary: Seavgabios for x86
Buildarch: noarch
Obsoletes: vgabios < 0.6c-10

%description -n seavgabios-bin
SeaVGABIOS is an open-source VGABIOS implementation.


%prep
%setup -q
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
%ifarch x86_64
export CFLAGS="$RPM_OPT_FLAGS"
mkdir binaries

build_bios() {
    make PYTHON=%{__python3} clean distclean
    cp $1 .config
    echo "CONFIG_DEBUG_LEVEL=%{debug_level}" >> .config
    make PYTHON=%{__python3} oldnoconfig V=1 EXTRAVERSION="-%release"

    make PYTHON=%{__python3} \
        V=1 \
        $4 \
        EXTRAVERSION="-%{release}" \

    cp out/$2 binaries/$3
}

# seabios
build_bios %{_sourcedir}/config.seabios-128k bios.bin bios.bin
build_bios %{_sourcedir}/config.seabios-256k bios.bin bios-256k.bin


# seavgabios
%global vgaconfigs cirrus qxl stdvga virtio ramfb bochs-display
for config in %{vgaconfigs}; do
    build_bios %{_sourcedir}/config.vga.${config} \
               vgabios.bin vgabios-${config}.bin out/vgabios.bin
done


%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/seabios
mkdir -p $RPM_BUILD_ROOT%{_datadir}/seavgabios
install -m 0644 binaries/bios.bin $RPM_BUILD_ROOT%{_datadir}/seabios/bios.bin
install -m 0644 binaries/bios-256k.bin $RPM_BUILD_ROOT%{_datadir}/seabios/bios-256k.bin
install -m 0644 binaries/vgabios*.bin $RPM_BUILD_ROOT%{_datadir}/seavgabios


%files
%doc COPYING COPYING.LESSER README


%files bin
%dir %{_datadir}/seabios/
%{_datadir}/seabios/bios*.bin

%files -n seavgabios-bin
%dir %{_datadir}/seavgabios/
%{_datadir}/seavgabios/vgabios*.bin

# endif for %ifarch x86_64 {power64}
%endif


%changelog
* Wed Jul 27 2022 Miroslav Rezanina <mrezanin@redhat.com> - 1.16.0-3
- seabios-virtio-blk-use-larger-default-request-size.patch [bz#2101787]
- Resolves: bz#2101787
  ([rhel.8.7] Loading a kernel/initrd is sometimes very slow)

* Mon May 30 2022 Jon Maloy <jmaloy@redhat.com> - 1.16.0-2
- seabios-shortcut-skip-unbootable-disks-optimitation.patch [bz#2073012]
- seabios-pci-refactor-the-pci_config_-functions.patch [bz#2083884]
- seabios-reset-force-standard-PCI-configuration-access.patch [bz#2083884]
- Resolves: bz#2073012
  (Guest whose os is installed multiple disks but boot partition is installed on single disk can't boot into OS on RHEL 8 [rhel-8.7.0])
- Resolves: bz#2083884
  (qemu reboot problem with seabios 1.16.0)

* Tue Apr 26 2022 Paweł Poławski <ppolawsk@redhat.com> - 1.16.0-1
- Rebase to upstream 1.16 tag [bz#2066828]
- Resolves: bz#2066828
  (rebase seabios to 1.16 release)

* Thu Dec 16 2021 Jon Maloy <jmaloy@redhat.com> - 1.15.0-1.el8
- Rebase to 1.15 (bz#2018392)
- Resolves: bz#2018392

* Thu Dec 16 2021 Jon Maloy <jmaloy@redhat.com> - 1.15.0-1.el8
- pci-reserve-resources-for-pcie-pci-bridge-to-fix-reg.patch [bz#2001921]
- pci: let firmware reserve IO for pcie-pci-bridge.patch [bz#2001921]
- Resolves: bz#2001921

* Tue Aug 11 2020 Miroslav Rezanina <mrezanin@redhat.com> - 1.14.0-1.el8
- Rebase to 1.14 (bz#1809772)
- Resolves: bz#1809772
  (rebase seabios for RHEL AV-8.3.0)

* Tue Jan 21 2020 Miroslav Rezanina <mrezanin@redhat.com> - 1.13.0-1.el8
- Rebase to 1.13 (bz#1793377)
- Resolves: bz#1793377
  (rebase seabios to 1.13)

* Tue Aug 20 2019 Danilo Cesar Lemes de Paula <ddepaula@redhat.com> - 1.12.0-5.el8
- seabios-add-get_keystroke_full-helper.patch [bz#1693031]
- seabios-bootmenu-add-support-for-more-than-9-entries.patch [bz#1693031]
- Resolves: bz#1693031
  (On systems with more than 10 available boot devices, keys are uninintuitive)

* Fri Aug 02 2019 Danilo Cesar Lemes de Paula <ddepaula@redhat.com> - 1.12.0-4.el8
- seabios-tpm-Check-for-TPM-related-ACPI-tables-before-attempt.patch [bz#1705212]
- seabios-usb-ehci-Clear-pipe-token-on-pipe-reallocate.patch [bz#1705212]
- Resolves: bz#1705212
  (Backport 1.12.1 patches to RHEL-AV 8.1.0)

* Tue Jul 09 2019 Miroslav Rezanina <mrezanin@redhat.com> - 1.12.0-3.el8
- seabios-rh-add-configs-for-ramfb-and-bochs-display.patch [bz#1724098]
- Resolves: bz#1724098
  (enable device: bochs-display (seabios))

* Mon Jan 21 2019 Miroslav Rezanina <mrezanin@redhat.com> - 1.12.0-1.el8
- Rebase to 1.12.0 [bz#1666134]
- Resolves: bz#1666134
  (Rebase seabios for RHEL-AV release in virt:8.0.0 stream)

* Fri Dec 07 2018 Danilo C. L. de Paula <ddepaula@redhat.com> - 1.11.1-3.el8
- Resolves: bz#1613465
  (Fix seabios package)

* Fri Aug 24 2018 Danilo C. L. de Paula <ddepaula@redhat.com> - 1.11.1-2.el8
- Resolves: bz#1607349
  (Serial Graphics Adapter show error seabios version)

* Thu Jul 12 2018 Danilo C. L. de Paula <ddepaula@redhat.com> - 1.11.1-1.el8
- Rebasing seabios 1.11.1

* Mon May 21 2018 Danilo C. L. de Paula <ddepaula@redhat.com> - 1.11.0-2.el8
- Syncronizing exploded tree with dist-git

* Mon Nov 20 2017 Danilo C. L. de Paula <ddepaula@redhat.com> - 1.11.0-1.el8
- Creating RHEL-8.0 initial branch based on 1.11.0
- Resolves: bz#1515300
- (Prepare seabios for RHEL-8.0)

* Fri Nov 17 2017 Paolo Bonzini <pbonzini@redhat.com> - 1.11.0-1
- Rebased to version 1.11.0
- Add three patches from RHEL

* Fri Nov 17 2017 Paolo Bonzini <pbonzini@redhat.com> - 1.10.2-3
- Disable cross-compilation on RHEL

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 15 2017 Cole Robinson <crobinso@redhat.com> - 1.10.2-1
- Rebased to version 1.10.2

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 04 2016 Cole Robinson <crobinso@redhat.com> - 1.10.1-1
- Rebased to version 1.10.1

* Wed Aug 03 2016 Cole Robinson <crobinso@redhat.com> - 1.9.3-1
- Rebased to version 1.9.3

* Thu Mar 24 2016 Paolo Bonzini <pbonzini@redhat.com> - 1.9.1-3
- Include MPT Fusion driver, in preparation for QEMU 2.6
- Include XHCI and SD in 128k ROM, sacrifice bootsplash instead

* Thu Mar 17 2016 Cole Robinson <crobinso@redhat.com> - 1.9.1-1
- Rebased to version 1.9.1
- Fix incorrect UUID format in boot output (bz #1284259)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 17 2015 Cole Robinson <crobinso@redhat.com> 1.9.0-1
- Rebased to version 1.9.0

* Tue Jul 14 2015 Cole Robinson <crobinso@redhat.com> 1.8.2-1
- Rebased to version 1.8.2

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 18 2015 Cole Robinson <crobinso@redhat.com> - 1.8.1-1
- Rebased to version 1.8.1

* Sat Feb 21 2015 Cole Robinson <crobinso@redhat.com> - 1.8.0-1
- Rebased to version 1.8.0
- Initial support for USB3 hubs
- Initial support for SD cards (on QEMU only)
- Initial support for transitioning to 32bit mode using SMIs (on QEMU TCG
  only)
- SeaVGABIOS improvements

* Sat Nov 15 2014 Cole Robinson <crobinso@redhat.com> - 1.7.5.1-1
- Update to seabios-1.7.5.1

* Wed Jul 09 2014 Cole Robinson <crobinso@redhat.com> - 1.7.5-3
- Fix PCI-e hotplug (bz #1115598)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 31 2014 Cole Robinson <crobinso@redhat.com> - 1.7.5-1
- Rebased to version 1.7.5
- Support for obtaining SMBIOS tables directly from QEMU.
- XHCI USB controller fixes for real hardware
- seavgabios: New driver for "coreboot native vga" support
- seavgabios: Improved detection of x86emu versions with incorrect
  emulation.
- Several bug fixes and code cleanups

* Wed Mar 26 2014 Matthias Clasen <mclasen@redhat.com> 1.7.4-5
- Fix booting FreeBSD VMs in virt-manager

* Mon Mar 17 2014 Cole Robinson <crobinso@redhat.com> 1.7.4-3
- Build 256k bios images for qemu 2.0

* Thu Mar 13 2014 Cole Robinson <crobinso@redhat.com> - 1.7.4-2
- Fix kvm migration with empty virtio-scsi controller (bz #1032208)

* Mon Jan 06 2014 Cole Robinson <crobinso@redhat.com> - 1.7.4-1
- Rebased to version 1.7.4
- Support for obtaining ACPI tables directly from QEMU.
- Initial support for XHCI USB controllers (initially for QEMU only).
- Support for booting from "pvscsi" devices on QEMU.
- Enhanced floppy driver - improved support for real hardware.
- coreboot cbmem console support.

* Tue Nov 19 2013 Cole Robinson <crobinso@redhat.com> - 1.7.3.2-1
- Update to 1.7.3.2 for qemu 1.7

* Thu Nov 14 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.3.1-3
- Fix pasto in CONFIG_DEBUG_LEVEL.

* Thu Nov 14 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.3.1-2
- Compile as all three of BIOS, CSM and CoreBoot payload.

* Wed Aug 14 2013 Cole Robinson <crobinso@redhat.com> - 1.7.3.1-1
- Rebased to version 1.7.3.1
- Fix USB EHCI detection that was broken in hlist conversion of
  PCIDevices.
- Fix bug in CBFS file walking with compressed files.
- acpi: sync FADT flags from PIIX4 to Q35

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Cole Robinson <crobinso@redhat.com> - 1.7.3-2
- Install aml files for use by qemu

* Mon Jul 08 2013 Cole Robinson <crobinso@redhat.com> - 1.7.3-1
- Rebased to version 1.7.3
- Initial support for using SeaBIOS as a UEFI CSM
- Support for detecting and using ACPI reboot ports.
- Non-standard floppy sizes now work again with recent QEMU versions.
- Several bug fixes and code cleanups
- Again fix vgabios obsoletes (bz #981147)

* Mon May 27 2013 Cole Robinson <crobinso@redhat.com> - 1.7.2.2-1
- Update to seabios stable 1.7.2.2
- Obsolete vgabios (bz #967315)

* Thu Jan 24 2013 Cole Robinson <crobinso@redhat.com> - 1.7.2-1
- Rebased to version 1.7.2
- Support for ICH9 host chipset ("q35") on emulators
- Support for booting from LSI MegaRAID SAS controllers
- Support for using the ACPI PM timer on emulators
- Improved Geode VGA BIOS support.
- Several bug fixes

* Thu Dec  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.1-4
- Root seabios package is noarch too because it only contains docs

* Fri Oct 19 2012 Cole Robinson <crobinso@redhat.com> - 1.7.1-3
- Add seavgabios subpackage

* Wed Oct 17 2012 Paolo Bonzini <pbonzini@redhat.com> - 1.7.1-2
- Build with cross compiler.  Resolves: #866664.

* Wed Sep 05 2012 Cole Robinson <crobinso@redhat.com> - 1.7.1-1
- Rebased to version 1.7.1
- Initial support for booting from USB attached scsi (USB UAS) drives
- USB EHCI 64bit controller support
- USB MSC multi-LUN device support
- Support for booting from LSI SCSI controllers on emulators
- Support for booting from AMD PCscsi controllers on emulators

* Mon Aug 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-4
- Modernise and tidy up the RPM.
- Allow debug versions of SeaBIOS to be built easily.

* Mon Aug 06 2012 Cole Robinson <crobinso@redhat.com> - 1.7.0-3
- Enable S3/S4 support for guests (it's an F18 feature after all)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Cole Robinson <crobinso@redhat.com> - 1.7.0-1
- Rebased to version 1.7.0
- Support for virtio-scsi
- Improved USB drive support
- Several USB controller bug fixes and improvements

* Wed Mar 28 2012 Paolo Bonzini <pbonzini@redhat.com> - 1.6.3-2
- Fix bugs in booting from host (or redirected) USB pen drives

* Wed Feb 08 2012 Justin M. Forbes <jforbes@redhat.com> - 1.6.3-1
- Update to 1.6.3 upstream
- Add virtio-scsi

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 05 2011 Justin M. Forbes <jforbes@redhat.com> - 0.6.2-3
- Stop advertising S3 and S4 in DSDT (bz#741375)
- incdule iasl buildreq

* Wed Jul 13 2011 Justin M. Forbes <jforbes@redhat.com> - 0.6.2-2
- Fix QXL bug in 0.6.2

* Wed Jul 13 2011 Justin M. forbes <jforbes@redhat.com> - 0.6.2-1
- Update to 0.6.2 upstream for a number of bugfixes

* Mon Feb 14 2011 Justin M. forbes <jforbes@redhat.com> - 0.6.1-1
- Update to 0.6.1 upstream for a number of bugfixes

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 10 2010 Justin M. Forbes <jforbes@redhat.com> 0.6.0-1
- Update seabios to latest stable so we can drop patches.

* Tue Apr 20 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-2
- Ugly hacks to make package noarch and available for arch that cannot build it.
- Disable useless debuginfo

* Wed Mar 03 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-1
- Update to 0.5.1 stable release
- Pick up patches required for current qemu

* Thu Jan 07 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-0.1.20100108git669c991
- Created initial package
