# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: assignService.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='assignService.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x13\x61ssignService.proto\"g\n\x06Region\x12\x14\n\x0c\x64omainNumber\x18\x01 \x01(\x05\x12\x0f\n\x07maxSize\x18\x02 \x01(\x05\x12\x13\n\x0b\x63urrentSize\x18\x03 \x01(\x05\x12!\n\x0b\x66ingerPrint\x18\x04 \x03(\x0b\x32\x0c.Fingerprint\";\n\x0b\x46ingerprint\x12\x13\n\x0b\x66ingerPrint\x18\x01 \x01(\x0c\x12\x17\n\x0f\x66ingerPrintSize\x18\x02 \x01(\x05\"]\n\x0f\x41\x63knowledgement\x12\x19\n\x11nonDuplicatesSize\x18\x01 \x01(\x05\x12\x1b\n\x13nonDuplicatesLength\x18\x02 \x01(\x05\x12\x12\n\ncpuPercent\x18\x03 \x01(\x02\"\x07\n\x05\x45mpty\"\"\n\x0fShutDownMessage\x12\x0f\n\x07message\x18\x01 \x01(\t2n\n\x14RegionReceiveService\x12+\n\x0c\x41ssignRegion\x12\x07.Region\x1a\x10.Acknowledgement\"\x00\x12)\n\x0bShutDownPod\x12\x06.Empty\x1a\x10.ShutDownMessage\"\x00\x62\x06proto3'
)




_REGION = _descriptor.Descriptor(
  name='Region',
  full_name='Region',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='domainNumber', full_name='Region.domainNumber', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='maxSize', full_name='Region.maxSize', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='currentSize', full_name='Region.currentSize', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fingerPrint', full_name='Region.fingerPrint', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=126,
)


_FINGERPRINT = _descriptor.Descriptor(
  name='Fingerprint',
  full_name='Fingerprint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='fingerPrint', full_name='Fingerprint.fingerPrint', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fingerPrintSize', full_name='Fingerprint.fingerPrintSize', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=128,
  serialized_end=187,
)


_ACKNOWLEDGEMENT = _descriptor.Descriptor(
  name='Acknowledgement',
  full_name='Acknowledgement',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='nonDuplicatesSize', full_name='Acknowledgement.nonDuplicatesSize', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nonDuplicatesLength', full_name='Acknowledgement.nonDuplicatesLength', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cpuPercent', full_name='Acknowledgement.cpuPercent', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=189,
  serialized_end=282,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=284,
  serialized_end=291,
)


_SHUTDOWNMESSAGE = _descriptor.Descriptor(
  name='ShutDownMessage',
  full_name='ShutDownMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='ShutDownMessage.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=293,
  serialized_end=327,
)

_REGION.fields_by_name['fingerPrint'].message_type = _FINGERPRINT
DESCRIPTOR.message_types_by_name['Region'] = _REGION
DESCRIPTOR.message_types_by_name['Fingerprint'] = _FINGERPRINT
DESCRIPTOR.message_types_by_name['Acknowledgement'] = _ACKNOWLEDGEMENT
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['ShutDownMessage'] = _SHUTDOWNMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Region = _reflection.GeneratedProtocolMessageType('Region', (_message.Message,), {
  'DESCRIPTOR' : _REGION,
  '__module__' : 'assignService_pb2'
  # @@protoc_insertion_point(class_scope:Region)
  })
_sym_db.RegisterMessage(Region)

Fingerprint = _reflection.GeneratedProtocolMessageType('Fingerprint', (_message.Message,), {
  'DESCRIPTOR' : _FINGERPRINT,
  '__module__' : 'assignService_pb2'
  # @@protoc_insertion_point(class_scope:Fingerprint)
  })
_sym_db.RegisterMessage(Fingerprint)

Acknowledgement = _reflection.GeneratedProtocolMessageType('Acknowledgement', (_message.Message,), {
  'DESCRIPTOR' : _ACKNOWLEDGEMENT,
  '__module__' : 'assignService_pb2'
  # @@protoc_insertion_point(class_scope:Acknowledgement)
  })
_sym_db.RegisterMessage(Acknowledgement)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'assignService_pb2'
  # @@protoc_insertion_point(class_scope:Empty)
  })
_sym_db.RegisterMessage(Empty)

ShutDownMessage = _reflection.GeneratedProtocolMessageType('ShutDownMessage', (_message.Message,), {
  'DESCRIPTOR' : _SHUTDOWNMESSAGE,
  '__module__' : 'assignService_pb2'
  # @@protoc_insertion_point(class_scope:ShutDownMessage)
  })
_sym_db.RegisterMessage(ShutDownMessage)



_REGIONRECEIVESERVICE = _descriptor.ServiceDescriptor(
  name='RegionReceiveService',
  full_name='RegionReceiveService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=329,
  serialized_end=439,
  methods=[
  _descriptor.MethodDescriptor(
    name='AssignRegion',
    full_name='RegionReceiveService.AssignRegion',
    index=0,
    containing_service=None,
    input_type=_REGION,
    output_type=_ACKNOWLEDGEMENT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ShutDownPod',
    full_name='RegionReceiveService.ShutDownPod',
    index=1,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_SHUTDOWNMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_REGIONRECEIVESERVICE)

DESCRIPTOR.services_by_name['RegionReceiveService'] = _REGIONRECEIVESERVICE

# @@protoc_insertion_point(module_scope)
