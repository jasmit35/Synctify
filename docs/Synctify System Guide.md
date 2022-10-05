# Synctify System Guide

## Deploying a new release to Test

If the new release is not tagged and ready, follow the steps in the section "New Releases" in the FireStarter's Users Guide.


**If FireStarter has not been updated to specify a release, stage the desired release in the /tmp directory before running auto_update. Then be sure to select the option to use the existing tar file.**

```
cd /tmp
git clone https://github.com/jasmit35/Synctify.git --branch release/v1.0.0
```

### Archive the existing version:
```
cd ~/test/
tar -czvf .archive/Synctify_2022_06_26.tar.gz Synctify
```

### Clean up any much older archives and the current version:
```
cd ~/test/.archive
ll
rm Synctify_2021*
cd ~/test
rm -rf Synctify
```

### Use auto-update to install the new release:
```
export ENVIRONMENT=test
auto-update -e test -a Synctify
```
### Update .db_secrets.env
The secrets files are not stored on GitHub because the contain user names and passwords. You need to manually copy the files:

```
cd /Users/jeff/test/Synctify/local/etc
cp /Users/jeff/devl/Synctify/local/etc/.db_secrets.env .
```

## Deploying a new release to Prod
**If FireStarter has not been updated to specify a release, stage the desired release in the /tmp directory before running auto_update. Then be sure to select the option to use the existing tar file.**

```
cd /tmp
git clone https://github.com/jasmit35/Synctify.git --branch release/v1.0.0
```

### Archive the existing version:

```
cd ~/prod/
tar -czvf Synctify_2022_06_26.tar.gz Synctify
```

### Clean up any much older archives and the current version:

```
cd ~/prod/
ll
rm Synctify_2021*
rm -rf Synctify
```

### Use auto-update to install the new release:

```
export ENVIRONMENT=prod
auto-update -e prod -a Synctify
```
### Update .db_secrets.env
The secrets files are not stored on GitHub because the contain user names and passwords. You need to manually copy the files:

```
cd /Users/jeff/prod/Synctify/local/etc
cp /Users/jeff/devl/Synctify/local/etc/.db_secrets.env .
```



# Requirements.txt
