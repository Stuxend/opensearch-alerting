#!/usr/bin/env python3

import requests
import sys
import logging
import os
import json
from requests_aws4auth import AWS4Auth
import urllib3
from aws_auth import get_aws_auth
urllib3.disable_warnings()


# SETUP LOGGING OPTIONS
logging.basicConfig(stream=sys.stdout,
                    format="%(asctime)s;%(levelname)s;%(message)s")
log = logging.getLogger("opensearch-alerting")
log.setLevel(logging.DEBUG)


# Authentication for AWS OpenSearch
awsauth = get_aws_auth()


def create(event, _data):
    try:
        # get kibana objects from API
        kibana_url = event.get('kibana_url')
        # Kibana API save objects info
        url = "%s/_opendistro/_alerting/monitors" % (
            kibana_url.rstrip("/"),)
        log.info("connected to: " + kibana_url)
        # log.info("creating rule: " + alert['name'])
        r = requests.post(
            url,
            auth=(awsauth),
            stream=True,
            headers={'kbn-xsrf': 'kibana', 'securitytenant': 'global',
                     'Content-Type': 'application/json'},
            data=json.dumps(_data[0], indent=4),
        )
        log.info("done")
        print(r)
    except Exception as e:
        log.warning(str("something goes wrong creating the rule: " + _data[0]['name']))
        log.error(str(e))


def get_monitors(event):
    try:
        # get kibana objects from API
        kibana_url = event.get('kibana_url')
        # Kibana API save objects info
        url = "%s/_opendistro/_alerting/monitors/_search" % (
            kibana_url.rstrip("/"),)
        log.info("getting monitors and destinations from "+kibana_url)
        query_send = json.dumps({"size": 500, "query": {"match_all": {}}})
        r = requests.get(
            url,
            auth=(awsauth),
            headers={'Content-Type': 'application/json'},
            data=query_send,
        )
        alerts = r.json()
        alert_json = []
        for alert in alerts['hits']['hits']:
            name = alert['_source'].get('name')
            id = alert['_id']
            _type = alert['_source'].get('type')
            obj = {
                "name": name,
                "id": id,
                "type": _type
            }
            alert_json.append(obj)
        log.info("done.. returning alert_json list")
        return(alert_json)
    except Exception as e:
        log.warning(str("something goes wrong getting the monitors"))
        log.error(str(e))


def get_destinations(event):
    try:
        # get kibana objects from API
        kibana_url = event.get('kibana_url')
        # Kibana API save objects info
        url = "%s/_opendistro/_alerting/destinations" % (
            kibana_url.rstrip("/"),)
        log.info("downloading saved objects from "+kibana_url)
        query_send = json.dumps({"size": 1000, "query": {"match_all": {}}})
        r = requests.get(
            url,
            auth=(awsauth),
            headers={'Content-Type': 'application/json',
                     'Content-Type': 'application/json'},
            data=query_send,
        )
        destinations = r.json()
        destination_json = []
        for destination in destinations['destinations']:
            name = destination.get('name')
            id = destination.get('id')
            _type = destination.get('type')
            obj = {
                "name": name,
                "id": id,
                "type": _type
            }
            destination_json.append(obj)
        log.info("done.. returning alert_json list")
        return(destination_json)
    except Exception as e:
        log.warning(str("something goes wrong getting the destination"))
        log.error(str(e))


def update(event, _data, _id):
    try:
        # get kibana objects from API
        kibana_url = event.get('kibana_url')
        # Kibana API save objects info
        url = "%s/_opendistro/_alerting/monitors/" % (
            kibana_url.rstrip("/"),)
        log.info("connected to: " + kibana_url)
        log.info("updating rule: " + _id)
        r = requests.put(
            url+_id,
            auth=(awsauth),
            headers={'kbn-xsrf': 'kibana', 'securitytenant': 'global',
                     'Content-Type': 'application/json'},
            data=json.dumps(_data[0], indent=4),
        )
        log.info("done")
    except Exception as e:
        log.warning(
            str("something goes wrong updating the rule: " + data.get('name')))
        log.error(str(e))
