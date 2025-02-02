import argparse
import logging

base_dir = "/opt/ml/processing"

logger = logging.getLogger("acs_features")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('acs_features %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def get_input_path(name):
    return f"{base_dir}/input/{name}"


def get_output_path(name):
    return f"{base_dir}/output/{name}"


def get_args(name, arg_type=str, default=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--" + name, type=arg_type, default=default)
    args, _ = parser.parse_known_args()
    return getattr(args, name)


def get_args_schema():
    return get_args("schema", default="stage")


def get_args_schema_path():
    return get_args("schema_path", default="s3://hyun/stage")


def log_info(*message):
    logger.info(message)


def log_exception(message):
    logger.exception(message)


def get_code_url(schema_path, file_name):
    return f"{schema_path}/code/{file_name}"


def get_pipeline_zip_url(schema_path):
    return get_code_url(schema_path, "acs_features.zip")


# There is a case no log exist. so, when start, print log. so that, the task is processed
log_info("Started")