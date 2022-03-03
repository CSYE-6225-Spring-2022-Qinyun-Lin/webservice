# Packer

```
# pwd ./webservice

# to validate packer syntax
packer validate -syntax-only ./packer/ami.json

# to build AMI
packer build -var-file='./packer/vars.json' ./packerami.json
```
