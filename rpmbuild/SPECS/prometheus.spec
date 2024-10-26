%undefine _missing_build_ids_terminate_build

Name:           prometheus
Version:        2.55.0
Release:        mit.1.1%{?dist}
Summary:        Prometheus monitoring system and time series database
License:        Apache License 2.0
URL:            https://prometheus.io/
Source0:        %{name}-%{version}.linux-amd64.tar.gz
Source1:        prometheus.service
Source2:        prometheus.yml  

BuildArch:      x86_64
Requires:       systemd

%global debug_package %{nil}

%description
Prometheus is an open-source systems monitoring and alerting toolkit, originally built by the Prometheus development team at SoundCloud. It is designed for reliability and scalability and is actively maintained by the Prometheus dev team and its community.

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%install
# Install the Prometheus binary
install -D -m 0755 %{_builddir}/%{name}-%{version}.linux-amd64/prometheus %{buildroot}/usr/local/bin/prometheus
install -D -m 0755 %{_builddir}/%{name}-%{version}.linux-amd64/promtool %{buildroot}/usr/local/bin/promtool

# Install the systemd service file
install -D -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/prometheus.service

# Install the configuration file to /etc/prometheus
install -D -m 0644 %{SOURCE2} %{buildroot}/etc/prometheus/prometheus.yml

%post
# Create a Prometheus user if it doesn't exist
getent passwd prometheus > /dev/null || useradd -r -s /sbin/nologin -d / -c "Prometheus User" prometheus

# Change ownership of the binaries to the prometheus user
chown prometheus:prometheus /usr/local/bin/prometheus
chown prometheus:prometheus /usr/local/bin/promtool

# Enable and start the Prometheus service
systemctl daemon-reload
systemctl enable prometheus

# Display message to the user
echo "Prometheus has been installed. To start the service, run:"
echo "  sudo systemctl start prometheus"

%preun
# Stop and disable the service before uninstalling
if [ $1 -eq 0 ]; then
    systemctl stop prometheus || true
    systemctl disable prometheus || true
fi

%files
/usr/local/bin/prometheus
/usr/local/bin/promtool
/usr/lib/systemd/system/prometheus.service
/etc/prometheus/prometheus.yml 

%changelog
* Sat Oct 26 2024 Your Name <mithuneeecu@gmail.com> - 2.55.0-mit.1.1
- Custom build with "mit.1.1" versioning for Prometheus 2.55.0
- Thanks to the Prometheus development team for their ongoing contributions

