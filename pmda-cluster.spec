
Name: pcp-pmda-cluster
URL: http://oss.sgi.com/projects/pcp
Summary: Performance Co-Pilot (PCP) PMDA for clusters
Version: 1.0
Release: 1
Group: Productivity/Networking
Vendor: SGI Inc.
Packager: SGI Inc. <http://www.sgi.com/>
License: GPL

Requires: pcp >= 3.0.1
BuildRequires: pcp >= 3.0.1 pcp-pmda-infiniband pcp-libs-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Source0: %{name}-%{version}.tar.bz2

%define pcp_pmdas_dir %( . /etc/pcp.conf ; echo $PCP_PMDAS_DIR )
%define pcp_binadm_dir %( . /etc/pcp.conf ; echo $PCP_BINADM_DIR )
%define pcp_rc_dir %( . /etc/pcp.conf ; echo $PCP_RC_DIR )

%description
This package contains the PMDA for collecting metrics from a
cluster of nodes using a "push" model, rather than the PMCD polling
other nodes.  It is useful for clusters where extra overhead from
running daemons is unacceptable.

%package client
Summary: Performance Co-Pilot (PCP) cluster PMDA client daemon
URL: http://oss.sgi.com/projects/pcp
Group: Productivity/Networking
Vendor: SGI Inc.
Packager: SGI Inc. <http://www.sgi.com/>
License: GPL

Requires: pcp >= 3.0.1

%description client
This is the client daemon for the Performance Co-Pilot (PCP) cluster
PMDA.


%prep
%setup -q

%build
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pcp_pmdas_dir}/cluster
make install PREFIX=%{buildroot}

%clean
rm -rf %{buildroot}

%preun
cd %{pcp_pmdas_dir}/cluster;
./Remove

%files
%defattr(-,root,root)
%{pcp_pmdas_dir}/cluster/pmdacluster
%{pcp_pmdas_dir}/cluster/Install
%{pcp_pmdas_dir}/cluster/Remove
%config(noreplace) %{pcp_pmdas_dir}/cluster/config
%doc %{pcp_pmdas_dir}/cluster/README
%{pcp_pmdas_dir}/cluster/pmns
%{pcp_pmdas_dir}/cluster/root
%{pcp_pmdas_dir}/cluster/help
%{pcp_pmdas_dir}/cluster/domain.h

%files client
%defattr(-,root,root)
%{pcp_binadm_dir}/pmclusterd
%{pcp_rc_dir}/pmclusterd
