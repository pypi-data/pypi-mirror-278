# -*- coding: utf-8 -*-
import json

import yaml
import click
import os
from computenestcli.processor.service import ServiceProcessor
from computenestcli.processor.check import CheckProcesser
from computenestcli.processor.jinja2 import Jinja2Processor
from computenestcli.service.project_setup import ProjectSetup
from computenestcli.common.context import Context
from computenestcli.common.credentials import Credentials


@click.group()
def main():
    click.echo("Welcome to computenest-cli")


@click.command(name='import')
@click.option('--update_artifact', default=None, help='Whether the artifact needs to be updated')
@click.option('--service_name', default=None, help='Service name')
@click.option('--version_name', default=None, help='Version name')
@click.option('--icon', default=None, help='Icon Oss URL')
@click.option('--desc', default=None, help='Service description')
@click.option('--file_path', required=True, help='File path')
@click.option('--access_key_id', required=True, help='Access Key ID')
@click.option('--access_key_secret', required=True, help='Access Key Secret')
@click.option('--parameters', required=False, default='{}', help='Parameters')
@click.option('--parameter_path', required=False, default='',
              help='Parameter file path, this option overrides parameters')
def import_command(update_artifact, service_name, version_name, icon, desc, file_path, access_key_id, access_key_secret,
                   parameters, parameter_path):
    if file_path is None:
        click.echo('Please provide the file_path')
        return
    if access_key_id is None:
        click.echo('Please provide the access_key_id')
        return
    if access_key_secret is None:
        click.echo('Please provide the access_key_secret')
        return
    if service_name == 'None':
        service_name = None
    if version_name == 'None':
        version_name = None
    if icon == 'None':
        icon = None
    if desc == 'None':
        desc = None
    if parameter_path:
        with open(parameter_path, 'r') as stream:
            parameter_json = yaml.load(stream, Loader=yaml.FullLoader)
    else:
        parameter_json = json.loads(parameters)
    with open(file_path, 'r') as stream:
        data = yaml.load(stream, Loader=yaml.FullLoader)
    region_id = data['Service']['RegionId']
    context = Context(region_id, Credentials(access_key_id, access_key_secret))
    service = ServiceProcessor(context)
    check = CheckProcesser(data, file_path)
    check.processor()
    service.import_command(data_config=data, file_path=file_path, update_artifact=update_artifact,
                           service_name=service_name,
                           version_name=version_name, icon=icon, desc=desc, parameters=parameter_json)


@click.command(name='export')
@click.option('--region_id', required=True, help='Region ID')
@click.option('--service_name', required=True, help='Service name')
@click.option('--file_path', required=True, help='File path')
@click.option('--access_key_id', required=True, help='Access Key ID')
@click.option('--access_key_secret', required=True, help='Access Key Secret')
def export_command(region_id, service_name, file_path, access_key_id, access_key_secret):
    context = Context(region_id, Credentials(access_key_id, access_key_secret))
    service = ServiceProcessor(context)
    service.export_command(service_name, file_path)


@click.command(name='generate')
@click.option('--type', default='file', help='Type of generation, including the whole project or a single file')
@click.option('--file_path', help='File path')
@click.option('--parameters', default='{}', help='Parameters')
@click.option('--output_path', required=True, help='Output path')
@click.option('--parameter_path', required=False, default='',
              help='Parameter file path, this option overrides parameters')
@click.option('--overwrite', '-y', is_flag=True, help='Confirm overwrite of output file without prompt')
def generate_command(file_path, type, parameters, output_path, parameter_path, overwrite):
    jinja2 = Jinja2Processor()
    if parameter_path:
        with open(parameter_path, 'r') as stream:
            parameter_json = yaml.load(stream, Loader=yaml.FullLoader)
    else:
        parameter_json = json.loads(parameters)

    # 如果文件已经存在，向用户提示是否想要继续
    if os.path.exists(output_path) and not overwrite:
        click.confirm(f'The file {output_path} already exists. Do you want to overwrite it?', abort=True)

    if type == 'project':
        project_setup_service = ProjectSetup(output_path, parameter_json)

        project_setup_service.setup_project()
    else:
        jinja2.process(file_path, parameter_json, output_path)


main.add_command(import_command)
main.add_command(export_command)
main.add_command(generate_command)

if __name__ == '__main__':
    main()
