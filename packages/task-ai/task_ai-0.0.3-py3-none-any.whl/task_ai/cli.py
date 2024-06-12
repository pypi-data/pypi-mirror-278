import os, sys, json
import click
from task_ai.utils.config_reader import read_config
from task_ai.utils import read_json
from task_ai.processors.anonymizer_processor import AnonymizerProcessor
from task_ai.processors.parsing_processor import ParsingProcessor
from task_ai.processors.description_processor import DescriptionProcessor
import logging
from . import __version__

DEFAULT_CONFIG_PATH = os.path.expanduser('~/.uac/task_ai.yml')

@click.command()
@click.option('--config-file', '-c', type=click.Path(exists=True), default=DEFAULT_CONFIG_PATH, show_default=True, help='Path to the configuration file.')
@click.option('--input', '-i', type=click.File('r'))
@click.option('--log-level', '-l', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']), default='ERROR')
@click.option('--debug', '-d', is_flag=True, default=False, help='Enable debug mode')
@click.option('--show-json', '-s', is_flag=True, default=False, help='Show shorten json')
def main(config_file, input=None, log_level='ERROR', debug=False, show_json=False):
    if debug:
        log_level = 'DEBUG'
    logger = setup_logging(log_level=log_level)

    config = read_config(config_file)
    json_data = read_json(input)
    anonymizer = AnonymizerProcessor(config['anonymization'], logger=logger)
    parser = ParsingProcessor(anonymizer, config, config.get("processing", {}), logger=logger)
    descriptor = DescriptionProcessor(config, logger=logger)
    
    anonymouse_values, removed_values = parser.process(json_data)
    if show_json:
        click.echo(click.style(json.dumps(anonymouse_values, indent=4), fg='blue', bold=True))
    description = descriptor.process(anonymouse_values)
    final_description = descriptor.update_values(description, removed_values)
    
    click.echo(click.style(final_description, fg='green', bold=True))
    
def setup_logging(log_level):
    if log_level != "DEBUG":
        sys.tracebacklimit = 0
    logging.basicConfig(level=log_level)
    logging.info(f'Task AI is running... (Version: {__version__})')
    return logging

if __name__ == "__main__":
    main()