# Build the image

```
cd vpnm
docker build -t vpnm .
```

# Args
* -u: user name
* -p: password
* -o: organization ID (aka the BG ID)
* -v: VPC ID
* -a: (action) only remove/restore
* --dryrun: “yes” to test running, “no” to apply


# Run the command
### remove
Removes the static routes to the legacy VPN so the same routes to the AVPN take effect. 
```
docker run -it --rm --name vpnm vpnm -u=syu -p='xxxxx' -o=b2ee7923-e6c7-4ca3-86a0-xxxxx -v=vpc-491bxxxx -a=remove --dryrun=no
```

### restore
Restore the static routes to the legacy VPN so the same routes to the AVPN will be ignored.
```
docker run -it --rm --name vpnm vpnm -u=syu -p='xxxxx' -o=b2ee7923-e6c7-4ca3-86a0-xxxxx -v=vpc-491bxxxx -a=restore --dryrun=no
```