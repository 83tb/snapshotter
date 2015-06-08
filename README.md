# snapshotter

Rename default_config.py file to config.py.
Set your API KEY/SECRET and tag_name inside this file.

And then run

```
python snapshotter.py
```

Snapshotter will do a backup of every volume that is tagged with 'tag_name' set by you.
'keep' value in config file decided how many copies would you like to keep. If you do daily backups and the value is set to '7' it will keep only 1 week old backups.
