sh create_distribution
rm -r /usr/local/lib/python3.4/dist-packages/auxi-0.2.0rc7-py3.4.egg
cd dist
rm -r auxi-0.2.0rc7
tar -xf auxi-0.2.0rc7.tar.gz
cd auxi-0.2.0rc7
python3 setup.py install

python3 /usr/local/lib/python3.4/dist-packages/auxi-0.2.0rc7-py3.4.egg/auxi/examples/courier_example.py