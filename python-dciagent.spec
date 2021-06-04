%global _name python-dciagent
%global _vers VERS

Name:           python3-dciagent
Version:        0.2.0
Release:        1^%{_vers}%{?dist}
Summary:        A python framework for DCI agents
License:        ASL 2.0
URL:            https://github.com/redhat-cip/%{_name}
Source0:        %{_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3-importlib-metadata

%description
This is a python framework to write *agents*: An *agent* is a control script
that will drive the execution of programs, specially for the DCI ecosystem.


%prep
%autosetup -n %{_name}-%{version}


%build
%py3_build


%install
%py3_install


%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/dci-agent-ctl


%changelog
* Mon Feb 28 2022 Jorge A Gallegos <jgallego@redhat.com> - 0.2.0-1
- Initial build
