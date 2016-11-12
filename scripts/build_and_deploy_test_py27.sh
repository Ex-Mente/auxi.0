sh create_distribution
rm -r /usr/local/lib/python3.4/dist-packages/auxi-0.3.3-py2.7.egg
cd ../dist
rm -r auxi-0.3.3
tar -xf auxi-0.3.3.tar.gz
cd auxi-0.3.3
python setup.py install

python /usr/local/lib/python2.7/dist-packages/auxi-0.3.3-py2.7.egg/auxi/tests.py
