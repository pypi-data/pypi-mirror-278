import argparse
import platformdirs
from pathlib import Path
import shutil
from .patient import Patient
from .parameter_parser import parameter_parser

appname = 'pyrt_lib'

config_dir = platformdirs.user_config_dir(appname)
default_database_dir = platformdirs.user_data_dir(appname)
default_database_path = Path(default_database_dir)
config_path = Path(config_dir)
config_file_name = "pyrt_lib_config.conf"
config_file_path = config_path / config_file_name

def add_patient_to_database(database_name, patient_path):
    database_path = get_database_path(database_name)
    new_patient = load_patient(patient_path)
    database = load_database(database_name)
    for patient in database:
        if int(float(patient["patient id"])) == int(new_patient.patient_id):
            return
    # patient is not in the databse, so we can just add it
    parameter_list = load_parameter_list(database_name)
    patient_data = [patient_path]
    for param in parameter_list:
        param_value = parameter_parser(new_patient, param)
        patient_data.append(param_value)
    with open(database_path,"a") as f:
        for i, param in enumerate(patient_data):
            if i == 0:
                f.write("{}".format(param))
                continue
            f.write(",{}".format(param))
        f.write("\n")
    
    


def load_patient(patient_path):
    return Patient(patient_path, wanted_structures="default")

def get_database_path(database_name):
    # Returns a list of dictionaries, each list element relating to a patient.

    database_path = ""
    with open(str(config_file_path), 'r') as f:
        for line in f:
            this_database_path = line.split(":")[0].strip()
            this_database_name = str(Path(this_database_path).name).strip()
            if this_database_name == database_name:
                database_path = this_database_path
                break
    if database_path == "":
        raise ValueError("Database name {} not found in config file: {}".format(database_name, str(config_file_path)))
    
    return database_path

def get_parameter_list_path(database_name):
    parameter_list_path = ""
    with open(str(config_file_path), 'r') as f:
        for line in f:
            this_database_path = line.split(":")[0].strip()
            this_parameter_list_path = line.split(":")[1].strip()
            this_database_name = str(Path(this_database_path).name).strip()
            if this_database_name == database_name:
                parameter_list_path = this_parameter_list_path
                break
    if parameter_list_path == "":
        raise ValueError("Database name {} not found or no parameter list file found in config file: {}".format(database_name, str(config_file_path)))
    
    return parameter_list_path

def load_parameter_list(database_name):
    # Returns list of parameters in file corresponding to database_name
    parameter_list_path = get_parameter_list_path(database_name)
    parameter_list = []
    with open(parameter_list_path, "r") as f:
        for line in f:
            if "," in line:
                raise ValueError("Parameter file {} for database name {} appears to have more than 1 parameter per line".format(parameter_list_path,database_name))
            parameter_list.append(line.strip())

    return parameter_list

def load_database(database_name):
    # Should return a database, i.e. a list of dicts
    database_path = get_database_path(database_name)
    database = []
    header = []
    with open(database_path, "r") as f:
        for i, line in enumerate(f):
            if i == 0:
                header = line.strip().split(",")
                continue
            patient_dict = {}
            for j, entry in enumerate(line.strip().split(",")):
                entry=entry.strip()
                if j == 0:
                    # By our definitions, this will always be the path to the patient directory
                    patient_dict["path"] = entry
                    continue
                param = header[j]
                patient_dict[param] = entry
            database.append(patient_dict)
    return database

                

def write_database(database, database_name):
    database_path = get_database_path(database_name)        
    if len(database) == 0:
        raise ValueError("Attempting to write empty database in {}".format(database_path))            
    header = list(database[0].keys())
    with open(database_path, "w") as f:
        for i, entry in enumerate(header):
            if i == 0:
                f.write("{}".format(entry))
                continue
            f.write(",{}".format(entry))
        f.write("\n")
        for patient in database[1:]:
            values = list(patient.values())
            for i, val in enumerate(values):
                if i==0:
                    f.write("{}".format(val))
                    continue
                f.write(",{}".format(val))
            f.write("\n")




def update_database(database_name):
    # This function should update the database according to the param file in the config file

    parameter_set = load_parameter_list(database_name)

    database = load_database(database_name)
    parameter_set = ["path"] + parameter_set
    new_database = [{l:l for l in parameter_set}]
    for patient in database:
        # database is list of dicts
        new_pat = {}
        patient_path = patient["path"]
        loaded_patient = None
        for param in parameter_set:
            if param in patient:
                new_pat[param] = patient[param]
                continue 
            # now we need to load the patient because the parameter was not found
            if loaded_patient is None:
                loaded_patient = load_patient(patient_path)
            new_pat[param] = parameter_parser(loaded_patient, param)
        # All parameters in the new parameter file have been set
        new_database.append(new_pat)
    write_database(new_database, database_name)
    


