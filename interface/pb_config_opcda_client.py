# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb_config_opcda_client.proto

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
  name='pb_config_opcda_client.proto',
  package='com.richisland.proto',
  syntax='proto3',
  serialized_pb=_b('\n\x1cpb_config_opcda_client.proto\x12\x14\x63om.richisland.proto\x1a\x13pb_config_tag.proto\"\xe5\x01\n\x16pb_config_opcda_client\x12\x17\n\x0fopcda_client_id\x18\x01 \x01(\x05\x12<\n\x0fmain_opc_server\x18\x02 \x01(\x0b\x32#.com.richisland.proto.pb_opc_server\x12<\n\x0f\x62\x61\x63k_opc_server\x18\x03 \x01(\x0b\x32#.com.richisland.proto.pb_opc_server\x12\x36\n\nopc_groups\x18\x04 \x03(\x0b\x32\".com.richisland.proto.pb_opc_group\"\xab\x01\n\rpb_opc_server\x12\x15\n\ropc_server_ip\x18\x01 \x01(\t\x12\x18\n\x10opc_server_prgid\x18\x02 \x01(\t\x12\x18\n\x10opc_server_clsid\x18\x03 \x01(\t\x12\x19\n\x11opc_server_domain\x18\x04 \x01(\t\x12\x17\n\x0fopc_server_user\x18\x05 \x01(\t\x12\x1b\n\x13opc_server_password\x18\x06 \x01(\t\"\x82\x01\n\x0cpb_opc_group\x12\x10\n\x08group_id\x18\x01 \x01(\x05\x12\x12\n\ngroup_name\x18\x02 \x01(\t\x12\x15\n\rcollect_cycle\x18\x03 \x01(\x05\x12\x35\n\x08opc_tags\x18\x04 \x03(\x0b\x32#.com.richisland.proto.pb_config_tagb\x06proto3')
  ,
  dependencies=[pb__config__tag__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PB_CONFIG_OPCDA_CLIENT = _descriptor.Descriptor(
  name='pb_config_opcda_client',
  full_name='com.richisland.proto.pb_config_opcda_client',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opcda_client_id', full_name='com.richisland.proto.pb_config_opcda_client.opcda_client_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='main_opc_server', full_name='com.richisland.proto.pb_config_opcda_client.main_opc_server', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='back_opc_server', full_name='com.richisland.proto.pb_config_opcda_client.back_opc_server', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='opc_groups', full_name='com.richisland.proto.pb_config_opcda_client.opc_groups', index=3,
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
  serialized_end=305,
)


_PB_OPC_SERVER = _descriptor.Descriptor(
  name='pb_opc_server',
  full_name='com.richisland.proto.pb_opc_server',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='opc_server_ip', full_name='com.richisland.proto.pb_opc_server.opc_server_ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='opc_server_prgid', full_name='com.richisland.proto.pb_opc_server.opc_server_prgid', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='opc_server_clsid', full_name='com.richisland.proto.pb_opc_server.opc_server_clsid', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='opc_server_domain', full_name='com.richisland.proto.pb_opc_server.opc_server_domain', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='opc_server_user', full_name='com.richisland.proto.pb_opc_server.opc_server_user', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='opc_server_password', full_name='com.richisland.proto.pb_opc_server.opc_server_password', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=308,
  serialized_end=479,
)


_PB_OPC_GROUP = _descriptor.Descriptor(
  name='pb_opc_group',
  full_name='com.richisland.proto.pb_opc_group',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='group_id', full_name='com.richisland.proto.pb_opc_group.group_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='group_name', full_name='com.richisland.proto.pb_opc_group.group_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='collect_cycle', full_name='com.richisland.proto.pb_opc_group.collect_cycle', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='opc_tags', full_name='com.richisland.proto.pb_opc_group.opc_tags', index=3,
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
  serialized_start=482,
  serialized_end=612,
)

_PB_CONFIG_OPCDA_CLIENT.fields_by_name['main_opc_server'].message_type = _PB_OPC_SERVER
_PB_CONFIG_OPCDA_CLIENT.fields_by_name['back_opc_server'].message_type = _PB_OPC_SERVER
_PB_CONFIG_OPCDA_CLIENT.fields_by_name['opc_groups'].message_type = _PB_OPC_GROUP
_PB_OPC_GROUP.fields_by_name['opc_tags'].message_type = pb__config__tag__pb2._PB_CONFIG_TAG
DESCRIPTOR.message_types_by_name['pb_config_opcda_client'] = _PB_CONFIG_OPCDA_CLIENT
DESCRIPTOR.message_types_by_name['pb_opc_server'] = _PB_OPC_SERVER
DESCRIPTOR.message_types_by_name['pb_opc_group'] = _PB_OPC_GROUP

pb_config_opcda_client = _reflection.GeneratedProtocolMessageType('pb_config_opcda_client', (_message.Message,), dict(
  DESCRIPTOR = _PB_CONFIG_OPCDA_CLIENT,
  __module__ = 'pb_config_opcda_client'
  # @@protoc_insertion_point(class_scope:com.richisland.proto.pb_config_opcda_client)
  ))
_sym_db.RegisterMessage(pb_config_opcda_client)

pb_opc_server = _reflection.GeneratedProtocolMessageType('pb_opc_server', (_message.Message,), dict(
  DESCRIPTOR = _PB_OPC_SERVER,
  __module__ = 'pb_config_opcda_client'
  # @@protoc_insertion_point(class_scope:com.richisland.proto.pb_opc_server)
  ))
_sym_db.RegisterMessage(pb_opc_server)

pb_opc_group = _reflection.GeneratedProtocolMessageType('pb_opc_group', (_message.Message,), dict(
  DESCRIPTOR = _PB_OPC_GROUP,
  __module__ = 'pb_config_opcda_client'
  # @@protoc_insertion_point(class_scope:com.richisland.proto.pb_opc_group)
  ))
_sym_db.RegisterMessage(pb_opc_group)


# @@protoc_insertion_point(module_scope)