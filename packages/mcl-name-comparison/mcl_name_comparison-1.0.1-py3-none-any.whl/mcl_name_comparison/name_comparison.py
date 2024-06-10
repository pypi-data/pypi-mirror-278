import torch
import os
import warnings
from pprint import pprint
from sentence_transformers import SentenceTransformer, util

warnings.filterwarnings("ignore", category=FutureWarning)


class NameComparison:
    def __init__(self, token=None):
        os.makedirs("./priv_model", exist_ok=True)
        self.model = SentenceTransformer("MCLinguistX/name-correlation-model", token=token, cache_folder="./priv_model")
        os.system("rm -rf ./priv_model")

    def get_comparison(self, name1: str, name2: str) -> float:
        """Returns the similarity score between two names

        Args:
            name1 (str)
            name2 (str)

        Returns:
            float: similarity score between names in [0, 1]
        """
        assert type(name1) == str and type(name2) == str, "Both inputs must be strings"
        try:
            response = util.pytorch_cos_sim(
                self.model.encode(name2, devices="cuda"),
                self.model.encode(name1, devices="cuda"),
            ).item()
        except:
            response = util.pytorch_cos_sim(
                self.model.encode(name1),
                self.model.encode(name2),
            ).item()
        return response
