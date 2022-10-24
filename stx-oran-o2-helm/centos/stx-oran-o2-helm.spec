# Application tunables (maps to metadata)
%global app_name oran-o2
%global helm_repo stx-platform
%global fluxcd_o2_version 2.0.0

# Install location
%global app_folder /usr/local/share/applications/helm

# Build variables
%global helm_folder /usr/lib/helm
%global toolkit_version 0.1.0

Summary: StarlingX O-ORAN O2 Application FluxCD Helm Charts
Name: stx-oran-o2-helm
Version: 2.0.0
Release: %{tis_patch_ver}%{?_tis_dist}
License: Apache-2.0
Group: base
Packager: Wind River <info@windriver.com>
URL: unknown

Source0: %{name}-%{version}.tar.gz

Source1: oran-o2-%{fluxcd_o2_version}.tar.gz

BuildArch: noarch

BuildRequires: helm
BuildRequires: chartmuseum
#BuildRequires: python-k8sapp-oran-o2
#BuildRequires: python-k8sapp-oran-o2-wheels

%description
StarlingX O-ORAN O2 Application FluxCD Helm Charts

%prep
%setup
# set up fluxcd tar source
cd %{_builddir}
mkdir -p oran-o2
/usr/bin/tar -C oran-o2 --strip-components=1 -xfv %{SOURCE1}

%build
# Host a server for the charts
cd %{_builddir}/oran-o2
chartmuseum --debug --port=8879 --context-path='/charts' --storage="local" --storage-local-rootdir="." &
sleep 2
helm repo add local http://localhost:8879/charts

# Make Chart
mkdir -p %{_builddir}/oran-o2/o2-charts
mv %{_builddir}/oran-o2/charts/* %{_builddir}/oran-o2/o2-charts
mv %{_builddir}/oran-o2/o2-charts %{_builddir}/oran-o2/charts/oran-o2
cd %{_builddir}/stx-oran-o2-helm-%{version}
cp files/Makefile %{_builddir}/oran-o2/charts
cd %{_builddir}/oran-o2/charts
make oran-o2

# Terminate helm server (the last backgrounded task)
kill %1

# Create a chart tarball compliant with sysinv kube-app.py
%define app_staging %{_builddir}/staging
%define app_tarball_fluxcd %{app_name}-%{version}-%{tis_patch_ver}.tgz

# Setup staging
mkdir -p %{app_staging}
cd %{_builddir}/stx-oran-o2-helm-%{version}
cp files/metadata.yaml %{app_staging}
cp -Rv fluxcd-manifests %{app_staging}/
mkdir -p %{app_staging}/charts

cd %{_builddir}/oran-o2
cp charts/*.tgz %{app_staging}/charts
cd %{app_staging}

# Populate metadata
sed -i 's/@APP_NAME@/%{app_name}/g' %{app_staging}/metadata.yaml
sed -i 's/@APP_VERSION@/%{version}-%{tis_patch_ver}/g' %{app_staging}/metadata.yaml
sed -i 's/@HELM_REPO@/%{helm_repo}/g' %{app_staging}/metadata.yaml

# Copy the plugins: installed in the buildroot
#mkdir -p %{app_staging}/plugins
#cp /plugins/%{app_name}/*.whl %{app_staging}/plugins

find . -type f ! -name '*.md5' -print0 | xargs -0 md5sum > checksum.md5
tar -zcf %{_builddir}/%{app_tarball_fluxcd} -C %{app_staging}/ .

# Cleanup staging
rm -fr %{app_staging}

%install
install -d -m 755 %{buildroot}/%{app_folder}
install -p -D -m 755 %{_builddir}/%{app_tarball_fluxcd} %{buildroot}/%{app_folder}

%files
%defattr(-,root,root,-)
%{app_folder}/%{app_tarball_fluxcd}
