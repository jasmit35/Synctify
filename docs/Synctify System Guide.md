# Synctify System Guide

## Deploying a new release to Test

If the new release is not tagged and ready, follow the steps in the section "New Releases" in the FireStarter's Users Guide.


**If FireStarter has not been updated to specify a release, stage the desired release in the /tmp directory before running auto_update. Then be sure to select the option to use the existing tar file.**

```
cd /tmp
git clone https://github.com/jasmit35/Syntify.git --branch release/v1.0.0
```


### Hide the existing version:

```
cd ~/test/Syntify
mkdir .old_2022_06_23
mv * .old_2022_06_23
```

### Clean up any older versions:

```
cd ~/test/Syntify
ll
rm -rf .old_2021*
```

### Use auto-update to install the new release:

```
export ENVIRONMENT=test
auto-update -e test -a Syntify
```
### Update .db_secrets.env
The secrets files are not stored on GitHub because the contain user names and passwords. You need to manually copy the files:

```
cd /Users/jeff/test/Syntify/local/etc
cp /Users/jeff/devl/Syntify/local/etc/.db_secrets.env .
```

## Deploying a new release to Prod
**If FireStarter has not been updated to specify a release, stage the desired release in the /tmp directory before running auto_update. Then be sure to select the option to use the existing tar file.**

```
cd /tmp
git clone https://github.com/jasmit35/Syntify.git --branch release/v1.0.0
```

### Archive the existing version:

```
cd ~/prod/
tar -czvf Syntify_2022_06_26.tar.gz Syntify
```

### Clean up any much older archives and the current version:

```
cd ~/prod/
ll
rm Syntify_2021*
rm -rf Syntify
```

### Use auto-update to install the new release:

```
export ENVIRONMENT=prod
auto-update -e prod -a Syntify
```
### Update .db_secrets.env
The secrets files are not stored on GitHub because the contain user names and passwords. You need to manually copy the files:

```
cd /Users/jeff/prod/Syntify/local/etc
cp /Users/jeff/devl/Syntify/local/etc/.db_secrets.env .
```



# Requirements.txt
