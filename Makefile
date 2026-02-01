# ----------------------------
# Project configuration
# ----------------------------
NAME        := tg-scanners
VERSION     := 1.0.0
ARCH        := arm64
DISTDIR     := dist
USER        := tgscanners
GROUP       := tgscanners
FPM         := fpm

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
# Main packaging target
# ----------------------------
.PHONY: package clean

package:
	@command -v fpm >/dev/null || (echo "fpm not found; install with 'sudo gem install fpm'" && exit 1)
	@echo "Creating source tarball..."
	mkdir -p $(DISTDIR)
	tar \
		-czf $(DISTDIR)/$(NAME).tar.gz \
		$(EXCLUDES) \
		--transform 's|^\./|$(NAME)/|' \
		.
	@echo "ARCH='$(ARCH)'"	
	@echo "Building .deb package..."
	$(FPM) -s tar -t deb \
		-n $(NAME) \
		-v $(VERSION) \
		--architecture $(ARCH) \
		--prefix /var/opt/$(NAME) \
		--deb-systemd tg-scanners.service \
		--after-install post-install.sh \
		-p $(DISTDIR)/$(NAME)_$(VERSION)_$(ARCH).deb \
		$(DISTDIR)/$(NAME).tar.gz

	@echo "DEB package created in $(DISTDIR)/"

# ----------------------------
# Clean build artifacts
# ----------------------------
clean:
	rm -rf $(DISTDIR)

