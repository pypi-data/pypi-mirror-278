# coding=utf-8
# Copyright 2024 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: skip-file

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dataset_info.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorflow_datasets.core.proto import feature_generated_pb2 as feature__pb2
from tensorflow_metadata.proto.v0 import schema_pb2 as tensorflow__metadata_dot_proto_dot_v0_dot_schema__pb2
from tensorflow_metadata.proto.v0 import statistics_pb2 as tensorflow__metadata_dot_proto_dot_v0_dot_statistics__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x12\x64\x61taset_info.proto\x12\x13tensorflow_datasets\x1a\rfeature.proto\x1a)tensorflow_metadata/proto/v0/schema.proto\x1a-tensorflow_metadata/proto/v0/statistics.proto"\x1f\n\x0f\x44\x61tasetLocation\x12\x0c\n\x04urls\x18\x01'
    b' \x03(\t"\xb8\x01\n\tSplitInfo\x12\x0c\n\x04name\x18\x01'
    b' \x01(\t\x12\x12\n\nnum_shards\x18\x02'
    b' \x01(\x03\x12\x15\n\rshard_lengths\x18\x04'
    b' \x03(\x03\x12\x11\n\tnum_bytes\x18\x05'
    b' \x01(\x03\x12\x44\n\nstatistics\x18\x03'
    b' \x01(\x0b\x32\x30.tensorflow.metadata.v0.DatasetFeatureStatistics\x12\x19\n\x11\x66ilepath_template\x18\x06'
    b' \x01(\t"\xf3\x03\n\x0eSupervisedKeys\x12\x11\n\x05input\x18\x01'
    b' \x01(\tB\x02\x18\x01\x12\x12\n\x06output\x18\x02'
    b' \x01(\tB\x02\x18\x01\x12\x38\n\x05tuple\x18\x03'
    b' \x01(\x0b\x32).tensorflow_datasets.SupervisedKeys.Tuple\x1a@\n\x05Tuple\x12\x37\n\x05items\x18\x01'
    b' \x03(\x0b\x32(.tensorflow_datasets.SupervisedKeys.Nest\x1a\x9f\x01\n\x04\x44ict\x12@\n\x04\x64ict\x18\x01'
    b' \x03(\x0b\x32\x32.tensorflow_datasets.SupervisedKeys.Dict.DictEntry\x1aU\n\tDictEntry\x12\x0b\n\x03key\x18\x01'
    b' \x01(\t\x12\x37\n\x05value\x18\x02'
    b' \x01(\x0b\x32(.tensorflow_datasets.SupervisedKeys.Nest:\x02\x38\x01\x1a\x9b\x01\n\x04Nest\x12\x15\n\x0b\x66\x65\x61ture_key\x18\x01'
    b' \x01(\tH\x00\x12:\n\x05tuple\x18\x02'
    b' \x01(\x0b\x32).tensorflow_datasets.SupervisedKeys.TupleH\x00\x12\x38\n\x04\x64ict\x18\x03'
    b' \x01(\x0b\x32(.tensorflow_datasets.SupervisedKeys.DictH\x00\x42\x06\n\x04nest"%\n\x12RedistributionInfo\x12\x0f\n\x07license\x18\x01'
    b' \x01(\t"\x8f\x02\n\x10\x44\x61taSourceAccess\x12\x1b\n\x13\x61\x63\x63\x65ss_timestamp_ms\x18\x01'
    b' \x01(\x03\x12\x36\n\x0b\x66ile_system\x18\x02'
    b' \x01(\x0b\x32\x1f.tensorflow_datasets.FileSystemH\x00\x12\x32\n\tsql_query\x18\x03'
    b' \x01(\x0b\x32\x1d.tensorflow_datasets.SqlQueryH\x00\x12\x41\n\x0ctfds_dataset\x18\x04'
    b' \x01(\x0b\x32).tensorflow_datasets.TfdsDatasetReferenceH\x00\x12%\n\x03url\x18\x05'
    b' \x01(\x0b\x32\x18.tensorflow_datasets.UrlB\x08\n\x06source"\x1a\n\nFileSystem\x12\x0c\n\x04path\x18\x01'
    b' \x01(\t"$\n\x03Url\x12\x0b\n\x03url\x18\x01'
    b' \x01(\t\x12\x10\n\x08\x63hecksum\x18\x02'
    b' \x01(\t"\x1d\n\x08SqlQuery\x12\x11\n\tsql_query\x18\x01'
    b' \x01(\t"m\n\x14TfdsDatasetReference\x12\x0c\n\x04name\x18\x01'
    b' \x01(\t\x12\x0e\n\x06\x63onfig\x18\x02'
    b' \x01(\t\x12\x0f\n\x07version\x18\x03'
    b' \x01(\t\x12\x10\n\x08\x64\x61ta_dir\x18\x04'
    b' \x01(\t\x12\x14\n\x0c\x64s_namespace\x18\x05'
    b' \x01(\t"\xb4\x07\n\x0b\x44\x61tasetInfo\x12\x0c\n\x04name\x18\x01'
    b' \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02'
    b' \x01(\t\x12\x0f\n\x07version\x18\t \x01(\t\x12I\n\rrelease_notes\x18\x12'
    b' \x03(\x0b\x32\x32.tensorflow_datasets.DatasetInfo.ReleaseNotesEntry\x12\x13\n\x0b\x63onfig_name\x18\r'
    b' \x01(\t\x12\x1a\n\x12\x63onfig_description\x18\x0e'
    b' \x01(\t\x12\x13\n\x0b\x63onfig_tags\x18\x15'
    b' \x03(\t\x12.\n\x08\x66\x65\x61tures\x18\x13'
    b' \x01(\x0b\x32\x1c.tensorflow_datasets.Feature\x12\x10\n\x08\x63itation\x18\x03'
    b' \x01(\t\x12\x19\n\rsize_in_bytes\x18\x04'
    b' \x01(\x03\x42\x02\x18\x01\x12\x15\n\rdownload_size\x18\x0c'
    b' \x01(\x03\x12\x36\n\x08location\x18\x05'
    b' \x01(\x0b\x32$.tensorflow_datasets.DatasetLocation\x12W\n\x12\x64ownload_checksums\x18\n'
    b' \x03(\x0b\x32\x37.tensorflow_datasets.DatasetInfo.DownloadChecksumsEntryB\x02\x18\x01\x12.\n\x06schema\x18\x06'
    b' \x01(\x0b\x32\x1e.tensorflow.metadata.v0.Schema\x12.\n\x06splits\x18\x07'
    b' \x03(\x0b\x32\x1e.tensorflow_datasets.SplitInfo\x12<\n\x0fsupervised_keys\x18\x08'
    b' \x01(\x0b\x32#.tensorflow_datasets.SupervisedKeys\x12\x44\n\x13redistribution_info\x18\x0b'
    b" \x01(\x0b\x32'.tensorflow_datasets.RedistributionInfo\x12\x13\n\x0bmodule_name\x18\x0f"
    b' \x01(\t\x12\x19\n\x11\x64isable_shuffling\x18\x10'
    b' \x01(\x08\x12\x13\n\x0b\x66ile_format\x18\x11'
    b' \x01(\t\x12\x43\n\x14\x64\x61ta_source_accesses\x18\x14'
    b' \x03(\x0b\x32%.tensorflow_datasets.DataSourceAccess\x1a\x33\n\x11ReleaseNotesEntry\x12\x0b\n\x03key\x18\x01'
    b' \x01(\t\x12\r\n\x05value\x18\x02'
    b' \x01(\t:\x02\x38\x01\x1a\x38\n\x16\x44ownloadChecksumsEntry\x12\x0b\n\x03key\x18\x01'
    b' \x01(\t\x12\r\n\x05value\x18\x02'
    b' \x01(\t:\x02\x38\x01\x42\x03\xf8\x01\x01\x62\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, 'dataset_info_pb2', globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\370\001\001'
  _SUPERVISEDKEYS_DICT_DICTENTRY._options = None
  _SUPERVISEDKEYS_DICT_DICTENTRY._serialized_options = b'8\001'
  _SUPERVISEDKEYS.fields_by_name['input']._options = None
  _SUPERVISEDKEYS.fields_by_name['input']._serialized_options = b'\030\001'
  _SUPERVISEDKEYS.fields_by_name['output']._options = None
  _SUPERVISEDKEYS.fields_by_name['output']._serialized_options = b'\030\001'
  _DATASETINFO_RELEASENOTESENTRY._options = None
  _DATASETINFO_RELEASENOTESENTRY._serialized_options = b'8\001'
  _DATASETINFO_DOWNLOADCHECKSUMSENTRY._options = None
  _DATASETINFO_DOWNLOADCHECKSUMSENTRY._serialized_options = b'8\001'
  _DATASETINFO.fields_by_name['size_in_bytes']._options = None
  _DATASETINFO.fields_by_name['size_in_bytes']._serialized_options = b'\030\001'
  _DATASETINFO.fields_by_name['download_checksums']._options = None
  _DATASETINFO.fields_by_name['download_checksums']._serialized_options = (
      b'\030\001'
  )
  _DATASETLOCATION._serialized_start = 148
  _DATASETLOCATION._serialized_end = 179
  _SPLITINFO._serialized_start = 182
  _SPLITINFO._serialized_end = 366
  _SUPERVISEDKEYS._serialized_start = 369
  _SUPERVISEDKEYS._serialized_end = 868
  _SUPERVISEDKEYS_TUPLE._serialized_start = 484
  _SUPERVISEDKEYS_TUPLE._serialized_end = 548
  _SUPERVISEDKEYS_DICT._serialized_start = 551
  _SUPERVISEDKEYS_DICT._serialized_end = 710
  _SUPERVISEDKEYS_DICT_DICTENTRY._serialized_start = 625
  _SUPERVISEDKEYS_DICT_DICTENTRY._serialized_end = 710
  _SUPERVISEDKEYS_NEST._serialized_start = 713
  _SUPERVISEDKEYS_NEST._serialized_end = 868
  _REDISTRIBUTIONINFO._serialized_start = 870
  _REDISTRIBUTIONINFO._serialized_end = 907
  _DATASOURCEACCESS._serialized_start = 910
  _DATASOURCEACCESS._serialized_end = 1181
  _FILESYSTEM._serialized_start = 1183
  _FILESYSTEM._serialized_end = 1209
  _URL._serialized_start = 1211
  _URL._serialized_end = 1247
  _SQLQUERY._serialized_start = 1249
  _SQLQUERY._serialized_end = 1278
  _TFDSDATASETREFERENCE._serialized_start = 1280
  _TFDSDATASETREFERENCE._serialized_end = 1389
  _DATASETINFO._serialized_start = 1392
  _DATASETINFO._serialized_end = 2340
  _DATASETINFO_RELEASENOTESENTRY._serialized_start = 2231
  _DATASETINFO_RELEASENOTESENTRY._serialized_end = 2282
  _DATASETINFO_DOWNLOADCHECKSUMSENTRY._serialized_start = 2284
  _DATASETINFO_DOWNLOADCHECKSUMSENTRY._serialized_end = 2340
# @@protoc_insertion_point(module_scope)
