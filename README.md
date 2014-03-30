eyeos2symbiose
==============

Convert Eyeos and Oneye users databse to Symbiose format.

Instructions
------------

You'll have to put Eyeos's XML user files in `input/eyeos/`. Usaly, these XML files are stored in `accounts/` in Eyeos. Make sure to remove `input/eyeos/demo.xml` (that's for test purposes).

If you have an existing Symbiose users database and you don't want to override it, put `/var/lib/jsondb/core/users.json` and `/var/lib/jsondb/core/users_permissions.json` in `input/symbiose/`.

Then, you can run the Python script `python eyeos2symbiose.py`. Python 3 is required.

After that, two files are generated in `output/`. Copy it to `/var/lib/jsondb/core/` and you're done!
