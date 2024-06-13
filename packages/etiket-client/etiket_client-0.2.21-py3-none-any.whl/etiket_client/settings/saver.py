import dataclasses, yaml, os, enum

class settings_saver:
    @classmethod
    def load(cls):
        if not os.path.isfile(cls._config_file):
            settings = cls()
            with open(cls._config_file, 'w') as file:
                yaml.dump(
                    clean_data_for_saving(dataclasses.asdict(settings), dataclasses.fields(cls)) ,
                    file)
            return settings
        else:
            with open(cls._config_file, 'r') as file:
                config = yaml.safe_load(file)
                if config is None:
                    config = {}

            fields = dataclasses.fields(cls)
            kwargs = {k.name : None for k in fields}
            for field in fields:
                if field.name in config.keys():
                    if issubclass(field.type, enum.Enum):
                        setattr(cls, field.name , field.type(config[field.name]))
                    else:
                        setattr(cls, field.name , config[field.name])
        
        return cls(**kwargs)

    @classmethod
    def write(cls):
        with open(cls._config_file, 'r') as file:
            config = yaml.safe_load(file)
            if config is None:
                config = {}

        fields = dataclasses.fields(cls)
        for field in fields:
            config[field.name] = getattr(cls, field.name)

        with open(cls._config_file, 'w') as file:
            yaml.dump(clean_data_for_saving(config, fields), file)

def clean_data_for_saving(data, fields):
    for field in fields:
        if field.name in data.keys():
            if issubclass(field.type, enum.Enum):
                data[field.name] = data[field.name].value

    return data