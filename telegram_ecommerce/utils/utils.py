from json import load


def load_file(path):
    with open(path, "r") as io_file:
        return io_file.read()


def load_json_file(path):
    with open(path, "r") as json_string:
        return load(json_string)

def get_sql_commands_from_a_file(path, delimiter=";"):
    sql = load_file(path)
    commands = ( sql
        .replace("\n", "")
        .split(delimiter)
        )
    commands.pop()
    return commands

