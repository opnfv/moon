pip install -r requirements.txt
pip install dist/moon_utilities-0.1.0.tar.gz 
pip install dist/moon_db-0.1.0.tar.gz 
pip install -r ../moon_utilities/requirements.txt 
pip install -r ../moon_db/requirements.txt 
python setup.py develop
docker rm -f moon_interface moon_router 
docker ps
