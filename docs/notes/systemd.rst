=======
Systemd
=======

.. contents:: Table of Contents
    :backlinks: none

Services Management
-------------------

.. code-block:: bash

   # start
   $ systemctl start app.service

   # stop
   $ systemctl stop app.service

   # restart
   $ systemctl restart app.service

   # reload
   $ systemctl reload app.service

   # reload a daemon after modifying a unit
   $ systemctl daemon-reload

   # enable a service
   $ systemctl enable app.service

   # disable a service
   $ systemctl disable app.service

   # check status
   $ systemctl status app.service

   # check is active
   $ systemctl is-active app.service

   # check is enabled
   $ systemctl is-enabled app.service

   # list all units
   $ systemctl list-units

   # list all timers
   $ systemctl list-timers

User Services
-------------

.. code-block:: bash

   $ sudo loginctl enable-linger $USER
   $ mkdir -p ~/.config/systemd/user/

   # allow journalctl --user -xe -f --all
   $ vim /etc/systemd/journald.conf

   [Journal]
   Storage=persistent

   # move app.service to ~/.config/systemd/user/
   $ systemctl --user start app.service
