from json import JSONEncoder

# override default JSON encoder to look for `to_dict` method
def json_encoder_override(self, obj):
  return getattr(
    obj.__class__,
    "to_dict",
    json_encoder_override.default
  )(obj)
json_encoder_override.default = JSONEncoder().default
JSONEncoder.default = json_encoder_override
