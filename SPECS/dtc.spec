Name:          dtc
Version:       1.6.1
Release:       2%{?dist}
Summary:       Device Tree Compiler
License:       GPLv2+
URL:           https://devicetree.org/

Source0:       https://www.kernel.org/pub/software/utils/%{name}/%{name}-%{version}.tar.xz

BuildRequires: gcc make
BuildRequires: flex bison swig
BuildRequires: python3-devel python3-setuptools

%description
Devicetree is a data structure for describing hardware. Rather than hard coding
every detail of a device into an operating system, many aspects of the hardware
can be described in a data structure that is passed to the operating system at
boot time. The devicetree is used by OpenFirmware, OpenPOWER Abstraction Layer
(OPAL), Power Architecture Platform Requirements (PAPR) and in the standalone
Flattened Device Tree (FDT) form.

%package -n libfdt
Summary: Device tree library

%description -n libfdt
libfdt is a library to process Open Firmware style device trees on various
architectures.

%package -n libfdt-devel
Summary: Development headers for device tree library
Requires: libfdt = %{version}-%{release}

%description -n libfdt-devel
This package provides development files for libfdt

%package -n libfdt-static
Summary: Static version of device tree library
Requires: libfdt-devel = %{version}-%{release}

%description -n libfdt-static
This package provides the static library of libfdt

%package -n python3-libfdt
Summary: Python 3 bindings for device tree library
%{?python_provide:%python_provide python2-libfdt}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n python3-libfdt
This package provides python2 bindings for libfdt

%prep
%autosetup -p1
sed -i 's/python2/python3/' pylibfdt/setup.py

%build
%{make_build} EXTRA_CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"

%install
%{make_install} DESTDIR=$RPM_BUILD_ROOT PREFIX=$RPM_BUILD_ROOT/usr \
                LIBDIR=%{_libdir} BINDIR=%{_bindir} INCLUDEDIR=%{_includedir}

# we don't want ftdump and it conflicts with freetype-demos, so drop it (rhbz 797805)
rm -f $RPM_BUILD_ROOT/%{_bindir}/ftdump

%ldconfig_scriptlets -n libfdt

%files
%license GPL
%doc Documentation/manual.txt
%{_bindir}/*

%files -n libfdt
%license GPL
%{_libdir}/libfdt-%{version}.so
%{_libdir}/libfdt.so.*

%files -n libfdt-static
%{_libdir}/libfdt.a

%files -n libfdt-devel
%{_libdir}/libfdt.so
%{_includedir}/*

%files -n python3-libfdt
%{python3_sitearch}/*

%changelog
* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.6.0-5
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.6.0-2
- Rebuilt for Python 3.9

* Fri Mar 13 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0

* Thu Jan 30 2020 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.1-4
- Upstream patch to fix gcc-10 build

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Tom Stellard <tstellar@redhat.com> - 1.5.1-2
- Use __cc macro instead of hard-coding gcc

* Wed Sep 11 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.1-1
- New dtc 1.5.1 release

* Tue Sep 10 2019 Miro Hrončok <mhroncok@redhat.com> - 1.5.0-3
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 12 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.0-1
- New dtc 1.5.0 release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.7-2
- Upstream fix for crash (rhbz 1663054)

* Sat Aug 18 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.7-1
- New dtc 1.4.7 release

* Tue Jul 17 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.6-7
- Update Python macros to new packaging standards
  (See https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 06 2018 Bas Mevissen <abuse@basmevissen.nl> 1.4.6-5
- Add static library package, see BZ#1440975

* Wed Mar  7 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.6-4
- Add gcc BR

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Florian Weimer <fweimer@redhat.com> - 1.4.6-2
- Use Fedora build flags during build

* Mon Jan 22 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.6-1
- New dtc 1.4.6 release

* Thu Sep 28 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.5-1
- New dtc 1.4.5 release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.4-2
- Add upstream patches for python bindings

* Fri Mar 17 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.4-1
- New dtc 1.4.4 release

* Tue Feb 28 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.2-3.0931cea
- Rebase to same git snapshot that kernel is using for DT Overlays

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Sep 11 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.2-1
- New dtc 1.4.2 release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.1-4
- Use %%license

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.4.1-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Jan  5 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.1-2
- Use tar file from kernel.org

* Mon Jan  5 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.1-1
- New dtc 1.4.1 release
- Update URL and Sources
- Cleanup spec

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.4.0-3
- Avoid shell invocation and fix deps of libfdt %%post* scripts.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Josh Boyer <jwboyer@redhat.com> - 1.4.0-1
- New dtc 1.4.0 release (rhbz 977480)

* Thu Jun 06 2013 Josh Boyer <jwboyer@redhat.com> - 1.3.0-8
- Fix type specifier error (from Dan Horák)

* Mon Jun 03 2013 Josh Boyer <jwboyer@redhat.com> - 1.3.0-7
- Update dtc to include libfdt_env.h (rhbz 969955)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Josh Boyer <jwboyer@redhat.com>
- Don't package ftdump (rhbz 797805)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Josh Boyer <jwboyer@gmail.com>
- Fixup error during tarball upload

* Tue Jun 28 2011 Josh Boyer <jwboyer@gmail.com>
- Point to git tree for URL (#717217)
- Add libfdt subpackages based on patch from Paolo Bonzini (#443882)
- Update to latest release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Josh Boyer <jwboyer@gmail.com>
- Update to latest release

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.0-2
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Josh Boyer <jwboyer@gmail.com>
- Update to 1.1.0

* Tue Aug 21 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Bump and rebuild

* Thu Aug 09 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Update to official 1.0.0 release

* Fri Aug 03 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Update license field

* Mon Jul 09 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Update to new snapshot

* Tue Jul 03 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Update to new snapshot
- Drop upstreamed install patch

* Fri Jun 29 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Fix packaging errors

* Thu Jun 28 2007 Josh Boyer <jwboyer@jdub.homelinux.org>
- Initial packaging
