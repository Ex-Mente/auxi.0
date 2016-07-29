sh create_distribution
rm -r /usr/local/lib/python3.4/dist-packages/auxi-0.3.2-py3.4.egg
rm /usr/local/lib/python3.4/dist-packages/auxi-0.3.2.egg-info
cd ../dist
rm -r auxi-0.3.2
tar -xf auxi-0.3.2.tar.gz
cd auxi-0.3.2
python3 setup.py install


