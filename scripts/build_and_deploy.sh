sh create_distribution
rm -r /usr/local/lib/python3.4/dist-packages/auxi-0.3.1-py3.4.egg
rm /usr/local/lib/python3.4/dist-packages/auxi-0.3.1.egg-info
cd ../dist
rm -r auxi-0.3.1
tar -xf auxi-0.3.1.tar.gz
cd auxi-0.3.1
python3 setup.py install


