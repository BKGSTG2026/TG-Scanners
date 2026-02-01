# ----------------------------
# Project configuration
# ----------------------------
NAME        := tg-scanners
VERSION     := 1.0.0
ARCH        ?= $(shell dpkg --print-architecture)
DISTDIR     := dist
USER        := tg-scanner
GROUP       := tg-scanner
FPM         := fpm

TARBALL := $(DISTDIR)/$(NAME).tar.gz
DEB     := $(DISTDIR)/$(NAME)_$(VERSION)_$(ARCH).deb

# ----------------------------
# Files to exclude from tarball
# ----------------------------
EXCLUDES := \
	--exclude-vcs \
	--exclude='__pycache__' \
	--exclude='*.pyc' \
	--exclude='*.pyo' \
	--exclude='*.swp' \
	--exclude='*.egg-info' \
	--exclude='venv' \
	--exclude='.venv' \
	--exclude='dist' \
	--exclude='rpmbuild'

# ----------------------------
# Declare package dependencies
# ----------------------------
DEPS := \
	-d python3 \
	-d python3-venv \
	-d python3-pip \
	-d unixodbc 

# ----------------------------
# Main packaging target
# ----------------------------
.PHONY: package clean

package: $(DEB)

$(DISTDIR):
	mkdir -p $(DISTDIR)


$(TARBALL): | $(DISTDIR)
	@command -v fpm >/dev/null || (echo "fpm not found; install with 'sudo gem install fpm'" && exit 1)
	@echo "Creating source tarball..."
	mkdir -p $(DISTDIR)
	tar \
		-C . -czf $(TARBALL) \
		$(EXCLUDES) \
		.

$(DEB): $(TARBALL)
	@echo "Building .dev package for architecture: '$(ARCH)'"
	$(FPM) -s tar -t deb \
		-n $(NAME) \
		-v $(VERSION) \
		--architecture $(ARCH) \
		--prefix /var/opt/$(NAME) \
		--deb-systemd $(NAME).service \
		--after-install post-install.sh \
		$(DEPS) \
		-p $(DEB) \
		$(TARBALL)

	@echo "DEB package created in $(DISTDIR)/"

# ----------------------------
# Clean build artifacts
# ----------------------------
clean:
	rm -rf $(DISTDIR)

