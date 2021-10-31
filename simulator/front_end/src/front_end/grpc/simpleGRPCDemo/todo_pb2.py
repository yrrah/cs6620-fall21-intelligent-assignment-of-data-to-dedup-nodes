# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: todo.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='todo.proto',
  package='todoPackage',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\ntodo.proto\x12\x0btodoPackage\"\x07\n\x05\x45mpty\"$\n\x08TodoItem\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04text\x18\x02 \x01(\t\"1\n\tTodoItems\x12$\n\x05items\x18\x01 \x03(\x0b\x32\x15.todoPackage.TodoItem2{\n\x04Todo\x12:\n\ncreateTodo\x12\x15.todoPackage.TodoItem\x1a\x15.todoPackage.TodoItem\x12\x37\n\treadTodos\x12\x12.todoPackage.Empty\x1a\x16.todoPackage.TodoItemsb\x06proto3'
)




_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='todoPackage.Empty',
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
  serialized_start=27,
  serialized_end=34,
)


_TODOITEM = _descriptor.Descriptor(
  name='TodoItem',
  full_name='todoPackage.TodoItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='todoPackage.TodoItem.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='todoPackage.TodoItem.text', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=36,
  serialized_end=72,
)


_TODOITEMS = _descriptor.Descriptor(
  name='TodoItems',
  full_name='todoPackage.TodoItems',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='items', full_name='todoPackage.TodoItems.items', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=74,
  serialized_end=123,
)

_TODOITEMS.fields_by_name['items'].message_type = _TODOITEM
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['TodoItem'] = _TODOITEM
DESCRIPTOR.message_types_by_name['TodoItems'] = _TODOITEMS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'todo_pb2'
  # @@protoc_insertion_point(class_scope:todoPackage.Empty)
  })
_sym_db.RegisterMessage(Empty)

TodoItem = _reflection.GeneratedProtocolMessageType('TodoItem', (_message.Message,), {
  'DESCRIPTOR' : _TODOITEM,
  '__module__' : 'todo_pb2'
  # @@protoc_insertion_point(class_scope:todoPackage.TodoItem)
  })
_sym_db.RegisterMessage(TodoItem)

TodoItems = _reflection.GeneratedProtocolMessageType('TodoItems', (_message.Message,), {
  'DESCRIPTOR' : _TODOITEMS,
  '__module__' : 'todo_pb2'
  # @@protoc_insertion_point(class_scope:todoPackage.TodoItems)
  })
_sym_db.RegisterMessage(TodoItems)



_TODO = _descriptor.ServiceDescriptor(
  name='Todo',
  full_name='todoPackage.Todo',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=125,
  serialized_end=248,
  methods=[
  _descriptor.MethodDescriptor(
    name='createTodo',
    full_name='todoPackage.Todo.createTodo',
    index=0,
    containing_service=None,
    input_type=_TODOITEM,
    output_type=_TODOITEM,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='readTodos',
    full_name='todoPackage.Todo.readTodos',
    index=1,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_TODOITEMS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TODO)

DESCRIPTOR.services_by_name['Todo'] = _TODO

# @@protoc_insertion_point(module_scope)
