def env_global(var_name):
    import os
    return os.getenv(var_name)

def set_env_variables(start_date, end_date, path_data):
    os.environ["start_date"] = start_date
    os.environ["end_date"] = end_date
    os.environ["path_data"] = path_data