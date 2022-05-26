#!/usr/bin/env python3

from alerting_functions import create, get_monitors, get_destinations, update
import argparse
import os
import sys
import ruamel.yaml
import logging
import urllib3
import boto3
urllib3.disable_warnings()


# SETUP LOGGING OPTIONS
logging.basicConfig(stream=sys.stdout,
                    format="%(asctime)s;%(levelname)s;%(message)s")
log = logging.getLogger("opendistro-alerting")
log.setLevel(logging.INFO)


def find(arr, name):
    for x in arr:
        if x['name'] == name:
            return x['id']


def pipeline_run(event):
    try:
        yaml = ruamel.yaml.YAML(typ='safe')
        log.info('initializing pipeline creation')
        data_monitors = get_monitors(event)
        lst = []
        for alert in os.listdir('./alerts/'):
            with open(os.path.join('./alerts/', alert)) as alert_load:
                yaml_object = yaml.load(alert_load)
            lst.append(yaml_object[0]['name'])
        for alert in os.listdir('./alerts/'):
            with open(os.path.join('./alerts/', alert)) as alert_load:
                yaml_object = yaml.load(alert_load)
                if len(set(lst)) == len(lst):
                    if yaml_object[0]['name'] in [monitor.get('name') for monitor in data_monitors]:
                        _id = find(data_monitors, yaml_object[0]['name'])
                        log.info('\U0001F60E' +
                            yaml_object[0]['name'] + ' is already created with the ID: ' + _id)
                        update(event, yaml_object, _id)
                    else:
                        log.info('\U0001F47E' + yaml_object[0]['name'] +
                                 ' not exist and need to be created')
                        print(yaml_object)
                        create(event, yaml_object)
                else:
                    log.error("\U0001F42C alert name into yaml files can't be duplicated: " +
                              yaml_object[0]['name'] + " into the file: " + alert)
    except Exception as e:
        log.error('\U0001F42C' + str(e))
        pass


def compare(event):
    try:
        yaml = ruamel.yaml.YAML(typ='safe')
        log.info('\U0001F6A8 initializing pipeline creation')
        data_monitors = get_monitors(event)
        # create list of local alerts to compare
        lst = []
        for alert in os.listdir('./alerts/'):
            with open(os.path.join('./alerts/', alert)) as alert_load:
                yaml_object = yaml.load(alert_load)
            lst.append(yaml_object[0]['name'])
        for alert in os.listdir('./alerts/'):
            with open(os.path.join('./alerts/', alert)) as alert_load:
                yaml_object = yaml.load(alert_load)
                # check duplicate files names:
                if len(set(lst)) == len(lst):
                    if yaml_object[0]['name'] in [monitor.get('name') for monitor in data_monitors]:
                        _id = find(data_monitors, yaml_object[0]['name'])
                        log.info('\U0001F60E' +
                            yaml_object[0]['name'] + ' is already created with the ID: ' + _id)
                    else:
                        log.info('\U0001F47E' + yaml_object[0]['name'] +
                                 ' not exist and need to be created')
                else:
                    log.error("\U0001F42C alert name into yaml files can't be duplicated: " +
                              yaml_object[0]['name'] + " into the file: " + alert)
    except Exception as e:
        log.error(str(e))
        pass


def main(argv):
    event = dict()
    event['kibana_url'] = argv.kibana_url
    event['action'] = argv.action
    if argv.action == 'create':
        create(event, data)
    elif argv.action == 'get_monitors':
        get_monitors(event)
    elif argv.action == 'get_destinations':
        get_destinations(event)
    elif argv.action == 'update':
        update(event)
    elif argv.action == 'pipeline':
        pipeline_run(event)
    elif argv.action == 'compare':
        compare(event)
    else:
        print('Please use a valid option, valid options are: "create", "get_monitors", "get_destinations" and "update"')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-k', '--kibana-url'
    )
    parser.add_argument(
        '-a', '--action'
    )
    args = parser.parse_args()
    main(args)
