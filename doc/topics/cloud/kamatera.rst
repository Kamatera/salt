=================================
Getting Started With Kamatera
=================================

`Kamatera`_ is a global cloud services platform provider, providing enterprise-grade
cloud infrastructure products. Kamatera is operating in 13 global data centers,
with thousands of servers worldwide, serving tens of thousands of clients including
start-ups, application developers, international enterprises, and SaaS providers.

.. _`Kamatera`: https://www.kamatera.com/

Configuration
=============
Using Salt for Kamatera requires an API key and secret which you can get by visiting
`Kamatera Console`_ and adding a new key under API Keys.  Use the created key ID and
Secret in the configuration:

.. _`Kamatera Console`: https://console.kamatera.com/

.. code-block:: yaml

    # Note: This example is for /etc/salt/cloud.providers or any file in the
    # /etc/salt/cloud.providers.d/ directory.

    my-kamatera-config:
      driver: kamatera
      api_client_id: xxxxxxxxxxxxx
      api_secret: yyyyyyyyyyyyyyyyyyyyyy
      minion:
        master: saltmaster.example.com

Profiles
========

Cloud Profiles
~~~~~~~~~~~~~~
Set up an initial profile at ``/etc/salt/cloud.profiles`` or in the
``/etc/salt/cloud.profiles.d/`` directory:

.. code-block:: yaml

    my-kamatera-profile:
      provider: my-kamatera-config
      # salt-cloud --list-locations my-kamatera-config
      location: EU
      # salt-cloud --location EU --list-sizes my-kamatera-config
      cpu_type: B
      cpu_cores: 2
      ram_mb: 2048
      # primary disk size
      # salt-cloud --location EU -f avail_server_options my-kamatera-config
      disk_size_gb: 50
      # up to 3 additional disks
      extra_disk_sizes_gb:
        - 100
        - 200
      # hourly / monthly
      billing_cycle: monthly
      # traffic package is only relevant for monthly billing cycle
      # salt-cloud --location EU -f avail_server_options my-kamatera-config
      monthly_traffic_package: t5000
      # salt-cloud --location EU --list-images my-kamatera-config
      image: EU:6000C29a5a7220dcf84716e7bba74215
      # up to 4 network interfaces can be attached
      # network name 'wan' provides a public IP
      # you can add additional private networks in the Kamatera web-ui
      networks:
        - name: wan
          ip: auto
        # - name: my-lan-id
        #   ip: auto
      # whether to enable daily backups for the created server
      daily_backup: false
      # whether to provide managed support service
      managed: false

Create a server using this profile:

.. code-block:: bash

    salt-cloud -p my-kamatera-profile my-server

Execute salt commands:

.. code-block:: bash

    salt my-server test.version

Locations can be obtained using the ``--list-locations`` option for the ``salt-cloud``
command:

.. code-block:: bash

    # salt-cloud --list-locations my-kamatera-config
    my-kamatera-config:
        ----------
        kamatera:
            ----------
            AS:
                Hong Kong, China (Asia)
            CA-TR:
                Toronto, Canada (North America)
            EU:
                Amsterdam, The Netherlands (Europe)
    ...SNIP...

CPU types and related options can be obtained using the ``--list-sizes`` option for the ``salt-cloud``.
Available CPU options depend on location, so a ``--location`` argument is required.
command:

.. code-block:: bash

    # salt-cloud --location=EU --list-sizes my-kamatera-config
    my-kamatera-config:
        ----------
        kamatera:
            ----------
            A:
                ----------
                cpuCores:
                    [1, 2, 4, 6, 8, 12, 16, 20, 24, 28, 32]
                description:
                    Server CPUs are assigned to a non-dedicated physical CPU thread with no resources guaranteed.
                name:
                    Type A - Availability
                ramMB:
                    [256, 512, 1024, 2048, 3072, 4096, 6144, 8192, 10240, 12288, 16384, 24576, 32768, 49152, 65536, 98304, 131072]
            B:
                ----------
                cpuCores:
                    [1, 2, 4, 6, 8, 12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72, 88, 104]
    ...SNIP...

Server options can be obtained using the ``avail_server_options`` function.
Available server options depend on location, so a ``--location`` argument is required.
command:

.. code-block:: bash

    # salt-cloud --location=EU -f avail_server_options my-kamatera-config
    my-kamatera-config:
        ----------
        kamatera:
            ----------
            A:
                ----------
                cpuCores:
                    [1, 2, 4, 6, 8, 12, 16, 20, 24, 28, 32]
                description:
                    Server CPUs are assigned to a non-dedicated physical CPU thread with no resources guaranteed.
                name:
                    Type A - Availability
                ramMB:
                    [256, 512, 1024, 2048, 3072, 4096, 6144, 8192, 10240, 12288, 16384, 24576, 32768, 49152, 65536, 98304, 131072]
            B:
                ----------
                cpuCores:
                    [1, 2, 4, 6, 8, 12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72, 88, 104]
    ...SNIP...

Images can be obtained using the ``--list-images`` option for the ``salt-cloud``.
Available images depend on location, so a ``--location`` argument is required.
command:

.. code-block:: bash

    # salt-cloud --location=EU --list-images my-kamatera-config
    my-kamatera-config:
        ----------
        kamatera:
            ----------
            EU:6000C2901a61dff371f4d1d34bd9548b:
                Ubuntu Server version 16.04 LTS (xenial) 32-bit
            EU:6000C29040fd67b51a229d7e641fba22:
                Ubuntu Server version 18.04 LTS (bionic) 64-bit.
                Optimized for best performance and with minimal OS services (OS use only 80MB RAM).
            EU:6000C2904fc6d8295d2b6d9687ed955e:
                Ubuntu Server version 18.04 LTS (bionic) 64-bit,
    ...SNIP...

See also :mod:`salt.cloud.clouds.libvirt`