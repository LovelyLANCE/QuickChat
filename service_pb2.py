# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\x12\x03rpc\"\'\n\x11\x43hatInviteRequest\x12\x12\n\ninviter_ip\x18\x01 \x01(\t\"4\n\x12\x43hatInviteResponse\x12\x10\n\x08\x61\x63\x63\x65pted\x18\x01 \x01(\x08\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x94\x01\n\x15\x43hatMemberInfoRequest\x12\x38\n\x07members\x18\x01 \x03(\x0b\x32\'.rpc.ChatMemberInfoRequest.MembersEntry\x12\x11\n\ttimestamp\x18\x02 \x01(\t\x1a.\n\x0cMembersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"+\n\x16\x43hatMemberInfoResponse\x12\x11\n\tconfirmed\x18\x01 \x01(\x08\"H\n\x12\x43hatMessageRequest\x12\x11\n\tsender_ip\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0e\n\x06vclock\x18\x03 \x03(\x04\"&\n\x13\x43hatMessageResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xea\x01\n\x10QuickChatService\x12\x41\n\x0eSendChatInvite\x12\x16.rpc.ChatInviteRequest\x1a\x17.rpc.ChatInviteResponse\x12M\n\x12SendChatMemberInfo\x12\x1a.rpc.ChatMemberInfoRequest\x1a\x1b.rpc.ChatMemberInfoResponse\x12\x44\n\x0fSendChatMessage\x12\x17.rpc.ChatMessageRequest\x1a\x18.rpc.ChatMessageResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CHATMEMBERINFOREQUEST_MEMBERSENTRY']._options = None
  _globals['_CHATMEMBERINFOREQUEST_MEMBERSENTRY']._serialized_options = b'8\001'
  _globals['_CHATINVITEREQUEST']._serialized_start=22
  _globals['_CHATINVITEREQUEST']._serialized_end=61
  _globals['_CHATINVITERESPONSE']._serialized_start=63
  _globals['_CHATINVITERESPONSE']._serialized_end=115
  _globals['_CHATMEMBERINFOREQUEST']._serialized_start=118
  _globals['_CHATMEMBERINFOREQUEST']._serialized_end=266
  _globals['_CHATMEMBERINFOREQUEST_MEMBERSENTRY']._serialized_start=220
  _globals['_CHATMEMBERINFOREQUEST_MEMBERSENTRY']._serialized_end=266
  _globals['_CHATMEMBERINFORESPONSE']._serialized_start=268
  _globals['_CHATMEMBERINFORESPONSE']._serialized_end=311
  _globals['_CHATMESSAGEREQUEST']._serialized_start=313
  _globals['_CHATMESSAGEREQUEST']._serialized_end=385
  _globals['_CHATMESSAGERESPONSE']._serialized_start=387
  _globals['_CHATMESSAGERESPONSE']._serialized_end=425
  _globals['_QUICKCHATSERVICE']._serialized_start=428
  _globals['_QUICKCHATSERVICE']._serialized_end=662
# @@protoc_insertion_point(module_scope)