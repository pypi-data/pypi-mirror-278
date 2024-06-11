import configparser
import json
import os
import re
import sys
from datetime import datetime

import click
import requests
from requests.exceptions import ConnectionError, InvalidSchema


class Utils:
    log_info = click.style('INFO:', fg='green')
    log_error = click.style('ERROR:', fg='red')

    @staticmethod
    def is_valid_url(url: str):
        pattern = r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$'
        return bool(re.match(pattern, url))

    @staticmethod
    def retrieve_conf(conf):
        if conf is None:
            conf = os.path.expanduser('~') + '/.deltatwin/conf.ini'

        return conf

    @staticmethod
    def retrieve_token(conf):
        try:
            token = Utils.get_token(conf)
        except KeyError:
            if os.path.isfile(conf):
                API.refresh_token(conf)
                token = Utils.get_token(conf)
            else:
                click.echo(f"{Utils.log_error} No token find please use "
                           f"deltatwin login before using this command.")
                sys.exit(ReturnCode.USAGE_ERROR)
        return token

    @staticmethod
    def retrieve_harbor_token(path) -> tuple[str, str]:
        try:
            conf = Utils.read_config(path, 'SERVICES')
            return conf["harbor_access_token"], conf["harbor_refresh_token"]
        except Exception:
            return None, None

    @staticmethod
    def check_status(response):
        if 400 > response.status_code >= 300:
            click.echo(f"{Utils.log_error} {response.reason} "
                       f"at {response.request.url}.")
            sys.exit(ReturnCode.RESOURCE_NOT_FOUND)
        if 500 > response.status_code >= 400:
            click.echo(f"{Utils.log_error} {response.reason} "
                       f"at {response.request.url}.")
            sys.exit(ReturnCode.UNAUTHORIZED)
        if response.status_code >= 500:
            click.echo(f"{Utils.log_error} {response.reason} "
                       f"at {response.request.url}.")
            sys.exit(ReturnCode.SERVICE_ERROR)

    @staticmethod
    def output_as_json(output_format, data):
        if output_format is not None and output_format.lower() == 'json':
            try:
                json.loads(json.dumps(data))
            except ValueError:
                return False
            return True
        return False

    @staticmethod
    def read_config(path: str, context: str = None):
        cfg = configparser.ConfigParser()

        if os.path.isfile(path):
            cfg.read(path)

        if context is not None:
            return dict(cfg[context])
        return cfg

    @staticmethod
    def save_config(path: str, context: str, config: dict):
        cfg = configparser.ConfigParser()

        cfg[context] = config

        with open(path, 'w') as configfile:  # save
            cfg.write(configfile)

    @staticmethod
    def get_token(path: str):
        return Utils.read_config(path, 'SERVICES')['token']

    @staticmethod
    def get_service(path: str):
        url = Utils.read_config(path, 'SERVICES')['api']
        return url[:-1] if url.endswith('/') else url


