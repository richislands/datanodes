# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb_config_opcalarm_server.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pb_config_opcalarm_server.proto',
  package='com.richisland.proto',
  syntax='proto3',
  serialized_pb=_b('\n\x1fpb_config_opcalarm_server.proto\x12\x14\x63om.richisland.proto\"L\n\x19pb_config_opcalarm_server\x12\x1a\n\x12opcalarm_server_id\x18\x01 \x01(\x05\x12\x13\n\x0bupdate_rate\x18\x02 \x01(\x05\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PB_CONFIG_OPCALARM_SERVER = _descriptor.Descriptor(
  name='pb_config_opcalarm_server',
  full_name='com.richisland.proto.pb_config_opcalarm_server',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opcalarm_server_id', full_name='com.richisland.proto.pb_config_opcalarm_server.opcalarm_server_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='update_rate', full_name='com.richisland.proto.pb_config_opcalarm_server.update_rate', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=57,
  serialized_end=133,
)

DESCRIPTOR.message_types_by_name['pb_config_opcalarm_server'] = _PB_CONFIG_OPCALARM_SERVER

pb_config_opcalarm_server = _reflection.GeneratedProtocolMessageType('pb_config_opcalarm_server', (_message.Message,), dict(
  DESCRIPTOR = _PB_CONFIG_OPCALARM_SERVER,
  __module__ = 'pb_config_opcalarm_server'
  # @@protoc_insertion_point(class_scope:com.richisland.proto.pb_config_opcalarm_server)
  ))
_sym_db.RegisterMessage(pb_config_opcalarm_server)


# @@protoc_insertion_point(module_scope)
