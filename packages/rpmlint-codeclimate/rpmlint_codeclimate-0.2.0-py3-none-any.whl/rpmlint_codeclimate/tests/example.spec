%define srcname example-project
%define distname %{lua:name = string.gsub(rpm.expand("%{srcname}"), "-", "_"); print(name)}
%define version 0.0.0
%define release 1

Name:     python-%{srcname}
Version:  %{version}
Release:  %{release}%{?dist}
Summary:  Example spec file for rpmlint-codeclimate

License:  MIT
Url:      https://gitlab.com/duncanmmacleod/rpmlint-codeclimate
Source0:  %pypi_source %distname

Packager: Duncan Macleod <macleoddm@cardiff.ac.uk>
Vendor:   Duncan Macleod <macleoddm@cardiff.ac.uk>

BuildArch: noarch

BuildRequires: python3-devel >= 3.6
BuildRequires: python3dist(pip)
BuildRequires: python3dist(setuptools)
BuildRequires: python3dist(setuptools-scm)
BuildRequires: python3dist(wheel)
# for tests
BuildRequires: python3dist(pytest)
BuildRequires: python3dist(requests-mock)

%description
This package is an example project binary package that should not be
distributed or installed on any systems save for the purpose of testing
and validation of the parent GitLab CI/CD component project.

%package -n python3-%{srcname}
Summary: Example project for Red Hat CI/CD component - Python %{python3_version} library
Obsoletes: other-example-package
%description -n python3-%{srcname}
Python %{python3_version} library for example project.

%prep
%autosetup -n %{distname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%check
export PYTHONPATH="%{buildroot}%{python3_sitelib}"
%{__python3} -m pip show %{srcname} -f
%{__python3} -m pytest --verbose -ra --pyargs example_project

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

%changelog
* Fri Apr 26 2024 Duncan Macleod <duncan.macleod@ligo.org> - 0.0.0-1
- initial build of example project
