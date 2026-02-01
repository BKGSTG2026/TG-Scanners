Name:           tg-scanners
Version:        1.0.0
Release:        1%{?dist}
Summary:        TG Scanners Python application

License:        Proprietary
Source0:        %{name}.tar.gz

BuildArch:      noarch

Requires:       python3
Requires(pre):  shadow-utils
Requires(post): coreutils
Requires(preun): coreutils

%description
TG Scanners is a Python-based scanning service deployed under /var/opt
and executed using a dedicated, non-login system user.

%prep
%autosetup -c -n %{name}

%build
# Nothing to build (pure Python, pre-packaged zip)

%install
rm -rf %{buildroot}

# Application directory
install -d %{buildroot}/var/opt/%{name}

# Copy application files
cp -a * %{buildroot}/var/opt/%{name}/

# Permissions will be finalized in %post
chmod -R 0755 %{buildroot}/var/opt/%{name}

%pre
# Create group if it does not exist
getent group tgscanners >/dev/null || \
    groupadd --system tgscanners

# Create user if it does not exist
getent passwd tg-scanners >/dev/null || \
    useradd \
        --system \
        --gid tg-scanners \
        --home-dir /var/opt/%{name} \
        --shell /sbin/nologin \
        --comment "TG Scanners service account" \
        tgscanners

%post
# Ensure ownership after install
chown -R tgscanners:tgscanners /var/opt/%{name}

%preun
if [ $1 -eq 0 ]; then
    # Package removal (not upgrade)
    echo "Removing %{name}"
fi

%files
%dir /var/opt/%{name}
/var/opt/%{name}

%changelog
* Thu Feb 01 2026 Secure Tech GRP vendors@securetechgrp.com - 1.0.0-1
- Initial RPM release

