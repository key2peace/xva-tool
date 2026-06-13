Name:           xva-tool
Version:        1.0.0
Release:        1%{?dist}
Summary:        Advanced Zero-Copy Streaming Core Engine for XenServer
License:        MIT
URL:            https://github.com
BuildArch:      noarch
Requires:       python27, python27-libs

%description
An enterprise-grade standalone utility core for Citrix XenServer XVA/OVA images designed by Alexander Maassen. Extracts and flattens XenServer XVA/OVA image streams into flat raw disk structures using a pure, zero-dependency Python 2.7 framework core.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 755 %{_sourcedir}/xva-tool $RPM_BUILD_ROOT%{_bindir}/xva-tool
install -m 755 %{_sourcedir}/xvapkg $RPM_BUILD_ROOT%{_bindir}/xvapkg
install -m 644 %{_sourcedir}/xva-tool.1 $RPM_BUILD_ROOT%{_mandir}/man1/xva-tool.1

%files
%{_bindir}/xva-tool
%{_bindir}/xvapkg
%{_mandir}/man1/xva-tool.1.gz
