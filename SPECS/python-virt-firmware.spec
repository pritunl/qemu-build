%global pypi_version 0.96

Name:           python-virt-firmware
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Tools for virtual machine firmware volumes

License:        GPLv2
URL:            https://gitlab.com/kraxel/virt-firmware
Source0:        https://gitlab.com/kraxel/virt-firmware/-/archive/v%{pypi_version}/virt-firmware-v%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
Tools for ovmf / armvirt firmware volumes This is a small collection of tools
for edk2 firmware images. They support decoding and printing the content of
firmware volumes. Variable stores (OVMF_VARS.fd) can be modified, for example
to enroll secure boot certificates.

%package -n     python3-virt-firmware
Summary:        %{summary}
%{?python_provide:%python_provide python3-virt-firmware}

Requires:       python3dist(cryptography)
Requires:       python3dist(setuptools)
%description -n python3-virt-firmware
Tools for ovmf / armvirt firmware volumes This is a small collection of tools
for edk2 firmware images. They support decoding and printing the content of
firmware volumes. Variable stores (OVMF_VARS.fd) can be modified, for example
to enroll secure boot certificates.

%prep
%autosetup -n virt-firmware-v%{pypi_version}

%build
%py3_build

%install
%py3_install

%files -n python3-virt-firmware
%license LICENSE
%doc README.md
%{_bindir}/host-efi-vars
%{_bindir}/virt-fw-dump
%{_bindir}/virt-fw-vars
%{python3_sitelib}/virt
%{python3_sitelib}/virt/firmware
%{python3_sitelib}/virt/firmware/efi
%{python3_sitelib}/virt/firmware/varstore
%{python3_sitelib}/virt_firmware-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Mon Apr 11 2022 Gerd Hoffmann <kraxel@redhat.com> - 0.95-1
- Initial package.
