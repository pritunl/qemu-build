Name:          dtc
Version:       1.6.0
Release:       1%{?dist}
Summary:       Device Tree Compiler
Group:          Development/Tools
License:       GPLv2+
URL:           https://devicetree.org/
Source:        https://github.com/dgibson/dtc/archive/v%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires: gcc make
BuildRequires: flex bison

%description
Devicetree is a data structure for describing hardware. Rather than hard coding
every detail of a device into an operating system, many aspects of the hardware
can be described in a data structure that is passed to the operating system at
boot time. The devicetree is used by OpenFirmware, OpenPOWER Abstraction Layer
(OPAL), Power Architecture Platform Requirements (PAPR) and in the standalone
Flattened Device Tree (FDT) form.

%package -n libfdt
Summary: Device tree library
Group: Development/Libraries

%description -n libfdt
libfdt is a library to process Open Firmware style device trees on various
architectures.

%package -n libfdt-devel
Summary: Development headers for device tree library
Group: Development/Libraries
Requires: libfdt = %{version}-%{release}

%description -n libfdt-devel
This package provides development files for libfdt

%prep
%setup -q -n dtc-%{version}


%build
make %{?_smp_mflags} V=1 CC="gcc $RPM_OPT_FLAGS $RPM_LD_FLAGS" NO_PYTHON=1

%install
make install DESTDIR=$RPM_BUILD_ROOT SETUP_PREFIX=$RPM_BUILD_ROOT/usr PREFIX=/usr LIBDIR=%{_libdir} NO_PYTHON=1
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.a

# we don't want or need ftdump and it conflicts with freetype-demos, so drop
# it (rhbz 797805)
rm -f $RPM_BUILD_ROOT/%{_bindir}/ftdump

%post -n libfdt -p /sbin/ldconfig

%postun -n libfdt -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license GPL
%doc Documentation/manual.txt
%{_bindir}/*

%files -n libfdt
%defattr(-,root,root,-)
%license GPL
%{_libdir}/libfdt-%{version}.so
%{_libdir}/libfdt.so.*

%files -n libfdt-devel
%defattr(-,root,root,-)
%{_libdir}/libfdt.so
%{_includedir}/*

%changelog
* Fri Apr 17 2020 Miroslav Rezanina <mrezanin@redhat.com> - 1.6.0-1
- Use 1.6.0 version [bz#1679676]
- Resolves: bz#1679676
  (dtc changes blocked until gating tests are added)

* Thu Aug 09 2018 Miroslav Rezanina <mrezanin@redhat.com> - 1.4.6-1
- Updated for RHEL 8 [bz#1518440]
- Resolves: bz#1518440
  (Prepare dtc for RHEL-8.0 )

* Mon Mar 06 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.4.3-1
- Rebase to 1.4.3 [bz#1427157]
- Resolves: bz#1427157
  (package libfdt 1.4.3, when available)

* Tue Aug 19 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.4.0-2
- Update power macro for ppc64le

* Fri Jul 25 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.4.0-1
- Initial version

