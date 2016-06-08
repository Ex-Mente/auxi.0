sh create_distribution
rm -r /usr/local/lib/python3.4/dist-packages/auxi-0.2.2-py2.7.egg
cd dist
rm -r auxi-0.2.2
tar -xf auxi-0.2.2.tar.gz
cd auxi-0.2.2
python setup.py install

python /usr/local/lib/python2.7/dist-packages/auxi-0.2.2-py2.7.egg/auxi/tests.py
