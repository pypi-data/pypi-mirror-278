import asyncio
import datetime
import json
import os
import shutil
import signal
import time
import click
import requests

from cli.fingerprint import get_fingerprint
from cli.lib import create_venv, get_and_download_plugin, get_current_user, get_inference_job, get_my_workers, install_requirements, install_torch_requirements, login_with_token, post_register_worker, process_inference_job, run_plugin

@click.group()
def cli():
    pass

@click.command(help="Share my AI CLI - Help")
def help():
    click.echo(f'Help:')
    click.echo(f'  - help: Show this help message')
    return

@click.command(help="Login with a token")
@click.option('--token', required=True, help='Your login token')
def login(token):
    logged_in_user = login_with_token(token)
    if not logged_in_user:
        click.echo('Login failed, please try again.')
        return
    click.echo(f'Logged in successfully as {logged_in_user["name"]} - {logged_in_user["id"]}')
    return

@click.command(help="Get the current user")
def current_user():
    user = get_current_user()
    formatted_json = json.dumps(user, indent=4, sort_keys=True)
    click.echo(f'Current user:\n{formatted_json}')
    return

@click.command(help="Get the current machines fingerprint")
def fingerprint():
    fingerprint_bytes = asyncio.run(get_fingerprint())
    fingerprint_str = fingerprint_bytes.hex()
    click.echo(f'Fingerprint: {fingerprint_str}')
    return

@click.command(help="Register new worker")
@click.option('--plugin_id', required=True, help='The plugin id to work on')
def register_worker(plugin_id):
    worker = post_register_worker(plugin_id)
    formatted_json = json.dumps(worker, indent=4, sort_keys=True)
    click.echo(f'Worker:\n{formatted_json}')
    return

@click.command(help="Get my workers")
def my_workers():
    workers = get_my_workers()
    formatted_json = json.dumps(workers, indent=4, sort_keys=True)
    click.echo(f'Workers:\n{formatted_json}')
    return

@click.command(help="Run worker")
@click.option('--plugin_id', required=True, help='The plugin id to work on')
def run_worker(plugin_id):
    # first, register a worker
    worker = post_register_worker(plugin_id)
    formatted_json = json.dumps(worker, indent=4, sort_keys=True)
    click.echo(f'Worker:\n{formatted_json}')
    # then, download the plugin
    plugin, plugin_path = get_and_download_plugin(plugin_id)
    click.echo(f'Plugin downloaded to {plugin_path}')
    # then, create a venv for the plugin
    venv_path = create_venv(plugin_path)
    click.echo(f'Venv created at {venv_path}')
    # then, install the plugin requirements
    install_torch_requirements(venv_path, plugin['torchRequirements'])
    install_requirements(venv_path, plugin['requirements'])
    click.echo(f'Requirements installed')
    # then, run the plugin
    pid = run_plugin(venv_path, plugin_path, plugin['name'])
    try:
        while True:
            click.echo(f'Checking for jobs - {datetime.datetime.now()}...')
            job = get_inference_job(worker['id'])
            if not job:
                click.echo(f'No job found - {datetime.datetime.now()}...')
                time.sleep(5)
                continue
            click.echo(f'Job found: {job}')
            # process it 
            process_inference_job(
                job['params'].get('prompt', ''),
                job['params'].get('image', ''),
                job['params'],
                plugin['params'],
                job['id']
            )
            time.sleep(5)
    except KeyboardInterrupt:
        click.echo(f'Stopping plugin - {datetime.datetime.now()}...')
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    click.echo(f'Plugin stopped - {datetime.datetime.now()}...')
    return

PLUGIN_BASE_DIR = './plugin_cache'