def edit_database(database, new_param_file):
    if not Path(new_param_file).exists() or not Path(new_param_file).is_file():
        raise ValueError("Parameter file at {} does either not exist or is not a file".format(new_param_file))

    shutil.copyfile(new_param_file, str(config_path / Path(new_param_file).name ))

    with open(config_file_path.absolute(), "r+") as f:
        lines=f.readlines()
        f.seek(0)
        for line in lines:
            if str(Path(line.split(":")[0]).name).strip() == database:
                origpath = line.split(":")[0]
                line = origpath + ":" + str(config_path / Path(new_param_file).name ) + "\n"
            f.write(line)
        f.truncate()
    
    update_database(database)


def create_new_database(new_database_path, parameter_file, only_name = False):
    
    if only_name:
        new_database_path = str(default_database_path / new_database_path)

        if not default_database_path.exists():
            default_database_path.mkdir()

    if not Path(new_database_path).parent.exists() and not Path(new_database_path).parent.is_dir():
        raise ValueError("New database entry at {} is not placed in a valid directory".format(new_database_path))
    if Path(new_database_path).exists():
        raise ValueError("The new database file name: {} already exists".format(new_database_path))

    if not Path(parameter_file).exists() or not Path(parameter_file).is_file():
        raise ValueError("Parameter file at {} does either not exist or is not a file".format(parameter_file))
    
    Path(new_database_path).touch()
    new_param_file_path = str(config_path / Path(parameter_file).name )
    shutil.copyfile(parameter_file, new_param_file_path)
    
    database_name = str(Path(new_database_path).name)


    add_database_to_config(str(Path(new_database_path).absolute()), str(config_path / parameter_file))

    update_database(database_name)



def ensure_database_present():
    if not config_path.exists() and not config_path.is_dir():
        config_path.mkdir()
    if not config_file_path.exists() and not config_file_path.is_file():
        config_file_path.touch()

def add_database_to_config(new_database_path, parameter_file):
    ensure_database_present()

    if not Path(new_database_path).exists() or not Path(new_database_path).is_file():
        raise ValueError("New database entry at {} does not exist or is not a file".format(new_database_path))

    with open(config_file_path.absolute(), "r") as f:
        for line in f:
            strpline=line.strip().split(":")[0]
            if Path(new_database_path).samefile(Path(strpline)):
                return

    endd = "\n"
    if "\n" in new_database_path:
        new_database_path = new_database_path.replace("\n","")
    with open(config_file_path.absolute(), "a") as f:
        f.write(new_database_path + " : " + parameter_file +endd)

def list_all_databases():
    ensure_database_present()
    
    config_lines = []
    with open(config_file_path.absolute(), "r") as f:
        for line in f:
            config_lines.append(line)
    for line in config_lines:
        endd="\n"
        if "\n" in line:
            endd=""
        print(line, end=endd)

def main():
    parent_parser = argparse.ArgumentParser(add_help=False)

    main_parser = argparse.ArgumentParser()

    main_option_subparsers = main_parser.add_subparsers(title="Type of action", dest='command')

    add_patient_subparser = main_option_subparsers.add_parser("add", help="Adds patient to existing database",
                        parents=[parent_parser])
    add_patient_subparser.add_argument("database_name", help="Database name to which we add the patient")
    add_patient_subparser.add_argument("patient_path", help="Path to the patient directory to add to the database")

    remove_patient_subparser = main_option_subparsers.add_parser("remove", help="Removes a patient from an existing database",
                        parents=[parent_parser])

    create_database_subparser = main_option_subparsers.add_parser("create", help="Creates a new database",
                        parents=[parent_parser])
    create_database_subparser.add_argument("database", help="Path to the database to be created at the supplied path")
    create_database_subparser.add_argument("--name", help="Only supply name for new database. Will be placed in {}".format(default_database_dir),
                                           action="store_true")
    create_database_subparser.add_argument("-p","--parameter-list", required=True, help="Path to file with parameters to include in database. One paramater per line.")

    config_database_subparser = main_option_subparsers.add_parser("config", help="Configures an existing database",
                        parents=[parent_parser])

    config_main_subparsers = config_database_subparser.add_subparsers(title="Type of action", dest='command')

    config_add_subparser = config_main_subparsers.add_parser("add-existing", help="Adds an existing database path to the config file")
    config_add_subparser.add_argument("database", help="Path to the database which is to be added to the config file")

    config_list_subparser = config_main_subparsers.add_parser("list", help="Lists all database paths present in the config file")

    config_edit_subparser = config_main_subparsers.add_parser("edit", help="Edits a database")
    config_edit_subparser.add_argument("database_name", help="Name of database to edit")
    config_edit_subparser.add_argument("--set-params", required=True, help="Path to new parameter list to use for database")


    args = main_parser.parse_args()
    match args.command:
        case "list":
            list_all_databases()
        case "add":
            add_patient_to_database(args.database_name, args.patient_path)
        case "add-existing":
            add_database_to_config(args.database)
        case "create":
            create_new_database(args.database, args.parameter_list ,only_name = args.name)
        case "edit":
            edit_database(args.database_name, args.set_params)
        case "remove":
            raise NotImplementedError("Removing patients has not been implemented yet.")
            remove_patient_from_database(args.patient_id)


if __name__ == "__main__":
    main()
    

