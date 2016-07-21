sh create_distribution
rm -r /usr/local/lib/python3.4/dist-packages/auxi-0.3.0-py3.4.egg
rm /usr/local/lib/python3.4/dist-packages/auxi-0.3.0.egg-info
cd ../dist
rm -r auxi-0.3.0
tar -xf auxi-0.3.0.tar.gz
cd auxi-0.3.0
python3 setup.py install


