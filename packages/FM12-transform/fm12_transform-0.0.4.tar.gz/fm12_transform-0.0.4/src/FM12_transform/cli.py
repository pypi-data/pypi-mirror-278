###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

import logging
import os.path

import click
import csv
from typing import Union

from FM12_transform.data2bufr import __version__, transform as transform_synop
from FM12_transform.elastic import create_station_index as init_station_index, create_feature_index
from elasticsearch import Elasticsearch

THISDIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_STATIONS = f"{THISDIR}{os.sep}resources{os.sep}station_list.csv"

# Configure logger
LOGGER = logging.getLogger()
log_level = os.environ.get("LOG_LEVEL", "WARNING")
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=getattr(logging, log_level),
    datefmt="%Y-%m-%d %H:%M:%S"
)

# if (LOGGER.hasHandlers()):
#     LOGGER.handlers.clear()

# # Configure error handler
# handler_err = logging.StreamHandler(sys.stderr)
# handler_err.setLevel(logging.ERROR)
# handler_err.setFormatter(logging.Formatter(
#     fmt="%(asctime)s [%(levelname)s] %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S"
# ))
# LOGGER.addHandler(handler_err)


def cli_option_verbosity(f):
    logging_options = ["ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]

    def callback(ctx, param, value):
        if value is not None:
            LOGGER.setLevel(getattr(logging, value))
        return True

    return click.option("--verbosity", "-v",
                        type=click.Choice(logging_options),
                        help="Verbosity",
                        callback=callback)(f)


def cli_callbacks(f):
    f = cli_option_verbosity(f)
    return f


def get_typed_value(value) -> Union[float, int, str]:
    """
    Derive true type from data value

    :param value: value

    :returns: value as a native Python data type
    """

    try:
        if '.' in value:  # float?
            value2 = float(value)
        elif len(value) > 1 and value.startswith('0'):
            value2 = value
        else:  # int?
            value2 = int(value)
    except ValueError:  # string (default)?
        value2 = value

    return value2

def publish_from_csv(station_csv) -> None:
    """
    Publishes station collection to API config and backend from csv

    :returns: `None`
    """

    oscar_baseurl = 'https://oscar.wmo.int/surface/#/search/station/stationReportDetails'  # noqa

    LOGGER.debug(f'Publishing station list from {station_csv}')
    station_list = []
    with station_csv.open() as fh:
        reader = csv.DictReader(fh)

        for row in reader:
            wigos_station_identifier = row['wigos_station_identifier']
            station_list.append(wigos_station_identifier)
            # topics = list(check_station_datasets(wigos_station_identifier))
            # topic = None if len(topics) == 0 else topics[0]['title']

            try:
                barometer_height = float(row['barometer_height'])
            except ValueError:
                barometer_height = None

            LOGGER.debug('Verifying station coordinate types')
            for pc in ['longitude', 'latitude', 'elevation']:
                value = get_typed_value(row[pc])
                if not isinstance(value, (int, float)):
                    msg = f'Invalid station {pc} value: {value}'
                    LOGGER.error(msg)
                    raise RuntimeError(msg)

            feature = {
                'id': wigos_station_identifier,
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        get_typed_value(row['longitude']),
                        get_typed_value(row['latitude'])
                    ]
                },
                'properties': {
                   'name': row['station_name'],
                   'wigos_station_identifier': wigos_station_identifier,
                   'traditional_station_identifier': row['traditional_station_identifier'],  # noqa
                   'barometer_height': barometer_height,
                   'facility_type': row['facility_type'],
                   'territory_name': row['territory_name'],
                   'wmo_region': row['wmo_region'],
                   'url': f"{oscar_baseurl}/{wigos_station_identifier}",
                   # TODO: update with real-time status as per https://codes.wmo.int/wmdr/_ReportingStatus  # noqa
                   'status': 'operational'
                },
                'links': None
            }

            # LOGGER.debug('Checking properties against WMDR code lists')
            # for key, values in get_wmdr_codelists().items():
            #     column_value = feature['properties'][key]
            #     if column_value not in values:
            #         msg = f'Invalid value {column_value}'
            #         raise RuntimeError(msg)

            station_elevation = get_typed_value(row['elevation'])

            if isinstance(station_elevation, (float, int)):
                LOGGER.debug('Adding z value to geometry')
                feature['geometry']['coordinates'].append(station_elevation)

            LOGGER.debug('Updating backend')
            client = Elasticsearch('http://localhost:9200')
            try:
                client.delete(index='wigos_stations', id=feature['id'])
                # delete_collection_item('stations', feature['id'])
            except RuntimeError as err:
                LOGGER.debug(f'Station does not exist: {err}')
            client.index(index='wigos_stations', id=feature['id'], document=feature)

@click.group()
@click.version_option(version=__version__)
def cli():
    """synop2bufr"""
    pass


# @click.group()
# def data():
#     """data utilities"""
#     pass

@click.command()
@click.pass_context
def create_station_index():
    init_station_index()

@click.command()
@click.pass_context
@click.option('--metadata', 'metadata', required=True,
              default=DEFAULT_STATIONS,
              type=click.File(errors='ignore'),
              help='Name/directory of the station metadata')
def publish_station_list(metadata):
    publish_from_csv(metadata)




@click.command()
@click.pass_context
@click.argument('synop_file', type=click.File(errors="ignore"))
@click.option('--metadata', 'metadata', required=False,
              default="station_list.csv",
              type=click.File(errors="ignore"),
              help="Name/directory of the station metadata")
@click.option('--output-dir', 'output_dir', required=False,
              default=".",
              help="Directory for the output BUFR files")
@click.option('--year', 'year', required=True,
              help="Year that the data corresponds to")
@click.option('--month', 'month', required=True,
              help="Month that the data corresponds to")
@cli_option_verbosity
def transform(ctx, synop_file, metadata, output_dir, year, month, verbosity):

    try:
        # Get content from synop file
        content = synop_file.read()

        # Boolean to know if the decoded CSV has a header
        # or not yet
        header_written = False

        try:
            result = transform_synop(
                content, metadata.read(), year, month
            )

        except Exception as e:
            raise click.ClickException(e)

        for item in result:

            # Return object may not have a datetime if there is an error
            # parsing a report
            if item["_meta"]["properties"].get("datetime") is not None:
                timestamp = item["_meta"]["properties"]["datetime"].strftime(
                    '%Y%m%dT%H%M%S'
                )
                filename = f"decoded_{timestamp}.csv"

                # Write the CSV file of decoded data
                csv_string = item["_meta"]["csv"]

                if header_written:
                    mode = "a"  # Append to file if headers
                else:
                    mode = "w"  # Write to file if no headers

                with open(filename, mode) as f:
                    # Check there was no problem writing the report to CSV
                    if csv_string is not None:
                        if not header_written:
                            # Write the whole string including headers
                            f.write(csv_string)
                            header_written = True
                        else:
                            # Skip the header row of the string
                            f.write(csv_string.split("\n")[1])

                # Check there was no problem encoding the BUFR message
                # before writing to a file
                if item.get("bufr4") is not None:
                    # Write the BUFR file
                    key = item['_meta']["id"]
                    bufr_filename = f"{output_dir}{os.sep}{key}.bufr4"

                    with open(bufr_filename, "wb") as fh:
                        fh.write(item["bufr4"])

    except Exception as e:
        raise click.ClickException(e)


# data.add_command(transform)
cli.add_command(create_station_index)
cli.add_command(publish_station_list)