
Autosubmit is a lightweight workflow manager designed to meet climate research necessities. Unlike other workflow solutions in the domain, it integrates the capabilities of an experiment manager, workflow orchestrator and monitor in a self-contained application. The experiment manager allows for defining and configuring experiments, supported by a hierarchical database that ensures reproducibility and traceability. The orchestrator is designed to run complex workflows in research and operational mode by managing their dependencies and interfacing with local and remote hosts. These multi-scale workflows can involve from a few to thousands of steps and from one to multiple platforms.

Autosubmit facilitates easy and fast integration and relocation on new platforms. On the one hand, users can rapidly execute general scripts and progressively parametrize them by reading Autosubmit variables. On the other hand, it is a self-contained desktop application capable of submitting jobs to remote platforms without any external deployment.

Due to its robustness, it can handle different eventualities, such as networking or I/O errors. Finally, the monitoring capabilities extend beyond the desktop application through a REST API that allows communication with workflow monitoring tools such as the Autosubmit web GUI. 

Autosubmit is a Python package provided in PyPI. Conda recipes can also be found on the website. A containerized version for testing purposes is also available but not public yet.

It has contributed to various European research projects and runs different operational systems. During the following years, it will support some of the Earth Digital Twins as the Digital Twin Ocean.

Concretely, it is currently used at Barcelona Supercomputing Centre (BSC) to run models (EC-Earth, MONARCH, NEMO, CALIOPE, HERMES...), operational toolchains (S2S4E), data-download workflows (ECMWF MARS), and many other. Autosubmit has run these workflows in different supercomputers in BSC, ECMWF, IC3, CESGA, EPCC, PDC, and OLCF.