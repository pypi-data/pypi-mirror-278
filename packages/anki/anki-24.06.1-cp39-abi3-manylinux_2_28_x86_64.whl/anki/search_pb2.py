# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: anki/search.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from anki import generic_pb2 as anki_dot_generic__pb2
from anki import collection_pb2 as anki_dot_collection__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x61nki/search.proto\x12\x0b\x61nki.search\x1a\x12\x61nki/generic.proto\x1a\x15\x61nki/collection.proto\"\xa0\x0b\n\nSearchNode\x12.\n\x05group\x18\x01 \x01(\x0b\x32\x1d.anki.search.SearchNode.GroupH\x00\x12*\n\x07negated\x18\x02 \x01(\x0b\x32\x17.anki.search.SearchNodeH\x00\x12\x17\n\rparsable_text\x18\x03 \x01(\tH\x00\x12\x12\n\x08template\x18\x04 \x01(\rH\x00\x12\r\n\x03nid\x18\x05 \x01(\x03H\x00\x12,\n\x04\x64upe\x18\x06 \x01(\x0b\x32\x1c.anki.search.SearchNode.DupeH\x00\x12\x14\n\nfield_name\x18\x07 \x01(\tH\x00\x12.\n\x05rated\x18\x08 \x01(\x0b\x32\x1d.anki.search.SearchNode.RatedH\x00\x12\x17\n\radded_in_days\x18\t \x01(\rH\x00\x12\x15\n\x0b\x64ue_in_days\x18\n \x01(\x05H\x00\x12,\n\x04\x66lag\x18\x0b \x01(\x0e\x32\x1c.anki.search.SearchNode.FlagH\x00\x12\x37\n\ncard_state\x18\x0c \x01(\x0e\x32!.anki.search.SearchNode.CardStateH\x00\x12.\n\x04nids\x18\r \x01(\x0b\x32\x1e.anki.search.SearchNode.IdListH\x00\x12\x18\n\x0e\x65\x64ited_in_days\x18\x0e \x01(\rH\x00\x12\x0e\n\x04\x64\x65\x63k\x18\x0f \x01(\tH\x00\x12\x14\n\ndue_on_day\x18\x10 \x01(\x05H\x00\x12\r\n\x03tag\x18\x11 \x01(\tH\x00\x12\x0e\n\x04note\x18\x12 \x01(\tH\x00\x12\x1c\n\x12introduced_in_days\x18\x13 \x01(\rH\x00\x12.\n\x05\x66ield\x18\x14 \x01(\x0b\x32\x1d.anki.search.SearchNode.FieldH\x00\x12\x16\n\x0cliteral_text\x18\x15 \x01(\tH\x00\x1a\x30\n\x04\x44upe\x12\x13\n\x0bnotetype_id\x18\x01 \x01(\x03\x12\x13\n\x0b\x66irst_field\x18\x02 \x01(\t\x1a\x45\n\x05Rated\x12\x0c\n\x04\x64\x61ys\x18\x01 \x01(\r\x12.\n\x06rating\x18\x02 \x01(\x0e\x32\x1e.anki.search.SearchNode.Rating\x1a\x15\n\x06IdList\x12\x0b\n\x03ids\x18\x01 \x03(\x03\x1a\x80\x01\n\x05Group\x12&\n\x05nodes\x18\x01 \x03(\x0b\x32\x17.anki.search.SearchNode\x12\x34\n\x06joiner\x18\x02 \x01(\x0e\x32$.anki.search.SearchNode.Group.Joiner\"\x19\n\x06Joiner\x12\x07\n\x03\x41ND\x10\x00\x12\x06\n\x02OR\x10\x01\x1a\x38\n\x05\x46ield\x12\x12\n\nfield_name\x18\x01 \x01(\t\x12\x0c\n\x04text\x18\x02 \x01(\t\x12\r\n\x05is_re\x18\x03 \x01(\x08\"\x95\x01\n\x04\x46lag\x12\r\n\tFLAG_NONE\x10\x00\x12\x0c\n\x08\x46LAG_ANY\x10\x01\x12\x0c\n\x08\x46LAG_RED\x10\x02\x12\x0f\n\x0b\x46LAG_ORANGE\x10\x03\x12\x0e\n\nFLAG_GREEN\x10\x04\x12\r\n\tFLAG_BLUE\x10\x05\x12\r\n\tFLAG_PINK\x10\x06\x12\x12\n\x0e\x46LAG_TURQUOISE\x10\x07\x12\x0f\n\x0b\x46LAG_PURPLE\x10\x08\"w\n\x06Rating\x12\x0e\n\nRATING_ANY\x10\x00\x12\x10\n\x0cRATING_AGAIN\x10\x01\x12\x0f\n\x0bRATING_HARD\x10\x02\x12\x0f\n\x0bRATING_GOOD\x10\x03\x12\x0f\n\x0bRATING_EASY\x10\x04\x12\x18\n\x14RATING_BY_RESCHEDULE\x10\x05\"\x91\x01\n\tCardState\x12\x12\n\x0e\x43\x41RD_STATE_NEW\x10\x00\x12\x14\n\x10\x43\x41RD_STATE_LEARN\x10\x01\x12\x15\n\x11\x43\x41RD_STATE_REVIEW\x10\x02\x12\x12\n\x0e\x43\x41RD_STATE_DUE\x10\x03\x12\x18\n\x14\x43\x41RD_STATE_SUSPENDED\x10\x04\x12\x15\n\x11\x43\x41RD_STATE_BURIED\x10\x05\x42\x08\n\x06\x66ilter\"F\n\rSearchRequest\x12\x0e\n\x06search\x18\x01 \x01(\t\x12%\n\x05order\x18\x02 \x01(\x0b\x32\x16.anki.search.SortOrder\"\x1d\n\x0eSearchResponse\x12\x0b\n\x03ids\x18\x01 \x03(\x03\"\xaa\x01\n\tSortOrder\x12#\n\x04none\x18\x01 \x01(\x0b\x32\x13.anki.generic.EmptyH\x00\x12\x10\n\x06\x63ustom\x18\x02 \x01(\tH\x00\x12\x31\n\x07\x62uiltin\x18\x03 \x01(\x0b\x32\x1e.anki.search.SortOrder.BuiltinH\x00\x1a*\n\x07\x42uiltin\x12\x0e\n\x06\x63olumn\x18\x01 \x01(\t\x12\x0f\n\x07reverse\x18\x02 \x01(\x08\x42\x07\n\x05value\"\xb0\x01\n\x16JoinSearchNodesRequest\x12\x34\n\x06joiner\x18\x01 \x01(\x0e\x32$.anki.search.SearchNode.Group.Joiner\x12.\n\rexisting_node\x18\x02 \x01(\x0b\x32\x17.anki.search.SearchNode\x12\x30\n\x0f\x61\x64\x64itional_node\x18\x03 \x01(\x0b\x32\x17.anki.search.SearchNode\"}\n\x18ReplaceSearchNodeRequest\x12.\n\rexisting_node\x18\x01 \x01(\x0b\x32\x17.anki.search.SearchNode\x12\x31\n\x10replacement_node\x18\x02 \x01(\x0b\x32\x17.anki.search.SearchNode\"\x81\x01\n\x15\x46indAndReplaceRequest\x12\x0c\n\x04nids\x18\x01 \x03(\x03\x12\x0e\n\x06search\x18\x02 \x01(\t\x12\x13\n\x0breplacement\x18\x03 \x01(\t\x12\r\n\x05regex\x18\x04 \x01(\x08\x12\x12\n\nmatch_case\x18\x05 \x01(\x08\x12\x12\n\nfield_name\x18\x06 \x01(\t\"\x97\x04\n\x0e\x42rowserColumns\x12\x33\n\x07\x63olumns\x18\x01 \x03(\x0b\x32\".anki.search.BrowserColumns.Column\x1a\xcb\x02\n\x06\x43olumn\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x18\n\x10\x63\x61rds_mode_label\x18\x02 \x01(\t\x12\x18\n\x10notes_mode_label\x18\x03 \x01(\t\x12:\n\rsorting_cards\x18\x04 \x01(\x0e\x32#.anki.search.BrowserColumns.Sorting\x12:\n\rsorting_notes\x18\t \x01(\x0e\x32#.anki.search.BrowserColumns.Sorting\x12\x16\n\x0euses_cell_font\x18\x05 \x01(\x08\x12\x38\n\talignment\x18\x06 \x01(\x0e\x32%.anki.search.BrowserColumns.Alignment\x12\x1a\n\x12\x63\x61rds_mode_tooltip\x18\x07 \x01(\t\x12\x1a\n\x12notes_mode_tooltip\x18\x08 \x01(\t\"J\n\x07Sorting\x12\x10\n\x0cSORTING_NONE\x10\x00\x12\x15\n\x11SORTING_ASCENDING\x10\x01\x12\x16\n\x12SORTING_DESCENDING\x10\x02\"6\n\tAlignment\x12\x13\n\x0f\x41LIGNMENT_START\x10\x00\x12\x14\n\x10\x41LIGNMENT_CENTER\x10\x01\"\xa5\x03\n\nBrowserRow\x12+\n\x05\x63\x65lls\x18\x01 \x03(\x0b\x32\x1c.anki.search.BrowserRow.Cell\x12,\n\x05\x63olor\x18\x02 \x01(\x0e\x32\x1d.anki.search.BrowserRow.Color\x12\x11\n\tfont_name\x18\x03 \x01(\t\x12\x11\n\tfont_size\x18\x04 \x01(\r\x1a$\n\x04\x43\x65ll\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x0e\n\x06is_rtl\x18\x02 \x01(\x08\"\xef\x01\n\x05\x43olor\x12\x11\n\rCOLOR_DEFAULT\x10\x00\x12\x10\n\x0c\x43OLOR_MARKED\x10\x01\x12\x13\n\x0f\x43OLOR_SUSPENDED\x10\x02\x12\x12\n\x0e\x43OLOR_FLAG_RED\x10\x03\x12\x15\n\x11\x43OLOR_FLAG_ORANGE\x10\x04\x12\x14\n\x10\x43OLOR_FLAG_GREEN\x10\x05\x12\x13\n\x0f\x43OLOR_FLAG_BLUE\x10\x06\x12\x13\n\x0f\x43OLOR_FLAG_PINK\x10\x07\x12\x18\n\x14\x43OLOR_FLAG_TURQUOISE\x10\x08\x12\x15\n\x11\x43OLOR_FLAG_PURPLE\x10\t\x12\x10\n\x0c\x43OLOR_BURIED\x10\n2\xb0\x05\n\rSearchService\x12\x42\n\x11\x42uildSearchString\x12\x17.anki.search.SearchNode\x1a\x14.anki.generic.String\x12\x46\n\x0bSearchCards\x12\x1a.anki.search.SearchRequest\x1a\x1b.anki.search.SearchResponse\x12\x46\n\x0bSearchNotes\x12\x1a.anki.search.SearchRequest\x1a\x1b.anki.search.SearchResponse\x12L\n\x0fJoinSearchNodes\x12#.anki.search.JoinSearchNodesRequest\x1a\x14.anki.generic.String\x12P\n\x11ReplaceSearchNode\x12%.anki.search.ReplaceSearchNodeRequest\x1a\x14.anki.generic.String\x12Y\n\x0e\x46indAndReplace\x12\".anki.search.FindAndReplaceRequest\x1a#.anki.collection.OpChangesWithCount\x12\x45\n\x11\x41llBrowserColumns\x12\x13.anki.generic.Empty\x1a\x1b.anki.search.BrowserColumns\x12?\n\x0f\x42rowserRowForId\x12\x13.anki.generic.Int64\x1a\x17.anki.search.BrowserRow\x12H\n\x17SetActiveBrowserColumns\x12\x18.anki.generic.StringList\x1a\x13.anki.generic.Empty2\x16\n\x14\x42\x61\x63kendSearchServiceB\x02P\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'anki.search_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'P\001'
  _SEARCHNODE._serialized_start=78
  _SEARCHNODE._serialized_end=1518
  _SEARCHNODE_DUPE._serialized_start=756
  _SEARCHNODE_DUPE._serialized_end=804
  _SEARCHNODE_RATED._serialized_start=806
  _SEARCHNODE_RATED._serialized_end=875
  _SEARCHNODE_IDLIST._serialized_start=877
  _SEARCHNODE_IDLIST._serialized_end=898
  _SEARCHNODE_GROUP._serialized_start=901
  _SEARCHNODE_GROUP._serialized_end=1029
  _SEARCHNODE_GROUP_JOINER._serialized_start=1004
  _SEARCHNODE_GROUP_JOINER._serialized_end=1029
  _SEARCHNODE_FIELD._serialized_start=1031
  _SEARCHNODE_FIELD._serialized_end=1087
  _SEARCHNODE_FLAG._serialized_start=1090
  _SEARCHNODE_FLAG._serialized_end=1239
  _SEARCHNODE_RATING._serialized_start=1241
  _SEARCHNODE_RATING._serialized_end=1360
  _SEARCHNODE_CARDSTATE._serialized_start=1363
  _SEARCHNODE_CARDSTATE._serialized_end=1508
  _SEARCHREQUEST._serialized_start=1520
  _SEARCHREQUEST._serialized_end=1590
  _SEARCHRESPONSE._serialized_start=1592
  _SEARCHRESPONSE._serialized_end=1621
  _SORTORDER._serialized_start=1624
  _SORTORDER._serialized_end=1794
  _SORTORDER_BUILTIN._serialized_start=1743
  _SORTORDER_BUILTIN._serialized_end=1785
  _JOINSEARCHNODESREQUEST._serialized_start=1797
  _JOINSEARCHNODESREQUEST._serialized_end=1973
  _REPLACESEARCHNODEREQUEST._serialized_start=1975
  _REPLACESEARCHNODEREQUEST._serialized_end=2100
  _FINDANDREPLACEREQUEST._serialized_start=2103
  _FINDANDREPLACEREQUEST._serialized_end=2232
  _BROWSERCOLUMNS._serialized_start=2235
  _BROWSERCOLUMNS._serialized_end=2770
  _BROWSERCOLUMNS_COLUMN._serialized_start=2307
  _BROWSERCOLUMNS_COLUMN._serialized_end=2638
  _BROWSERCOLUMNS_SORTING._serialized_start=2640
  _BROWSERCOLUMNS_SORTING._serialized_end=2714
  _BROWSERCOLUMNS_ALIGNMENT._serialized_start=2716
  _BROWSERCOLUMNS_ALIGNMENT._serialized_end=2770
  _BROWSERROW._serialized_start=2773
  _BROWSERROW._serialized_end=3194
  _BROWSERROW_CELL._serialized_start=2916
  _BROWSERROW_CELL._serialized_end=2952
  _BROWSERROW_COLOR._serialized_start=2955
  _BROWSERROW_COLOR._serialized_end=3194
  _SEARCHSERVICE._serialized_start=3197
  _SEARCHSERVICE._serialized_end=3885
  _BACKENDSEARCHSERVICE._serialized_start=3887
  _BACKENDSEARCHSERVICE._serialized_end=3909
# @@protoc_insertion_point(module_scope)
