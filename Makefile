CWD		= `pwd`

debug dev::
	EVENTBRITE_TOKEN="${EVENTBRITE_TOKEN}" gunicorn --chdir src server:app -b 127.0.0.1:5000

debug-docker::
	docker run -it --rm -p 80:80 -p 5000:80 -e "EVENTBRITE_TOKEN=${EVENTBRITE_TOKEN}" xebiafrance/api-conferences:v1.1.0


validate::
	docker run -it \
	  -v ${CWD}/conferences:/srv/conferences \
	  -v ${CWD}/tests/schema.json:/srv/schema.json \
	  horgix/pajv:1.2.0 pajv -s /srv/schema.json -d '/srv/conferences/*/*'

nodocker_validate:;
	pajv -s tests/schema.json -d conferences/*/*

