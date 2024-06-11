import pickle

import boto3


def _init_config_s3(self):
    if self.PYTHON_ENV == "production":
        from ..config.s3 import ProductionConfig

        self.s3_config = ProductionConfig()
    elif self.PYTHON_ENV == "staging":
        from ..config.s3 import StagingConfig

        self.s3_config = StagingConfig()
    else:
        from ..config.s3 import DevelopmentConfig

        self.s3_config = DevelopmentConfig()

    pass


def push_model_to_s3(self, model, model_key):
    pickle_byte_obj = pickle.dumps(model)

    _s3_model_obj(self, model_key).put(Body=pickle_byte_obj)

    pass


def load_model_from_s3(self, model_key):
    # Model => S3 => Download Model
    obj = _s3_model_obj(self, model_key)

    return pickle.loads(obj.get()["Body"].read())

# To support custom model loading
def load_model_content_from_s3(self, model_key):
    obj = _s3_model_obj(self, model_key)

    return obj.get()["Body"].read()

def _s3_key_with_default_extension(self, key):
    if "." not in key:
        return f"{key}.pickle"

    return key

def _s3_model_obj(self, model_key):
    bucket_name = self.s3_config.S3_TRAINED_MODELS_BUCKET
    fileprefix = self.get_parameter("logical_step_name")  # Supposed to be step_name
    filepath = _s3_key_with_default_extension(f"{fileprefix}/{model_key}")

    s3 = boto3.resource("s3")

    return s3.Object(bucket_name, filepath)
