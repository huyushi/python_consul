dist_path="~/coding/flexiv_consul_service/dist"
build_path="~/coding/flexiv_consul_service/build"
egg_path="~/coding/flexiv_consul_service/flexiv_consul_service.egg-info/"

if [ ! -d "$dist_path" ]; then
  rm -rf ~/coding/flexiv_consul_service/dist
fi

if [ ! -d "$build_path" ]; then
  rm -rf ~/coding/flexiv_consul_service/e/build
fi

if [ ! -d "$egg_path" ]; then
  rm -rf egg_path
fi

python setup.py sdist bdist_wheel && python -m twine upload --repository-url http://10.24.11.188:12345 dist/*