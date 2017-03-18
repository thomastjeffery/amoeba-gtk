import unittest
import json

class Config(dict):
    """Configuration

    """

    def __init__(self, filename=None, config=None):
        """Creates a new config

        filename:
            a JSON file to load
        config:
            a Config or dict to inherit from
        
        If both "filename" and "config" are set, the file is loaded first,
        then "config" is merged.
        """
        if filename:
            self.load_file(filename)
        if config:
            self.merge(config)

    def merge(self, config):
        """Merges a new Config into self.

        Attributes from the new Config overwrite any already defined by self.
        """

        for key, value in config.items():
            self[key] = value

    def load_file(self, filename):
        """Merges the configuration described in json file

        """

        file = open(filename, 'r')

        self.merge(json.load(file))

        file.close()


class ConfigTest(unittest.TestCase):
    def test_init(self):
        # No arguments
        simple = Config()
        simple["one"] = 1
        self.assertEqual(simple["one"], 1)

        # Config as argument
        derived = Config(config=simple)
        self.assertEqual(derived["one"], 1)

        # dict as argument
        from_dict = Config(config={
            "one": "one"
        })
        self.assertEqual(from_dict["one"], "one")

        # Filename as argument
        from_file = Config(filename="config.json")
        self.assertEqual(from_file["font"]["family"], "Monospace")

        # filename and config both defined
        from_file_and_derived = Config(filename="config.json", config={
            "font": {
                "family": "DejaVu Sans Mono"
            }
        })
        self.assertEqual(from_file_and_derived["font"]["family"], "DejaVu Sans Mono")


    def test_merge(self):
        config = Config()

        config["foo"] = "foo"
        config["bar"] = "bar"

        new_config = Config()
        new_config["foo"] = "Foo"
        new_config["baz"] = "Baz"

        config.merge(new_config)

        for key in ["foo", "baz"]:
            self.assertEqual(config[key], new_config[key])

        self.assertEqual(config["bar"], "bar")

    def test_load_file(self):
        config = Config()

        config["font"] = "Overwrite me!"

        config.load_file("config.json")

        self.assertEqual(config["font"]["family"], "Monospace")

if __name__ == "__main__":
    unittest.main()