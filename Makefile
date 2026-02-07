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

PACKAGE_FILE := $(DISTDIR)/$(NAME)_$(VERSION)_$(ARCH).deb
SRC          := .
TARBALL      := $(DISTDIR)/$(NAME).tar.gz

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
	-d unixodbc \
	-d unixodbc-dev \
	-d freetds-bin \
	-d freetds-dev \
	-d telegraf \
	-d tdsodbc 

# ----------------------------
# Main packaging target
# ----------------------------
.PHONY: clean package

package: clean
	@command -v fpm >/dev/null || (echo "fpm not found; install with 'sudo gem install fpm'" && exit 1)
	@echo "Creating source tarball..."
	mkdir -p $(DISTDIR)
	@tar -C $(SRC) -czf $(TARBALL) \
		$(EXCLUDES) \
		$(SRC)

	@echo "Building .dev package for architecture: '$(ARCH)'"

	fpm -s tar -t deb \
		-p $(PACKAGE_FILE) \
		-n $(NAME) \
		-v $(VERSION) \
		--architecture $(ARCH) \
		--prefix /var/opt/$(NAME) \
		--deb-systemd $(NAME).service \
		--after-install post-install.sh \
		$(DEPS) \
		$(TARBALL)

	@echo "DEB package created in $(DISTDIR)/"

# ----------------------------
# Clean build artifacts
# ----------------------------
.PHONY: clean

clean:
	@echo "Cleaning dist directory"
	rm -rf $(DISTDIR)

