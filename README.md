# [VIVOHarvester](https://pypi.org/project/VIVOHarvester/)

## Installation
```
pip install VIVOHarvester
```

## Usage
* Harvest data from Elements (Default)
```
vivotool -f local.yml -t harvest -d 0
```

* Harvest data from Elements a day ago (Current time -1 day)
```
vivotool -f local.yml -t harvest -d 1
```

* Import RDF data into a VIVO instance
```
vivotool -f local.yml -t ingest
```

* Fetch user_map.csv
```
vivotool -f local.yml -t getuser
```
or
```
vivotool -f local.yml -t getuser -o yourpath/yourfilename
```

## Database creation
* Create require database
```
vivotool -f local.yml -t db
```

## Upgrade to newer version
```
pip uninstall VIVOHarvester
pip install VIVOHarvester==0.1.2 (e.g.)
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/VTUL/VTDLP/tags).

## Authors

* Virginia Tech Libraries - Digital Libraries Development developers
	* [Yinlin Chen](https://github.com/yinlinchen)
	* [Tingting Jiang](https://github.com/tingtingjh)
	* [Lee Hunter](https://github.com/whunter)

See also the list of [contributors](https://github.com/VTUL/VTDLP/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
