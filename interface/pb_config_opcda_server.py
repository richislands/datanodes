# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb_config_opcda_server.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import pb_config_tag as pb__config__tag__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pb_config_opcda_server.proto',
  package='com.richisland.proto',
  syntax='proto3',
  serialized_pb=_b('\n\x1cpb_config_opcda_server.proto\x12\x14\x63om.richisland.proto\x1a\x13pb_config_tag.proto\"\x9c\x01\n\x16pb_config_opcda_server\x12\x17\n\x0fopcda_server_id\x18\x01 \x01(\x05\x12\x15\n\rrelease_cycle\x18\x02 \x01(\x05\x12\x11\n\ttime_mode\x18\x03 \x01(\x05\x12?\n\x12\x63onfig_tag_release\x18\x04 \x03(\x0b\x32#.com.richisland.proto.pb_config_tagb\x06proto3')
  ,
  dependencies=[pb__config__tag__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PB_CONFIG_OPCDA_SERVER = _descriptor.Descriptor(
  name='pb_config_opcda_server',
  full_name='com.richisland.proto.pb_config_opcda_server',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opcda_server_id', full_name='com.richisland.proto.pb_config_opcda_server.opcda_server_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='release_cycle', full_name='com.richisland.proto.pb_config_opcda_server.release_cycle', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_mode', full_name='com.richisland.proto.pb_config_opcda_server.time_mode', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='config_tag_release', full_name='com.richisland.proto.pb_config_opcda_server.config_tag_release', index=3,
      number=4, type=11, cpp_type=10, label=3,
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
  serialized_start=76,
  serialized_end=232,
)

_PB_CONFIG_OPCDA_SERVER.fields_by_name['config_tag_release'].message_type = pb__config__tag__pb2._PB_CONFIG_TAG
DESCRIPTOR.message_types_by_name['pb_config_opcda_server'] = _PB_CONFIG_OPCDA_SERVER

pb_config_opcda_server = _reflection.GeneratedProtocolMessageType('pb_config_opcda_server', (_message.Message,), dict(
  DESCRIPTOR = _PB_CONFIG_OPCDA_SERVER,
  __module__ = 'pb_config_opcda_server'
  # @@protoc_insertion_point(class_scope:com.richisland.proto.pb_config_opcda_server)
  ))
_sym_db.RegisterMessage(pb_config_opcda_server)


# @@protoc_insertion_point(module_scope)
