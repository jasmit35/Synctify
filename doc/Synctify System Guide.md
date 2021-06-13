# Synctify System Guide
# Development Cycle
## Startup

### Shutdown the previous version (if running)

## Debugging

## Validation

## Shutdown

### Finalizing the version in development.
Finsh the commit and pushes to the git repositories:

`git add --all`

`git commit -m ''`

`git push github`

`git push woz`

If you are working on a branch and not on master, decide if it is time to merge the branch. If so, follow the directions in the 'Fire Starter User's Guide'.

##  Deployment in test

Complete the normal auto_update steps from Fire-Starter.

Create the file pgpods/.secrets-db-data that holds the Postgres account's password. This file does not get saved to Git Hub (on purpose) and must be recreated each time.

Remove the existing container and volume.



