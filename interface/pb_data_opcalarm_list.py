# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb_data_opcalarm_list.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import pb_data_opcalarm as pb__data__opcalarm


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pb_data_opcalarm_list.proto',
  package='com.richisland.proto',
  syntax='proto3',
  serialized_pb=_b('\n\x1bpb_data_opcalarm_list.proto\x12\x14\x63om.richisland.proto\x1a\x16pb_data_opcalarm.proto\"k\n\x15pb_data_opcalarm_list\x12\x0f\n\x07list_id\x18\x01 \x01(\x05\x12\x41\n\x11pb_data_opcalarms\x18\x02 \x03(\x0b\x32&.com.richisland.proto.pb_data_opcalarmb\x06proto3')
  ,
  dependencies=[pb__data__opcalarm.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PB_DATA_OPCALARM_LIST = _descriptor.Descriptor(
  name='pb_data_opcalarm_list',
  full_name='com.richisland.proto.pb_data_opcalarm_list',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='list_id', full_name='com.richisland.proto.pb_data_opcalarm_list.list_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pb_data_opcalarms', full_name='com.richisland.proto.pb_data_opcalarm_list.pb_data_opcalarms', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=77,
  serialized_end=184,
)

_PB_DATA_OPCALARM_LIST.fields_by_name['pb_data_opcalarms'].message_type = pb__data__opcalarm._PB_DATA_OPCALARM
DESCRIPTOR.message_types_by_name['pb_data_opcalarm_list'] = _PB_DATA_OPCALARM_LIST

pb_data_opcalarm_list = _reflection.GeneratedProtocolMessageType('pb_data_opcalarm_list', (_message.Message,), dict(
  DESCRIPTOR = _PB_DATA_OPCALARM_LIST,
  __module__ = 'pb_data_opcalarm_list'
  # @@protoc_insertion_point(class_scope:com.richisland.proto.pb_data_opcalarm_list)
  ))
_sym_db.RegisterMessage(pb_data_opcalarm_list)


# @@protoc_insertion_point(module_scope)
