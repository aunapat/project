#change to root
sudo -i
#go to your home directory with the console
apt-get install build-essential autoconf libtool pkg-config make python-dev python-protobuf python2.7 wget git
#install pip
wget https://bootstrap.pypa.io/get-pip.py
python2.7 get-pip.py
rm -f get-pip.py
#get git repo
git clone --recursive -b dev https://github.com/PokemonGoF/PokemonGo-Bot
cd PokemonGo-Bot
#install and enable virtualenv
#You need to make shure your python version and virtualenv verison work together
#install virtualenv and activate it
pip install virtualenv
virtualenv .
source bin/activate
#then install the requierements
pip install -r requirements.txt

##get the encryption.so and move to right folder
wget http://pgoapi.com/pgoencrypt.tar.gz
tar -xzvf pgoencrypt.tar.gz
cd pgoencrypt/src/
make
cd ../../
#make the encrypt able to load
mv pgoencrypt/src/libencrypt.so encrypt.so

##edit the configuration file
cp configs/config.json.example configs/config.json
vi configs/config.json
# gedit is possible too with 'gedit configs/config.json'
#edit &quot;google&quot; to &quot;ptc&quot; if you have a pokemon trainer account
#edit all settings


##update to newest
#if you need to do more i'll update this file
#make shure virtualenv is enabled and you are in the correct folder
git pull
pip install -r requirements.txt

##start the bot
./run.sh configs/config.json

##after reboot or closing the terminal
#at every new start go into the folder of the PokemonGo-Bot by
#going into the folder where you startet installing it an then
cd PokemonGo-Bot
#activate virtualenv and start
source bin/activate
./run.sh configs/config.json
