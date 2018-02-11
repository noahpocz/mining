#!/bin/bash

sudo apt-get update -y

# dependencies
sudo apt-get install -y screen fglrx-updates git vim ssh wget

# autorun miner
sudo mv rc.local /etc/rc.local

# boot to cli
sudo mv grub /etc/default/grub
sudo update-grub

# open port 22 for ssh
sudo ufw allow 22

# install claymore's miner
wget https://github.com/nanopool/Claymore-Dual-Miner/releases/download/v10.0/Claymore.s.Dual.Ethereum.Decred_Siacoin_Lbry_Pascal.AMD.NVIDIA.GPU.Miner.v10.0.-.LINUX.tar.gz -O claymore.tar.gz

mkdir ../claymore
tar -xf claymore.tar.gz -C ../claymore
rm claymore.tar.gz

echo "Setup complete!"
