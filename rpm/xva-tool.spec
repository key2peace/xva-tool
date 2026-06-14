Name:           xva-tool
Version:        1.0.0
Release:        1%{?dist}
Summary:        Enterprise XVA Zero-Copy Streaming Architecture Utility
License:        MIT
URL:            https://github.com
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       python >= 2.7

%description
High-performance cross-platform hypervisor migration and forensic data recovery tool.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp xva-tool $RPM_BUILD_ROOT%{_bindir}/
cp xvapkg $RPM_BUILD_ROOT%{_bindir}/
cp xva-tool.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%files
%{_bindir}/xva-tool
%{_bindir}/xvapkg
%{_mandir}/man1/xva-tool.1*