class API:
    @staticmethod
    def log_to_api(api: str, username: str, password: str):
        myobj = {
            'username': username,
            'password': password

        }

        try:
            resp = requests.post(
                url=f"{api}/connect",
                json=myobj
            )
        except (ConnectionError, InvalidSchema):
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {api}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(resp)

        return json.loads(resp.text)

    @staticmethod
    def query_token(api: str, token: str, harbor_token: str):
        myobj = {
            'refresh_token': token
        }

        harbor_headers = {
            "refresh_token": harbor_token
        }

        try:
            resp = requests.post(
                url=f"{api}/refresh",
                json=myobj
            )

            harbor_resp = requests.post(
                url=f"{api}/harbor_refresh_token",
                json=harbor_headers
            )
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{api}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(resp)
        Utils.check_status(harbor_resp)

        data = resp.json()
        data["harbor"] = harbor_resp.json()
        return data

    @staticmethod
    def refresh_token(conf: str):
        created = datetime.now()
        try:
            config = Utils.read_config(conf, 'SERVICES')

            # Check if refresh token in conf
            if 'refresh_token' in config:
                date = datetime.strptime(
                    config['token_created'], '%Y-%m-%d %H:%M:%S')
                now = datetime.now()

                # check if refresh token is still valid
                if (now - date).total_seconds() < float(
                        config['refresh_expires_in']):
                    data = API.query_token(config['api'],
                                           config['refresh_token'],
                                           config['harbor_refresh_token'])
                    click.echo(f'{Utils.log_info} Refreshing token')
                else:
                    data = API.log_to_api(
                        config['api'],
                        config['username'],
                        config['password'])
                    click.echo(
                        f'{Utils.log_info} Refresh token '
                        f'expired log again to the service')
            else:
                data = API.log_to_api(
                    config['api'],
                    config["username"],
                    config["password"]
                )

                click.echo(f"{Utils.log_info}"
                           f" Log to the service {config['api']}")

        except KeyError:
            click.echo(f"{Utils.log_error} No config find please use "
                       f"deltatwin login before using this command.")
            sys.exit(ReturnCode.USAGE_ERROR)

        created = created.strftime("%Y-%m-%d %H:%M:%S")
        config['token_created'] = created
        config['token'] = data['access_token']
        config['expires_in'] = data["expires_in"]
        config['refresh_expires_in'] = data["refresh_expires_in"]
        config['refresh_token'] = data["refresh_token"]

        # Register config harbor informations
        config['harbor_access_token'] = data['harbor']['harbor_access_token']
        config['harbor_refresh_token'] = data['harbor']['harbor_refresh_token']

        Utils.save_config(conf, 'SERVICES', config)

    @staticmethod
    def force_login(conf: str):
        created = datetime.now()

        config = Utils.read_config(conf, 'SERVICES')

        data = API.log_to_api(
            config['api'],
            config["username"],
            config["password"]
        )

        created = created.strftime("%Y-%m-%d %H:%M:%S")
        config['token_created'] = created
        config['token'] = data['access_token']
        config['expires_in'] = data["expires_in"]
        config['refresh_expires_in'] = data["refresh_expires_in"]
        config['refresh_token'] = data["refresh_token"]

        # Register config harbor informations
        config['harbor_access_token'] = data['harbor']['harbor_access_token']
        config['harbor_refresh_token'] = data['harbor']['harbor_refresh_token']

        Utils.save_config(conf, 'SERVICES', config)

    @staticmethod
    def get_harbor_url(path: str):
        conf = Utils.retrieve_conf(path)
        token = Utils.retrieve_token(conf)

        url = f'{Utils.get_service(conf)}/harbor_get_url'
        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()['harbor_url']

    @staticmethod
    def get_twin_id_by_run_id(conf: str, run_id: str):

        token = Utils.retrieve_token(conf)

        url = f'{Utils.get_service(conf)}/runs/{run_id}'

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)
        Utils.check_status(r)

        return r.json()['dtwin_id']

    @staticmethod
    def create_artifact(conf, run_id, output_name, name, description, tags):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        twin_id = API.get_twin_id_by_run_id(conf, run_id)

        url = (f'{Utils.get_service(conf)}/deltatwins/'
               f'{twin_id}/runs/{run_id}/{output_name}/artifact')
        try:
            r = requests.post(
                url,
                headers={'Authorization': f'Bearer {token}'},
                json={"name": name, "description": description,
                      "tags": str(tags)}  # TODO pass [] when api was ready.
            )
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

    @staticmethod
    def download_artifact(conf, artifact_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        url = (f'{Utils.get_service(conf)}/artifacts/{artifact_id}/download')
        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r

    @staticmethod
    def list_artifact(conf):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        url = f'{Utils.get_service(conf)}/artifacts'

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @staticmethod
    def download_run(conf, run_id, output_name):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        twin_id = API.get_twin_id_by_run_id(conf, run_id)

        url = (f'{Utils.get_service(conf)}/deltatwins/'
               f'{twin_id}/runs/{run_id}/{output_name}/download')

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r

    @staticmethod
    def get_run(conf, run_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)
        url = f'{Utils.get_service(conf)}/runs/{run_id}'

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @staticmethod
    def delete_run(conf, run_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)
        url = f'{Utils.get_service(conf)}/runs/{run_id}'

        try:
            r = requests.delete(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

    @staticmethod
    def list_runs(conf, twin_name, status, limit, offset):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        url = f'{Utils.get_service(conf)}/deltatwins/{twin_name}/runs'

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'},
                params={"status": status,
                        "limit": limit, "offset": offset})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @staticmethod
    def start_run(conf, twin_name, input_file, input_run):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)
        inputs_json = []

        if input_run is not None and len(input_run) > 0:
            if input_file is not None:
                raise click.UsageError("the options inputs-file and inputs "
                                       "are mutually exclusive")
            for input_arg in input_run:
                inputs_json.append(
                    {'name': input_arg[0], 'value': input_arg[1]})
        if input_file is not None:
            file_inputs = open(input_file)
            inputs_json = json.load(file_inputs)

        url = f'{Utils.get_service(conf)}/deltatwins/{twin_name}/runs'

        try:
            r = requests.post(
                url,
                headers={'Authorization': f'Bearer {token}'}, json=inputs_json)
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @staticmethod
    def delete_artifact(conf, artifact_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            r = requests.delete(
                f'{Utils.get_service(conf)}/artifacts/{artifact_id}',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

    @staticmethod
    def get_artifact(conf, artifact_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            r = requests.get(
                f'{Utils.get_service(conf)}/artifacts/{artifact_id}',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)
        Utils.check_status(r)

        return r.json()

    @staticmethod
    def get_dt(conf, dt_name, param):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            dt_info_response = requests.get(
                f'{Utils.get_service(conf)}/deltatwins/{dt_name}',
                headers={'Authorization': f'Bearer {token}'},
                params=param)
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(dt_info_response)

        return dt_info_response.json()

    @staticmethod
    def publish_dt(conf, data):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            resp = requests.post(
                f'{Utils.get_service(conf)}/deltatwins',
                headers={'Authorization': f'Bearer {token}'},
                json=data
            )
        except (ConnectionError, InvalidSchema):
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(resp)

    @staticmethod
    def publish_version_dt(conf, dt_name, data):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            resp = requests.post(
                f'{Utils.get_service(conf)}/deltatwins/{dt_name}',
                headers={'Authorization': f'Bearer {token}'},
                json=data
            )
        except (ConnectionError, InvalidSchema):
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(resp)

    @staticmethod
    def publish_dt_file(conf, data, file_to_publish):
        """
        Cett fonction renvoie une requete HTTP POST vers delta-api.
        La requete permet d'associer des fichiers à des deltatwin components
        Args:
            conf: la configuration des accès aux différents services autour
            data: les données pour savoir quel fichier associer à quel cmponent
            file_to_publish: le chemin du fichier à associer

        Returns:
            Aucun retour, mais on affiche les logs des appels sous-jacents
        """
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            # convertie depuis Postman
            resp = requests.post(
                url=f'{Utils.get_service(conf)}/deltatwins/'
                    f'{data["deltaTwinName"]}/files',
                headers={
                    'Authorization': f'Bearer {token}',
                    **data
                },
                files=[
                    ('file', ('file', open(file_to_publish, 'rb'),
                              'application/octet-stream'))
                ])
        except (ConnectionError, InvalidSchema):
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(resp)

    @staticmethod
    def get_dt_version(conf, dt_name):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            version_resp = requests.get(
                f'{Utils.get_service(conf)}/deltatwins/{dt_name}/versions',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(version_resp)

        return version_resp.json()

    @staticmethod
    def get_stater_kit(conf):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            starter_kits_response = requests.get(
                f'{Utils.get_service(conf)}/dashboard',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(starter_kits_response)

        return starter_kits_response.json()

    @staticmethod
    def get_dts(conf):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            dt_public = requests.get(
                f'{Utils.get_service(conf)}/deltatwins?visibility=public',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(dt_public)

        try:
            dt_private = requests.get(
                f'{Utils.get_service(conf)}/deltatwins?visibility=private',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(dt_private)

        return dt_private.json() + dt_public.json()

    @staticmethod
    def retrieve_harbor_creds(conf) -> tuple[str, str]:
        conf = Utils.retrieve_conf(conf)
        token = Utils.retrieve_token(conf)
        access_token, _ = Utils.retrieve_harbor_token(path=conf)

        headers = {
            'Authorization': f'Bearer {token}',
            'Harbor-Auth': f'{access_token}'
        }

        try:
            credentials_resp = requests.get(
                f'{Utils.get_service(conf)}/harbor_credentials',
                headers=headers)
            Utils.check_status(credentials_resp)
            data = credentials_resp.json()

            return data["harbor_username"], data["harbor_secret"]
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)
        except Exception:
            click.echo("Error")
            sys.exit(ReturnCode.USAGE_ERROR)

    @staticmethod
    def create_project_harbor(conf,
                              project_name: str,
                              public: bool) -> tuple[str, str]:
        conf = Utils.retrieve_conf(conf)
        token = Utils.retrieve_token(conf)
        access_token, _ = Utils.retrieve_harbor_token(path=conf)

        headers = {
            'Authorization': f'Bearer {token}',
            'Harbor-Auth': f'{access_token}'
        }

        data = {
            "project_name": project_name,
            "public": public
        }
        create_project_resp = requests.post(
            f'{Utils.get_service(conf)}/harbor_create_project',
            headers=headers,
            data=json.dumps(data)
        )
        return create_project_resp.status_code


class ReturnCode:
    INPUT_ERROR = 1  # , "Input Error"
    UNAUTHORIZED = 2  # , "Unauthorized"
    SERVICE_ERROR = 3  # , "Service error"
    SERVICE_NOT_FOUND = 4  # , "Service not found"
    RESOURCE_NOT_FOUND = 5  # , "Resource not found"
    USAGE_ERROR = 6  # , "Usage Error"

    INVALID_RUN_INPUT = 7  # , "Invalid run input"
    REQUIRED_INPUT_MISSING = 8  # , "Required input missing"
