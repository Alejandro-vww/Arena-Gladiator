import json
import logging, logging.config
import os

class JsonToDict:
    buffer = None
    @staticmethod
    def get_dict(line):
        """
        Parses a JSON string and returns a dictionary.

        Args:
            line (str): A string that potentially contains JSON data.

        Returns:
            dict or None: The parsed JSON as a dictionary, or None if parsing fails.
        """

        if line.startswith('[UnityCrossThreadLogger]Client.SceneChange {'):
            line = line[43:]  # Dict part

        # Para diccionarios en varias líneas
        if line == '{\n':
            JsonToDict.buffer = line.strip()
        elif JsonToDict.buffer:
            JsonToDict.buffer = JsonToDict.buffer + line.strip()
        if line == '}\n':
            line = JsonToDict.buffer
            JsonToDict.buffer = False
            dic = json.loads(line)

        try:
            dic = json.loads(line)
        except Exception as e:
            return None

        return dic if isinstance(dic, dict) else None

