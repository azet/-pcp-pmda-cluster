
include /etc/pcp.conf

default:
	make -C src

install: default
	make -C src install
	install -m 644 README $(PREFIX)$(PCP_PMDAS_DIR)/cluster

clean:
	make -C src clean
