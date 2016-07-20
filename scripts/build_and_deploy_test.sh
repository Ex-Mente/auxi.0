sh create_distribution
rm -r /usr/local/lib/python3.4/dist-packages/auxi-0.2.3-py3.4.egg
cd dist
rm -r auxi-0.2.3
tar -xf auxi-0.2.3.tar.gz
cd auxi-0.2.3
python3 setup.py install

# python3 /usr/local/lib/python3.4/dist-packages/auxi-0.2.3-py3.4.egg/auxi/tests.py
python3 /usr/local/lib/python3.4/dist-packages/auxi-0.2.3-py3.4.egg/auxi/tools/transportphenomena/heattransfer/naturalconvection_test.py IsothermalFlatSurface
