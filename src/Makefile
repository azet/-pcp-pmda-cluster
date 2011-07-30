#
# Copyright (c) 2008-2009 Silicon Graphics, Inc.  All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#

include /etc/pcp.conf
include $(PCP_INC_DIR)/builddefs

DFILES	= config
CFILES	= pmda.c server.c util.c pmclusterd.c
HFILES  = cluster.h
# These C files are automatically generated.
AUTO_CFILES = metric_table.c subdomains.c
CMDTARGET = pmdacluster$(EXECSUFFIX)
DAEMON = pmclusterd
LLDLIBS = -lpcp -lpcp_pmda
LCFLAGS = -I.
LSRCFILES = Install Remove $(DFILES) root GNUmakefile.install \
	    rc_pmclusterd clusterns.pl
IAM	= cluster
DOMAIN	= CLUSTER
PMDADIR	= $(PCP_PMDAS_DIR)/$(IAM)
$(CMDTARGET)_OBJS = pmda.o server.o util.o $(AUTO_CFILES:.c=.o)
$(DAEMON)_OBJS = pmclusterd.o util.o $(AUTO_CFILES:.c=.o)

# sub-PMDA namespace root nodes and help files

SUBPMNS = $(PCP_VAR_DIR)/pmns/root_linux $(PCP_PMDAS_DIR)/ib/root
SUBHELP = $(PCP_PMDAS_DIR)/linux/help $(PCP_PMDAS_DIR)/ib/help

LDIRT	= help pmns metric_table.c domain.h pcp *.o $(IAM).log \
	  pmda$(IAM) pmda_$(IAM).so $(DAEMON) pmns.tmp* subdomains.c

default: help pmns domain.h subdomains.c $(CMDTARGET) $(DAEMON)

install: default
	install -m 755 -d $(PREFIX)$(PMDADIR)
	install -m 755 -d $(PREFIX)$(PMDADIR)/nodes
	install -m 755 -d $(PREFIX)$(PCP_BINADM_DIR)
	install -m 755 -d $(PREFIX)$(PCP_RC_DIR)
	install -m 755 Install Remove $(CMDTARGET) $(PREFIX)$(PMDADIR)
	install -m 644 $(DFILES) pmns root help domain.h $(PREFIX)$(PMDADIR)
	install -m 755 pmclusterd $(PREFIX)$(PCP_BINADM_DIR)/pmclusterd
	install -m 755 rc_pmclusterd $(PREFIX)$(PCP_RC_DIR)/pmclusterd

PMNSMERGE = $(PCP_BINADM_DIR)/pmnsmerge

# Build a namespace containing all of the sub-PMDAS.  At the same time
# generate a list of metric names and domain numbers and generate a C
# source file containing the corresponding subdomain mapping.

help pmns metric_table.c subdomains.c : \
		config cluster.h $(SUBPMNS) $(SUBHELP) $(STDPMID) clusterns.pl
	rm -f pmns.tmp*
	echo "root {" >pmns.tmp
	echo "}" >>pmns.tmp
	thisDir=`pwd` && \
	for ns in $(SUBPMNS) ; do \
	    pmdaName=`dirname $$ns` ; \
	    pmdaName=`basename $$pmdaName` ; \
	    echo "including PMNS from $$ns" ; \
	    cd `dirname $$ns` && \
	    pmdaroot=`basename $$ns` && \
	    echo $(PMNSMERGE) $$thisDir/pmns.tmp $$pmdaroot $$thisDir/pmns.tmp.out && \
	    $(PMNSMERGE) $$thisDir/pmns.tmp $$pmdaroot $$thisDir/pmns.tmp.out && \
	    echo pminfo -m -n $$ns && pminfo -m -n $$ns | \
		awk -v pmda=$$pmdaName -v ns=$$ns \
		    >>$$thisDir/pmns.tmp.map ' \
		    NF==3 && $$2=="PMID:" && \
		    $$3 ~ /^[0-9]+\.[0-9]+\.[0-9]+$$/ \
		    { \
			n++; \
			d = substr($$3, 1, index($$3, ".") - 1); \
			print d, pmda; \
			exit(0); \
		    } ; \
		    END { \
			if (n==0) { \
			    print "no metrics in ", ns, "\n" >"/dev/stderr"; \
			    exit(1) \
			} \
		    }' && \
	    mv $$thisDir/pmns.tmp.out $$thisDir/pmns.tmp ; \
	    cd $$thisDir ; \
	    rm -f pmns.tmp.out* ; \
	done
	./clusterns.pl pmns.tmp pmns.tmp.map $(SUBHELP)
	rm -f pmns.tmp*

domain.h: $(PCP_VAR_DIR)/pmns/stdpmid.pcp
	$(DOMAIN_MAKERULE)

$(CMDTARGET) : OBJECTS=$($(CMDTARGET)_OBJS)
$(CMDTARGET) : $($(CMDTARGET)_OBJS)

$(DAEMON): OBJECTS=$($(DAEMON)_OBJS)
$(DAEMON): $($(DAEMON)_OBJS)
	$(CCF) -o $(DAEMON) $(LDFLAGS) $(OBJECTS) $(LDLIBS)

include $(PCP_INC_DIR)/buildrules

