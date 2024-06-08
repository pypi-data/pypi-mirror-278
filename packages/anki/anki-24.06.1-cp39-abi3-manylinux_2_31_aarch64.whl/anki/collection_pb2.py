# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: anki/collection.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from anki import generic_pb2 as anki_dot_generic__pb2
from anki import sync_pb2 as anki_dot_sync__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x61nki/collection.proto\x12\x0f\x61nki.collection\x1a\x12\x61nki/generic.proto\x1a\x0f\x61nki/sync.proto\"b\n\x15OpenCollectionRequest\x12\x17\n\x0f\x63ollection_path\x18\x01 \x01(\t\x12\x19\n\x11media_folder_path\x18\x02 \x01(\t\x12\x15\n\rmedia_db_path\x18\x03 \x01(\t\"7\n\x16\x43loseCollectionRequest\x12\x1d\n\x15\x64owngrade_to_schema11\x18\x01 \x01(\x08\")\n\x15\x43heckDatabaseResponse\x12\x10\n\x08problems\x18\x01 \x03(\t\"\xe1\x01\n\tOpChanges\x12\x0c\n\x04\x63\x61rd\x18\x01 \x01(\x08\x12\x0c\n\x04note\x18\x02 \x01(\x08\x12\x0c\n\x04\x64\x65\x63k\x18\x03 \x01(\x08\x12\x0b\n\x03tag\x18\x04 \x01(\x08\x12\x10\n\x08notetype\x18\x05 \x01(\x08\x12\x0e\n\x06\x63onfig\x18\x06 \x01(\x08\x12\x13\n\x0b\x64\x65\x63k_config\x18\x0b \x01(\x08\x12\r\n\x05mtime\x18\x0c \x01(\x08\x12\x15\n\rbrowser_table\x18\x07 \x01(\x08\x12\x17\n\x0f\x62rowser_sidebar\x18\x08 \x01(\x08\x12\x11\n\tnote_text\x18\t \x01(\x08\x12\x14\n\x0cstudy_queues\x18\n \x01(\x08\"<\n\rOpChangesOnly\x12+\n\x07\x63hanges\x18\x01 \x01(\x0b\x32\x1a.anki.collection.OpChanges\"P\n\x12OpChangesWithCount\x12+\n\x07\x63hanges\x18\x01 \x01(\x0b\x32\x1a.anki.collection.OpChanges\x12\r\n\x05\x63ount\x18\x02 \x01(\r\"J\n\x0fOpChangesWithId\x12+\n\x07\x63hanges\x18\x01 \x01(\x0b\x32\x1a.anki.collection.OpChanges\x12\n\n\x02id\x18\x02 \x01(\x03\";\n\nUndoStatus\x12\x0c\n\x04undo\x18\x01 \x01(\t\x12\x0c\n\x04redo\x18\x02 \x01(\t\x12\x11\n\tlast_step\x18\x03 \x01(\r\"\xb5\x01\n\x12OpChangesAfterUndo\x12+\n\x07\x63hanges\x18\x01 \x01(\x0b\x32\x1a.anki.collection.OpChanges\x12\x11\n\toperation\x18\x02 \x01(\t\x12\x1d\n\x15reverted_to_timestamp\x18\x03 \x01(\x03\x12/\n\nnew_status\x18\x04 \x01(\x0b\x32\x1b.anki.collection.UndoStatus\x12\x0f\n\x07\x63ounter\x18\x05 \x01(\r\"\xed\x05\n\x08Progress\x12#\n\x04none\x18\x01 \x01(\x0b\x32\x13.anki.generic.EmptyH\x00\x12\x32\n\nmedia_sync\x18\x02 \x01(\x0b\x32\x1c.anki.sync.MediaSyncProgressH\x00\x12\x15\n\x0bmedia_check\x18\x03 \x01(\tH\x00\x12\x37\n\tfull_sync\x18\x04 \x01(\x0b\x32\".anki.collection.Progress.FullSyncH\x00\x12;\n\x0bnormal_sync\x18\x05 \x01(\x0b\x32$.anki.collection.Progress.NormalSyncH\x00\x12\x41\n\x0e\x64\x61tabase_check\x18\x06 \x01(\x0b\x32\'.anki.collection.Progress.DatabaseCheckH\x00\x12\x13\n\timporting\x18\x07 \x01(\tH\x00\x12\x13\n\texporting\x18\x08 \x01(\tH\x00\x12\x42\n\x0f\x63ompute_weights\x18\t \x01(\x0b\x32\'.anki.collection.ComputeWeightsProgressH\x00\x12\x46\n\x11\x63ompute_retention\x18\n \x01(\x0b\x32).anki.collection.ComputeRetentionProgressH\x00\x12@\n\x0e\x63ompute_memory\x18\x0b \x01(\x0b\x32&.anki.collection.ComputeMemoryProgressH\x00\x1a.\n\x08\x46ullSync\x12\x13\n\x0btransferred\x18\x01 \x01(\r\x12\r\n\x05total\x18\x02 \x01(\r\x1a;\n\nNormalSync\x12\r\n\x05stage\x18\x01 \x01(\t\x12\r\n\x05\x61\x64\x64\x65\x64\x18\x02 \x01(\t\x12\x0f\n\x07removed\x18\x03 \x01(\t\x1aJ\n\rDatabaseCheck\x12\r\n\x05stage\x18\x01 \x01(\t\x12\x13\n\x0bstage_total\x18\x02 \x01(\r\x12\x15\n\rstage_current\x18\x03 \x01(\rB\x07\n\x05value\"x\n\x16\x43omputeWeightsProgress\x12\x0f\n\x07\x63urrent\x18\x01 \x01(\r\x12\r\n\x05total\x18\x02 \x01(\r\x12\x0f\n\x07reviews\x18\x03 \x01(\r\x12\x16\n\x0e\x63urrent_preset\x18\x04 \x01(\r\x12\x15\n\rtotal_presets\x18\x05 \x01(\r\":\n\x18\x43omputeRetentionProgress\x12\x0f\n\x07\x63urrent\x18\x01 \x01(\r\x12\r\n\x05total\x18\x02 \x01(\r\"R\n\x15\x43omputeMemoryProgress\x12\x15\n\rcurrent_cards\x18\x01 \x01(\r\x12\x13\n\x0btotal_cards\x18\x02 \x01(\r\x12\r\n\x05label\x18\x03 \x01(\t\"X\n\x13\x43reateBackupRequest\x12\x15\n\rbackup_folder\x18\x01 \x01(\t\x12\r\n\x05\x66orce\x18\x02 \x01(\x08\x12\x1b\n\x13wait_for_completion\x18\x03 \x01(\x08\x32\xad\x04\n\x11\x43ollectionService\x12L\n\rCheckDatabase\x12\x13.anki.generic.Empty\x1a&.anki.collection.CheckDatabaseResponse\x12\x41\n\rGetUndoStatus\x12\x13.anki.generic.Empty\x1a\x1b.anki.collection.UndoStatus\x12@\n\x04Undo\x12\x13.anki.generic.Empty\x1a#.anki.collection.OpChangesAfterUndo\x12@\n\x04Redo\x12\x13.anki.generic.Empty\x1a#.anki.collection.OpChangesAfterUndo\x12@\n\x12\x41\x64\x64\x43ustomUndoEntry\x12\x14.anki.generic.String\x1a\x14.anki.generic.UInt32\x12\x44\n\x10MergeUndoEntries\x12\x14.anki.generic.UInt32\x1a\x1a.anki.collection.OpChanges\x12@\n\x0eLatestProgress\x12\x13.anki.generic.Empty\x1a\x19.anki.collection.Progress\x12\x39\n\rSetWantsAbort\x12\x13.anki.generic.Empty\x1a\x13.anki.generic.Empty2\xc4\x03\n\x18\x42\x61\x63kendCollectionService\x12M\n\x0eOpenCollection\x12&.anki.collection.OpenCollectionRequest\x1a\x13.anki.generic.Empty\x12O\n\x0f\x43loseCollection\x12\'.anki.collection.CloseCollectionRequest\x1a\x13.anki.generic.Empty\x12H\n\x0c\x43reateBackup\x12$.anki.collection.CreateBackupRequest\x1a\x12.anki.generic.Bool\x12\x41\n\x15\x41waitBackupCompletion\x12\x13.anki.generic.Empty\x1a\x13.anki.generic.Empty\x12@\n\x0eLatestProgress\x12\x13.anki.generic.Empty\x1a\x19.anki.collection.Progress\x12\x39\n\rSetWantsAbort\x12\x13.anki.generic.Empty\x1a\x13.anki.generic.EmptyB\x02P\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'anki.collection_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'P\001'
  _OPENCOLLECTIONREQUEST._serialized_start=79
  _OPENCOLLECTIONREQUEST._serialized_end=177
  _CLOSECOLLECTIONREQUEST._serialized_start=179
  _CLOSECOLLECTIONREQUEST._serialized_end=234
  _CHECKDATABASERESPONSE._serialized_start=236
  _CHECKDATABASERESPONSE._serialized_end=277
  _OPCHANGES._serialized_start=280
  _OPCHANGES._serialized_end=505
  _OPCHANGESONLY._serialized_start=507
  _OPCHANGESONLY._serialized_end=567
  _OPCHANGESWITHCOUNT._serialized_start=569
  _OPCHANGESWITHCOUNT._serialized_end=649
  _OPCHANGESWITHID._serialized_start=651
  _OPCHANGESWITHID._serialized_end=725
  _UNDOSTATUS._serialized_start=727
  _UNDOSTATUS._serialized_end=786
  _OPCHANGESAFTERUNDO._serialized_start=789
  _OPCHANGESAFTERUNDO._serialized_end=970
  _PROGRESS._serialized_start=973
  _PROGRESS._serialized_end=1722
  _PROGRESS_FULLSYNC._serialized_start=1530
  _PROGRESS_FULLSYNC._serialized_end=1576
  _PROGRESS_NORMALSYNC._serialized_start=1578
  _PROGRESS_NORMALSYNC._serialized_end=1637
  _PROGRESS_DATABASECHECK._serialized_start=1639
  _PROGRESS_DATABASECHECK._serialized_end=1713
  _COMPUTEWEIGHTSPROGRESS._serialized_start=1724
  _COMPUTEWEIGHTSPROGRESS._serialized_end=1844
  _COMPUTERETENTIONPROGRESS._serialized_start=1846
  _COMPUTERETENTIONPROGRESS._serialized_end=1904
  _COMPUTEMEMORYPROGRESS._serialized_start=1906
  _COMPUTEMEMORYPROGRESS._serialized_end=1988
  _CREATEBACKUPREQUEST._serialized_start=1990
  _CREATEBACKUPREQUEST._serialized_end=2078
  _COLLECTIONSERVICE._serialized_start=2081
  _COLLECTIONSERVICE._serialized_end=2638
  _BACKENDCOLLECTIONSERVICE._serialized_start=2641
  _BACKENDCOLLECTIONSERVICE._serialized_end=3093
# @@protoc_insertion_point(module_scope)
