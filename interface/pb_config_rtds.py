# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb_config_rtds.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import pb_data_sensor as pb__data__sensor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pb_config_rtds.proto',
  package='com.richisland.proto',
  syntax='proto3',
  serialized_pb=_b('\n\x14pb_config_rtds.proto\x12\x14\x63om.richisland.proto\x1a\x14pb_data_sensor.proto\"q\n\x0epb_config_rtds\x12\x0f\n\x07rtds_id\x18\x01 \x01(\x05\x12\x14\n\x0cupdate_cycle\x18\x02 \x01(\x05\x12\x38\n\ntag_infors\x18\x03 \x03(\x0b\x32$.com.richisland.proto.pb_data_sensorb\x06proto3')
  ,
  dependencies=[pb__data__sensor__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PB_CONFIG_RTDS = _descriptor.Descriptor(
  name='pb_config_rtds',
  full_name='com.richisland.proto.pb_config_rtds',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rtds_id', full_name='com.richisland.proto.pb_config_rtds.rtds_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='update_cycle', full_name='com.richisland.proto.pb_config_rtds.update_cycle', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='tag_infors', full_name='com.richisland.proto.pb_config_rtds.tag_infors', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=181,
)

_PB_CONFIG_RTDS.fields_by_name['tag_infors'].message_type = pb__data__sensor__pb2._PB_DATA_SENSOR
DESCRIPTOR.message_types_by_name['pb_config_rtds'] = _PB_CONFIG_RTDS

pb_config_rtds = _reflection.GeneratedProtocolMessageType('pb_config_rtds', (_message.Message,), dict(
  DESCRIPTOR = _PB_CONFIG_RTDS,
  __module__ = 'pb_config_rtds'
  # @@protoc_insertion_point(class_scope:com.richisland.proto.pb_config_rtds)
  ))
_sym_db.RegisterMessage(pb_config_rtds)


# @@protoc_insertion_point(module_scope)
