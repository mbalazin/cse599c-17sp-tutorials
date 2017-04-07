if [ $(command -v virtualenv2) ]; then
    virtualenv2 --no-site-packages --distribute .env
else
    virtualenv --no-site-packages --distribute .env
fi

source .env/bin/activate
pip install -r requirements.txt
