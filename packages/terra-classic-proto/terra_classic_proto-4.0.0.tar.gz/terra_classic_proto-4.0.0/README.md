# Python implementation for terra.proto

This is a version of terra.proto which specifically supports Terra Classic.

It is intended to be a drop-in replacement for terra.proto - it will install itself as terra.proto.

This is required if you are using the Terra Classic SDK.

## Build instructions

### Requirements:

```bash
python -m pip install "betterproto[compiler]==2.0.0b6"
brew install protobuf
```

### Steps

Download the 50.x version of terra.proto. You can replace the branch name with whatever is relevant.

```bash
git clone -b v0.50.x-support https://github.com/geoffmunn/terra.proto.git
```
Alongside this, download the current version of terra/core from terra-money 

```bash
git clone https://github.com/terra-money/core.git terra/
```

If ```terra/``` already exists, then delete it with this: ```git rm -r terra```

Move into the terra.proto directory and add the submodules

```bash
cd terra.proto
git submodule add https://github.com/classic-terra/core terra/
git submodule update --init 
cd terra/
git checkout 680792d
```

> [!IMPORTANT]
> 680792d is the commit ID of the terra branch we want to use (not 'main'). Replace this with the version you are interested in.

Now copy from the terra-money terra location the following files into the terra.proto/terra/proto location:

```bash
cd ./proto
cp -r ../../../terra/proto/cosmos .
cp -r ../../../terra/proto/juno .
cp -r ../../../terra/proto/osmosis .
```

Move to the scripts location to start the build process

```bash
cd ../../python/scripts
rm -rf ../terra.proto (location may not exist, ok if it doesn’t)
sh proto-gen.sh
```

AFTER RUNNING THE PROTO BUILD SH FILE:

```bash
cp -r ./gamm-files/ ../terra_proto/osmosis/
```

**Finished!**
You can run the python module build steps from here.

Alternative options to this library can be found here:
- GoLang [Terra Core](https://github.com/terra-money/core) clients, 
- JavaScript [@terra-money/terra.proto](https://www.npmjs.com/package/@terra-money/terra.proto/),
- Rust [terra-proto-rs](https://crates.io/crates/terra-proto-rs).