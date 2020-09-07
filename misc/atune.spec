%define __global_requires_exclude_from  /usr/libexec

Summary: AI auto tuning system
Name: atune
Version: 0.3
Release: 0.1
License: Mulan PSL v2
URL: https://gitee.com/openeuler/A-Tune
Source: https://gitee.com/openeuler/A-Tune/repository/archive/v%{version}.tar.gz

BuildRequires: rpm-build golang-bin procps-ng
BuildRequires: sqlite >= 3.24.0 openssl
BuildRequires: python3-scikit-optimize python3-pandas python3-xgboost
Requires: systemd
Requires: atune-client
Requires: atune-db
Requires: python3-dict2xml
Requires: python3-flask-restful
Requires: python3-pandas
Requires: prefetch_tuning
Requires: perf
Requires: sysstat
Requires: hwloc-gui
Requires: psmisc

%define  debug_package %{nil}

%description
atune is a service for atuned AI tuning system.

%package client
Summary: client tool for auto tuning system
License: MuLan PSL v2

%description client
atune client tool for manage atuned AI tuning system.

%package db
Summary: database and AI model for auto tuning system
License: MuLan PSL v2

%description db
Database and AI model used by atuned AI tuning system.

%package engine
Summary: engine tool for auto tuning system
License: MuLan PSL v2
Requires: python3-scikit-optimize
Requires: python3-xgboost
Requires: python3-flask-restful
Requires: python3-pandas
Requires: python3-lhsmdu

%description engine
atune engine tool for manage atuned AI tuning system.

%prep
%autosetup -n A-Tune -p1

%build
sed -i "s/^rest_tls.*/rest_tls = false/" misc/atuned.cnf
sed -i "s/^engine_tls.*/engine_tls = false/" misc/atuned.cnf
sed -i "s/^engine_tls.*/engine_tls = false/" misc/engine.cnf
make models
%make_build

%install
%make_install

%check

%files
%license License/LICENSE
%defattr(0640,root,root,-)
%attr(0640,root,root) /usr/lib/atuned/modules/daemon_profile_server.so
%attr(0640,root,root) %{_unitdir}/atuned.service
%attr(0750,root,root) %{_bindir}/atuned
%attr(0750,root,root) /usr/libexec/atuned/scripts/*
%attr(0750,root,root) /usr/libexec/atuned/analysis/*
%attr(0640,root,root) /usr/lib/atuned/profiles/*
%exclude /usr/libexec/atuned/analysis/app_engine.py
%exclude /usr/libexec/atuned/analysis/models/
%exclude /usr/libexec/atuned/analysis/optimizer/
%exclude /usr/libexec/atuned/analysis/engine/
%attr(0750,root,root) %dir /usr/lib/atuned
%attr(0750,root,root) %dir /usr/lib/atuned/modules
%attr(0750,root,root) %dir /usr/lib/atuned/profiles
%attr(0750,root,root) %dir /usr/libexec/atuned
%attr(0750,root,root) %dir /usr/libexec/atuned/scripts
%attr(0750,root,root) %dir /usr/libexec/atuned/analysis
%attr(0750,root,root) %dir /usr/share/atuned
%attr(0750,root,root) %dir /etc/atuned
%attr(0750,root,root) %dir /etc/atuned/rules
%attr(0750,root,root) %dir /var/atuned
%attr(0640,root,root) /etc/atuned/atuned.cnf
%exclude /etc/atuned/engine_certs/*
%exclude /etc/atuned/rest_certs/*

%files client
%attr(0750,root,root) %{_bindir}/atune-adm
%attr(0640,root,root) /usr/share/bash-completion/completions/atune-adm

%files db
%attr(0750,root,root) %dir /var/lib/atuned
%attr(0750,root,root) %dir /var/run/atuned
%attr(0750,root,root) /var/lib/atuned/atuned.db
%attr(0750,root,root) %dir /usr/libexec/atuned
%attr(0750,root,root) %dir /usr/libexec/atuned/analysis
%attr(0750,root,root) %dir /usr/libexec/atuned/analysis/models
%attr(0750,root,root) /usr/libexec/atuned/analysis/models/*

%files engine
%license License/LICENSE
%defattr(0640,root,root,-)
%attr(0640,root,root) %{_unitdir}/atune-engine.service
%attr(0750,root,root) /usr/libexec/atuned/analysis/*
%attr(0750,root,root) /usr/libexec/atuned/resources/*
%attr(0750,root,root) /etc/atuned/*
%exclude /usr/libexec/atuned/analysis/app.py
%exclude /usr/libexec/atuned/analysis/plugin/
%exclude /usr/libexec/atuned/analysis/atuned/
%attr(0750,root,root) %dir /usr/libexec/atuned/analysis
%attr(0750,root,root) %dir /usr/libexec/atuned/resources
%attr(0750,root,root) %dir /etc/atuned
%exclude /etc/atuned/atuned.cnf
%exclude /etc/atuned/rules
%exclude /etc/atuned/engine_certs/*
%exclude /etc/atuned/rest_certs/*

%post
%systemd_post atuned.service

%preun
%systemd_preun atuned.service

%postun
%systemd_postun_with_restart atuned.service

%changelog
* Fri Sep 4 2020 Zhipeng Xie<xiezhipeng1@huawei.com> - 0.3-0.1
- upgrade to v0.3

* Thu Mar 19 2020 openEuler Buildteam <buildteam@openeuler.org> - 0.2-0.1
- Package init

* Tue Nov 12 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.1-0.1
- Package init