@click.command(help="Run worker that will dynamically download and run plugins")
@click.option('--reset', default=False, help='Reset the worker')
def run_multiplugin_worker(reset):
    # if we are resetting, delete all our downloaded plugins 
    if reset:
        for item in os.listdir(PLUGIN_BASE_DIR):
            item_path = os.path.join(PLUGIN_BASE_DIR, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        click.echo(f'Deleted all downloaded plugins')
        return

    # first, register a worker
    worker = post_register_worker()
    formatted_json = json.dumps(worker, indent=4, sort_keys=True)
    click.echo(f'Worker:\n{formatted_json}')

    cached_plugins_file = "cached_plugins.json"
    if os.path.exists(cached_plugins_file):
        with open(cached_plugins_file, "r") as f:
            cached_plugins = json.load(f)
    else:
        cached_plugins = {"current": ""}

    while True:
        try:
            click.echo(f'Checking for jobs - {datetime.datetime.now()}...')
            job = get_inference_job(worker['id'])
            if not job:
                click.echo(f'No job found - {datetime.datetime.now()}...')
                time.sleep(5)
                continue

            click.echo(f'Job found: {job}')

            # get the plugin id from the job
            plugin_id = job['pluginId']

            if cached_plugins["current"] != plugin_id:
                # kill any other running plugins 
                for plugin_key in cached_plugins:
                    if plugin_key != "current":
                        pid = cached_plugins[plugin_key].get('pid')
                        if pid:
                            try:
                                os.kill(pid, signal.SIGTERM)
                            except ProcessLookupError:
                                pass
                            click.echo(f'Plugin stopped - {datetime.datetime.now()}...')

                # if the plugin is not the same as the current one, update the current one
                cached_plugins["current"] = plugin_id

                if plugin_id in cached_plugins:
                    # if the plugin is already cached, use the cached version
                    plugin = cached_plugins[plugin_id]['plugin']
                    plugin_path = cached_plugins[plugin_id]['plugin_path']
                    venv_path = cached_plugins[plugin_id]['venv_path']
                    click.echo(f'Using cached plugin: {plugin_id}')
                else:
                    # if the plugin is not cached, download and set it up
                    plugin, plugin_path = get_and_download_plugin(plugin_id, PLUGIN_BASE_DIR)
                    click.echo(f'Plugin downloaded to {plugin_path}')

                    venv_path = create_venv(plugin_path)
                    click.echo(f'Venv created at {venv_path}')

                    install_torch_requirements(venv_path, plugin['torchRequirements'])
                    install_requirements(venv_path, plugin['requirements'])
                    click.echo(f'Requirements installed')

                    # cache the plugin for future use
                    cached_plugins[plugin_id] = {
                        'plugin': plugin,
                        'plugin_path': plugin_path,
                        'venv_path': venv_path
                    }
                    # save the updated cached_plugins to file
                    with open(cached_plugins_file, "w") as f:
                        json.dump(cached_plugins, f)
            else:
                venv_path = cached_plugins[plugin_id]['venv_path']
                plugin_path = cached_plugins[plugin_id]['plugin_path']
                plugin = cached_plugins[plugin_id]['plugin']
                
            # run the plugin only if it's not already running
            if 'pid' not in cached_plugins[plugin_id] or not cached_plugins[plugin_id]['pid']:
                pid = run_plugin(venv_path, plugin_path, plugin['name'])
                cached_plugins[plugin_id]['pid'] = pid
            else:
                pid = cached_plugins[plugin_id]['pid']
                # check that the pid exists
                try:
                    response = requests.get(f"http://localhost:3030/healthcheck")
                except Exception as e:
                    print('Healthcheck failed, plugin needs restart')
                    pid = run_plugin(venv_path, plugin_path, plugin['name'])
                    cached_plugins[plugin_id]['pid'] = pid

            # wait till we get a response from our healthcheck endpoint
            while True:
                print('Waiting for healthcheck...')
                try:
                    response = requests.get(f"http://localhost:3030/healthcheck")
                except Exception as e:
                    print('Healthcheck failed, retrying in 5 seconds...')
                    time.sleep(5)
                    continue
                if response.status_code == 200:
                    print('Healthcheck passed, continuing...')
                    break
                print('Healthcheck failed, retrying in 5 seconds...')
                time.sleep(5)

            # process the job
            process_inference_job(
                job['params'].get('prompt', ''),
                job['params'].get('image', ''),
                job['params'],
                plugin['params'],
                job['id']
            )

        except KeyboardInterrupt:
            click.echo(f'Stopping worker - {datetime.datetime.now()}...')
            break
    return

cli.add_command(help)
cli.add_command(login)
cli.add_command(current_user)
cli.add_command(fingerprint)
cli.add_command(register_worker)
cli.add_command(my_workers)
cli.add_command(run_worker)
cli.add_command(run_multiplugin_worker)



