sh create_distribution
rm -r /usr/local/lib/python3.4/dist-packages/auxi
rm /usr/local/lib/python3.4/dist-packages/auxi-0.2.0rc6.egg-info
cd dist
rm -r auxi-0.2.0rc6
tar -xf auxi-0.2.0rc6.tar.gz
cd auxi-0.2.0rc6
python3 setup.py install


