#
# Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# This software product is a proprietary product of Nvidia Corporation and its affiliates
# (the "Company") and all right, title, and interest in and to the software
# product, including all associated intellectual property rights, are and
# shall remain exclusively with the Company.
#
# This software product is governed by the End User License Agreement
# provided with the software product.
#
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()
from . import model_config_pb2 as model__config__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x12grpc_service.proto\x12\tinference\x1a\x12model_config.proto"\x13\n\x11ServerLiveRequest""\n\x12ServerLiveResponse\x12\x0c\n\x04live\x18\x01'
    b' \x01(\x08"\x14\n\x12ServerReadyRequest"$\n\x13ServerReadyResponse\x12\r\n\x05ready\x18\x01'
    b' \x01(\x08"2\n\x11ModelReadyRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02'
    b' \x01(\t"#\n\x12ModelReadyResponse\x12\r\n\x05ready\x18\x01'
    b' \x01(\x08"\x17\n\x15ServerMetadataRequest"K\n\x16ServerMetadataResponse\x12\x0c\n\x04name\x18\x01'
    b" \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x12\n\nextensions\x18\x03"
    b' \x03(\t"5\n\x14ModelMetadataRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02'
    b' \x01(\t"\x8d\x02\n\x15ModelMetadataResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08versions\x18\x02'
    b" \x03(\t\x12\x10\n\x08platform\x18\x03 \x01(\t\x12?\n\x06inputs\x18\x04"
    b" \x03(\x0b2/.inference.ModelMetadataResponse.TensorMetadata\x12@\n\x07outputs\x18\x05"
    b" \x03(\x0b2/.inference.ModelMetadataResponse.TensorMetadata\x1a?\n\x0eTensorMetadata\x12\x0c\n\x04name\x18\x01"
    b" \x01(\t\x12\x10\n\x08datatype\x18\x02 \x01(\t\x12\r\n\x05shape\x18\x03"
    b' \x03(\x03"\x99\x01\n\x0eInferParameter\x12\x14\n\nbool_param\x18\x01'
    b" \x01(\x08H\x00\x12\x15\n\x0bint64_param\x18\x02 \x01(\x03H\x00\x12\x16\n\x0cstring_param\x18\x03"
    b" \x01(\tH\x00\x12\x16\n\x0cdouble_param\x18\x04 \x01(\x01H\x00\x12\x16\n\x0cuint64_param\x18\x05"
    b' \x01(\x04H\x00B\x12\n\x10parameter_choice"\xd0\x01\n\x13InferTensorContents\x12\x15\n\rbool_contents\x18\x01'
    b" \x03(\x08\x12\x14\n\x0cint_contents\x18\x02 \x03(\x05\x12\x16\n\x0eint64_contents\x18\x03"
    b" \x03(\x03\x12\x15\n\ruint_contents\x18\x04 \x03(\r\x12\x17\n\x0fuint64_contents\x18\x05"
    b" \x03(\x04\x12\x15\n\rfp32_contents\x18\x06 \x03(\x02\x12\x15\n\rfp64_contents\x18\x07"
    b" \x03(\x01\x12\x16\n\x0ebytes_contents\x18\x08"
    b' \x03(\x0c"\xee\x06\n\x11ModelInferRequest\x12\x12\n\nmodel_name\x18\x01 \x01(\t\x12\x15\n\rmodel_version\x18\x02'
    b" \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12@\n\nparameters\x18\x04"
    b" \x03(\x0b2,.inference.ModelInferRequest.ParametersEntry\x12=\n\x06inputs\x18\x05"
    b" \x03(\x0b2-.inference.ModelInferRequest.InferInputTensor\x12H\n\x07outputs\x18\x06"
    b" \x03(\x0b27.inference.ModelInferRequest.InferRequestedOutputTensor\x12\x1a\n\x12raw_input_contents\x18\x07"
    b" \x03(\x0c\x1a\x94\x02\n\x10InferInputTensor\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08datatype\x18\x02"
    b" \x01(\t\x12\r\n\x05shape\x18\x03 \x03(\x03\x12Q\n\nparameters\x18\x04"
    b" \x03(\x0b2=.inference.ModelInferRequest.InferInputTensor.ParametersEntry\x120\n\x08contents\x18\x05"
    b" \x01(\x0b2\x1e.inference.InferTensorContents\x1aL\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12(\n\x05value\x18\x02"
    b" \x01(\x0b2\x19.inference.InferParameter:\x028\x01\x1a\xd5\x01\n\x1aInferRequestedOutputTensor\x12\x0c\n\x04name\x18\x01"
    b" \x01(\t\x12[\n\nparameters\x18\x02"
    b" \x03(\x0b2G.inference.ModelInferRequest.InferRequestedOutputTensor.ParametersEntry\x1aL\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12(\n\x05value\x18\x02"
    b" \x01(\x0b2\x19.inference.InferParameter:\x028\x01\x1aL\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12(\n\x05value\x18\x02"
    b' \x01(\x0b2\x19.inference.InferParameter:\x028\x01"\xd5\x04\n\x12ModelInferResponse\x12\x12\n\nmodel_name\x18\x01'
    b" \x01(\t\x12\x15\n\rmodel_version\x18\x02 \x01(\t\x12\n\n\x02id\x18\x03 \x01(\t\x12A\n\nparameters\x18\x04"
    b" \x03(\x0b2-.inference.ModelInferResponse.ParametersEntry\x12@\n\x07outputs\x18\x05"
    b" \x03(\x0b2/.inference.ModelInferResponse.InferOutputTensor\x12\x1b\n\x13raw_output_contents\x18\x06"
    b" \x03(\x0c\x1a\x97\x02\n\x11InferOutputTensor\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08datatype\x18\x02"
    b" \x01(\t\x12\r\n\x05shape\x18\x03 \x03(\x03\x12S\n\nparameters\x18\x04"
    b" \x03(\x0b2?.inference.ModelInferResponse.InferOutputTensor.ParametersEntry\x120\n\x08contents\x18\x05"
    b" \x01(\x0b2\x1e.inference.InferTensorContents\x1aL\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12(\n\x05value\x18\x02"
    b" \x01(\x0b2\x19.inference.InferParameter:\x028\x01\x1aL\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12(\n\x05value\x18\x02"
    b' \x01(\x0b2\x19.inference.InferParameter:\x028\x01"h\n\x18ModelStreamInferResponse\x12\x15\n\rerror_message\x18\x01'
    b" \x01(\t\x125\n\x0einfer_response\x18\x02"
    b' \x01(\x0b2\x1d.inference.ModelInferResponse"3\n\x12ModelConfigRequest\x12\x0c\n\x04name\x18\x01'
    b' \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t"=\n\x13ModelConfigResponse\x12&\n\x06config\x18\x01'
    b' \x01(\x0b2\x16.inference.ModelConfig"7\n\x16ModelStatisticsRequest\x12\x0c\n\x04name\x18\x01'
    b' \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t".\n\x11StatisticDuration\x12\r\n\x05count\x18\x01'
    b' \x01(\x04\x12\n\n\x02ns\x18\x02 \x01(\x04"\x9c\x03\n\x0fInferStatistics\x12-\n\x07success\x18\x01'
    b" \x01(\x0b2\x1c.inference.StatisticDuration\x12*\n\x04fail\x18\x02"
    b" \x01(\x0b2\x1c.inference.StatisticDuration\x12+\n\x05queue\x18\x03"
    b" \x01(\x0b2\x1c.inference.StatisticDuration\x123\n\rcompute_input\x18\x04"
    b" \x01(\x0b2\x1c.inference.StatisticDuration\x123\n\rcompute_infer\x18\x05"
    b" \x01(\x0b2\x1c.inference.StatisticDuration\x124\n\x0ecompute_output\x18\x06"
    b" \x01(\x0b2\x1c.inference.StatisticDuration\x12/\n\tcache_hit\x18\x07"
    b" \x01(\x0b2\x1c.inference.StatisticDuration\x120\n\ncache_miss\x18\x08"
    b' \x01(\x0b2\x1c.inference.StatisticDuration"\xca\x01\n\x14InferBatchStatistics\x12\x12\n\nbatch_size\x18\x01'
    b" \x01(\x04\x123\n\rcompute_input\x18\x02 \x01(\x0b2\x1c.inference.StatisticDuration\x123\n\rcompute_infer\x18\x03"
    b" \x01(\x0b2\x1c.inference.StatisticDuration\x124\n\x0ecompute_output\x18\x04"
    b' \x01(\x0b2\x1c.inference.StatisticDuration":\n\x0bMemoryUsage\x12\x0c\n\x04type\x18\x01'
    b" \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x03\x12\x11\n\tbyte_size\x18\x03"
    b' \x01(\x04"\x93\x02\n\x0fModelStatistics\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02'
    b" \x01(\t\x12\x16\n\x0elast_inference\x18\x03 \x01(\x04\x12\x17\n\x0finference_count\x18\x04"
    b" \x01(\x04\x12\x17\n\x0fexecution_count\x18\x05 \x01(\x04\x123\n\x0finference_stats\x18\x06"
    b" \x01(\x0b2\x1a.inference.InferStatistics\x124\n\x0bbatch_stats\x18\x07"
    b" \x03(\x0b2\x1f.inference.InferBatchStatistics\x12,\n\x0cmemory_usage\x18\x08"
    b' \x03(\x0b2\x16.inference.MemoryUsage"J\n\x17ModelStatisticsResponse\x12/\n\x0bmodel_stats\x18\x01'
    b' \x03(\x0b2\x1a.inference.ModelStatistics"\x8a\x01\n\x18ModelRepositoryParameter\x12\x14\n\nbool_param\x18\x01'
    b" \x01(\x08H\x00\x12\x15\n\x0bint64_param\x18\x02 \x01(\x03H\x00\x12\x16\n\x0cstring_param\x18\x03"
    b" \x01(\tH\x00\x12\x15\n\x0bbytes_param\x18\x04"
    b' \x01(\x0cH\x00B\x12\n\x10parameter_choice"@\n\x16RepositoryIndexRequest\x12\x17\n\x0frepository_name\x18\x01'
    b' \x01(\t\x12\r\n\x05ready\x18\x02 \x01(\x08"\xa4\x01\n\x17RepositoryIndexResponse\x12=\n\x06models\x18\x01'
    b" \x03(\x0b2-.inference.RepositoryIndexResponse.ModelIndex\x1aJ\n\nModelIndex\x12\x0c\n\x04name\x18\x01"
    b" \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12\x0e\n\x06reason\x18\x04"
    b' \x01(\t"\xec\x01\n\x1aRepositoryModelLoadRequest\x12\x17\n\x0frepository_name\x18\x01'
    b" \x01(\t\x12\x12\n\nmodel_name\x18\x02 \x01(\t\x12I\n\nparameters\x18\x03"
    b" \x03(\x0b25.inference.RepositoryModelLoadRequest.ParametersEntry\x1aV\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x122\n\x05value\x18\x02"
    b' \x01(\x0b2#.inference.ModelRepositoryParameter:\x028\x01"\x1d\n\x1bRepositoryModelLoadResponse"\xf0\x01\n\x1cRepositoryModelUnloadRequest\x12\x17\n\x0frepository_name\x18\x01'
    b" \x01(\t\x12\x12\n\nmodel_name\x18\x02 \x01(\t\x12K\n\nparameters\x18\x03"
    b" \x03(\x0b27.inference.RepositoryModelUnloadRequest.ParametersEntry\x1aV\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x122\n\x05value\x18\x02"
    b' \x01(\x0b2#.inference.ModelRepositoryParameter:\x028\x01"\x1f\n\x1dRepositoryModelUnloadResponse"/\n\x1fSystemSharedMemoryStatusRequest\x12\x0c\n\x04name\x18\x01'
    b' \x01(\t"\xa5\x02\n SystemSharedMemoryStatusResponse\x12I\n\x07regions\x18\x01'
    b" \x03(\x0b28.inference.SystemSharedMemoryStatusResponse.RegionsEntry\x1aL\n\x0cRegionStatus\x12\x0c\n\x04name\x18\x01"
    b" \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\x0e\n\x06offset\x18\x03 \x01(\x04\x12\x11\n\tbyte_size\x18\x04"
    b" \x01(\x04\x1ah\n\x0cRegionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12G\n\x05value\x18\x02"
    b' \x01(\x0b28.inference.SystemSharedMemoryStatusResponse.RegionStatus:\x028\x01"a\n!SystemSharedMemoryRegisterRequest\x12\x0c\n\x04name\x18\x01'
    b" \x01(\t\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\x0e\n\x06offset\x18\x03 \x01(\x04\x12\x11\n\tbyte_size\x18\x04"
    b' \x01(\x04"$\n"SystemSharedMemoryRegisterResponse"3\n#SystemSharedMemoryUnregisterRequest\x12\x0c\n\x04name\x18\x01'
    b' \x01(\t"&\n$SystemSharedMemoryUnregisterResponse"-\n\x1dCudaSharedMemoryStatusRequest\x12\x0c\n\x04name\x18\x01'
    b' \x01(\t"\x95\x02\n\x1eCudaSharedMemoryStatusResponse\x12G\n\x07regions\x18\x01'
    b" \x03(\x0b26.inference.CudaSharedMemoryStatusResponse.RegionsEntry\x1aB\n\x0cRegionStatus\x12\x0c\n\x04name\x18\x01"
    b" \x01(\t\x12\x11\n\tdevice_id\x18\x02 \x01(\x04\x12\x11\n\tbyte_size\x18\x03"
    b" \x01(\x04\x1af\n\x0cRegionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12E\n\x05value\x18\x02"
    b' \x01(\x0b26.inference.CudaSharedMemoryStatusResponse.RegionStatus:\x028\x01"i\n\x1fCudaSharedMemoryRegisterRequest\x12\x0c\n\x04name\x18\x01'
    b" \x01(\t\x12\x12\n\nraw_handle\x18\x02 \x01(\x0c\x12\x11\n\tdevice_id\x18\x03"
    b' \x01(\x03\x12\x11\n\tbyte_size\x18\x04 \x01(\x04""\n'
    b' CudaSharedMemoryRegisterResponse"1\n!CudaSharedMemoryUnregisterRequest\x12\x0c\n\x04name\x18\x01'
    b' \x01(\t"$\n"CudaSharedMemoryUnregisterResponse"\xe6\x01\n\x13TraceSettingRequest\x12>\n\x08settings\x18\x01'
    b" \x03(\x0b2,.inference.TraceSettingRequest.SettingsEntry\x12\x12\n\nmodel_name\x18\x02"
    b" \x01(\t\x1a\x1d\n\x0cSettingValue\x12\r\n\x05value\x18\x01"
    b" \x03(\t\x1a\\\n\rSettingsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12:\n\x05value\x18\x02"
    b' \x01(\x0b2+.inference.TraceSettingRequest.SettingValue:\x028\x01"\xd5\x01\n\x14TraceSettingResponse\x12?\n\x08settings\x18\x01'
    b" \x03(\x0b2-.inference.TraceSettingResponse.SettingsEntry\x1a\x1d\n\x0cSettingValue\x12\r\n\x05value\x18\x01"
    b" \x03(\t\x1a]\n\rSettingsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12;\n\x05value\x18\x02"
    b' \x01(\x0b2,.inference.TraceSettingResponse.SettingValue:\x028\x01"\x9a\x02\n\x12LogSettingsRequest\x12=\n\x08settings\x18\x01'
    b" \x03(\x0b2+.inference.LogSettingsRequest.SettingsEntry\x1ah\n\x0cSettingValue\x12\x14\n\nbool_param\x18\x01"
    b" \x01(\x08H\x00\x12\x16\n\x0cuint32_param\x18\x02 \x01(\rH\x00\x12\x16\n\x0cstring_param\x18\x03"
    b" \x01(\tH\x00B\x12\n\x10parameter_choice\x1a[\n\rSettingsEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x129\n\x05value\x18\x02"
    b' \x01(\x0b2*.inference.LogSettingsRequest.SettingValue:\x028\x01"\x9d\x02\n\x13LogSettingsResponse\x12>\n\x08settings\x18\x01'
    b" \x03(\x0b2,.inference.LogSettingsResponse.SettingsEntry\x1ah\n\x0cSettingValue\x12\x14\n\nbool_param\x18\x01"
    b" \x01(\x08H\x00\x12\x16\n\x0cuint32_param\x18\x02 \x01(\rH\x00\x12\x16\n\x0cstring_param\x18\x03"
    b" \x01(\tH\x00B\x12\n\x10parameter_choice\x1a\\\n\rSettingsEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12:\n\x05value\x18\x02"
    b' \x01(\x0b2+.inference.LogSettingsResponse.SettingValue:\x028\x012\xb7\x0f\n\x14GRPCInferenceService\x12K\n\nServerLive\x12\x1c.inference.ServerLiveRequest\x1a\x1d.inference.ServerLiveResponse"\x00\x12N\n\x0bServerReady\x12\x1d.inference.ServerReadyRequest\x1a\x1e.inference.ServerReadyResponse"\x00\x12K\n\nModelReady\x12\x1c.inference.ModelReadyRequest\x1a\x1d.inference.ModelReadyResponse"\x00\x12W\n\x0eServerMetadata\x12'
    b' .inference.ServerMetadataRequest\x1a!.inference.ServerMetadataResponse"\x00\x12T\n\rModelMetadata\x12\x1f.inference.ModelMetadataRequest\x1a'
    b' .inference.ModelMetadataResponse"\x00\x12K\n\nModelInfer\x12\x1c.inference.ModelInferRequest\x1a\x1d.inference.ModelInferResponse"\x00\x12[\n\x10ModelStreamInfer\x12\x1c.inference.ModelInferRequest\x1a#.inference.ModelStreamInferResponse"\x00(\x010\x01\x12N\n\x0bModelConfig\x12\x1d.inference.ModelConfigRequest\x1a\x1e.inference.ModelConfigResponse"\x00\x12Z\n\x0fModelStatistics\x12!.inference.ModelStatisticsRequest\x1a".inference.ModelStatisticsResponse"\x00\x12Z\n\x0fRepositoryIndex\x12!.inference.RepositoryIndexRequest\x1a".inference.RepositoryIndexResponse"\x00\x12f\n\x13RepositoryModelLoad\x12%.inference.RepositoryModelLoadRequest\x1a&.inference.RepositoryModelLoadResponse"\x00\x12l\n\x15RepositoryModelUnload\x12\'.inference.RepositoryModelUnloadRequest\x1a(.inference.RepositoryModelUnloadResponse"\x00\x12u\n\x18SystemSharedMemoryStatus\x12*.inference.SystemSharedMemoryStatusRequest\x1a+.inference.SystemSharedMemoryStatusResponse"\x00\x12{\n\x1aSystemSharedMemoryRegister\x12,.inference.SystemSharedMemoryRegisterRequest\x1a-.inference.SystemSharedMemoryRegisterResponse"\x00\x12\x81\x01\n\x1cSystemSharedMemoryUnregister\x12..inference.SystemSharedMemoryUnregisterRequest\x1a/.inference.SystemSharedMemoryUnregisterResponse"\x00\x12o\n\x16CudaSharedMemoryStatus\x12(.inference.CudaSharedMemoryStatusRequest\x1a).inference.CudaSharedMemoryStatusResponse"\x00\x12u\n\x18CudaSharedMemoryRegister\x12*.inference.CudaSharedMemoryRegisterRequest\x1a+.inference.CudaSharedMemoryRegisterResponse"\x00\x12{\n\x1aCudaSharedMemoryUnregister\x12,.inference.CudaSharedMemoryUnregisterRequest\x1a-.inference.CudaSharedMemoryUnregisterResponse"\x00\x12Q\n\x0cTraceSetting\x12\x1e.inference.TraceSettingRequest\x1a\x1f.inference.TraceSettingResponse"\x00\x12N\n\x0bLogSettings\x12\x1d.inference.LogSettingsRequest\x1a\x1e.inference.LogSettingsResponse"\x00B\x13Z\x11go-nvcf-worker/pbb\x06proto3'
)
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "grpc_service_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"Z\x11go-nvcf-worker/pb"
    _MODELINFERREQUEST_INFERINPUTTENSOR_PARAMETERSENTRY._options = None
    _MODELINFERREQUEST_INFERINPUTTENSOR_PARAMETERSENTRY._serialized_options = b"8\x01"
    _MODELINFERREQUEST_INFERREQUESTEDOUTPUTTENSOR_PARAMETERSENTRY._options = None
    _MODELINFERREQUEST_INFERREQUESTEDOUTPUTTENSOR_PARAMETERSENTRY._serialized_options = b"8\x01"
    _MODELINFERREQUEST_PARAMETERSENTRY._options = None
    _MODELINFERREQUEST_PARAMETERSENTRY._serialized_options = b"8\x01"
    _MODELINFERRESPONSE_INFEROUTPUTTENSOR_PARAMETERSENTRY._options = None
    _MODELINFERRESPONSE_INFEROUTPUTTENSOR_PARAMETERSENTRY._serialized_options = b"8\x01"
    _MODELINFERRESPONSE_PARAMETERSENTRY._options = None
    _MODELINFERRESPONSE_PARAMETERSENTRY._serialized_options = b"8\x01"
    _REPOSITORYMODELLOADREQUEST_PARAMETERSENTRY._options = None
    _REPOSITORYMODELLOADREQUEST_PARAMETERSENTRY._serialized_options = b"8\x01"
    _REPOSITORYMODELUNLOADREQUEST_PARAMETERSENTRY._options = None
    _REPOSITORYMODELUNLOADREQUEST_PARAMETERSENTRY._serialized_options = b"8\x01"
    _SYSTEMSHAREDMEMORYSTATUSRESPONSE_REGIONSENTRY._options = None
    _SYSTEMSHAREDMEMORYSTATUSRESPONSE_REGIONSENTRY._serialized_options = b"8\x01"
    _CUDASHAREDMEMORYSTATUSRESPONSE_REGIONSENTRY._options = None
    _CUDASHAREDMEMORYSTATUSRESPONSE_REGIONSENTRY._serialized_options = b"8\x01"
    _TRACESETTINGREQUEST_SETTINGSENTRY._options = None
    _TRACESETTINGREQUEST_SETTINGSENTRY._serialized_options = b"8\x01"
    _TRACESETTINGRESPONSE_SETTINGSENTRY._options = None
    _TRACESETTINGRESPONSE_SETTINGSENTRY._serialized_options = b"8\x01"
    _LOGSETTINGSREQUEST_SETTINGSENTRY._options = None
    _LOGSETTINGSREQUEST_SETTINGSENTRY._serialized_options = b"8\x01"
    _LOGSETTINGSRESPONSE_SETTINGSENTRY._options = None
    _LOGSETTINGSRESPONSE_SETTINGSENTRY._serialized_options = b"8\x01"
    _globals["_SERVERLIVEREQUEST"]._serialized_start = 53
    _globals["_SERVERLIVEREQUEST"]._serialized_end = 72
    _globals["_SERVERLIVERESPONSE"]._serialized_start = 74
    _globals["_SERVERLIVERESPONSE"]._serialized_end = 108
    _globals["_SERVERREADYREQUEST"]._serialized_start = 110
    _globals["_SERVERREADYREQUEST"]._serialized_end = 130
    _globals["_SERVERREADYRESPONSE"]._serialized_start = 132
    _globals["_SERVERREADYRESPONSE"]._serialized_end = 168
    _globals["_MODELREADYREQUEST"]._serialized_start = 170
    _globals["_MODELREADYREQUEST"]._serialized_end = 220
    _globals["_MODELREADYRESPONSE"]._serialized_start = 222
    _globals["_MODELREADYRESPONSE"]._serialized_end = 257
    _globals["_SERVERMETADATAREQUEST"]._serialized_start = 259
    _globals["_SERVERMETADATAREQUEST"]._serialized_end = 282
    _globals["_SERVERMETADATARESPONSE"]._serialized_start = 284
    _globals["_SERVERMETADATARESPONSE"]._serialized_end = 359
    _globals["_MODELMETADATAREQUEST"]._serialized_start = 361
    _globals["_MODELMETADATAREQUEST"]._serialized_end = 414
    _globals["_MODELMETADATARESPONSE"]._serialized_start = 417
    _globals["_MODELMETADATARESPONSE"]._serialized_end = 686
    _globals["_MODELMETADATARESPONSE_TENSORMETADATA"]._serialized_start = 623
    _globals["_MODELMETADATARESPONSE_TENSORMETADATA"]._serialized_end = 686
    _globals["_INFERPARAMETER"]._serialized_start = 689
    _globals["_INFERPARAMETER"]._serialized_end = 842
    _globals["_INFERTENSORCONTENTS"]._serialized_start = 845
    _globals["_INFERTENSORCONTENTS"]._serialized_end = 1053
    _globals["_MODELINFERREQUEST"]._serialized_start = 1056
    _globals["_MODELINFERREQUEST"]._serialized_end = 1934
    _globals["_MODELINFERREQUEST_INFERINPUTTENSOR"]._serialized_start = 1364
    _globals["_MODELINFERREQUEST_INFERINPUTTENSOR"]._serialized_end = 1640
    _globals["_MODELINFERREQUEST_INFERINPUTTENSOR_PARAMETERSENTRY"]._serialized_start = 1564
    _globals["_MODELINFERREQUEST_INFERINPUTTENSOR_PARAMETERSENTRY"]._serialized_end = 1640
    _globals["_MODELINFERREQUEST_INFERREQUESTEDOUTPUTTENSOR"]._serialized_start = 1643
    _globals["_MODELINFERREQUEST_INFERREQUESTEDOUTPUTTENSOR"]._serialized_end = 1856
    _globals["_MODELINFERREQUEST_INFERREQUESTEDOUTPUTTENSOR_PARAMETERSENTRY"]._serialized_start = 1564
    _globals["_MODELINFERREQUEST_INFERREQUESTEDOUTPUTTENSOR_PARAMETERSENTRY"]._serialized_end = 1640
    _globals["_MODELINFERREQUEST_PARAMETERSENTRY"]._serialized_start = 1564
    _globals["_MODELINFERREQUEST_PARAMETERSENTRY"]._serialized_end = 1640
    _globals["_MODELINFERRESPONSE"]._serialized_start = 1937
    _globals["_MODELINFERRESPONSE"]._serialized_end = 2534
    _globals["_MODELINFERRESPONSE_INFEROUTPUTTENSOR"]._serialized_start = 2177
    _globals["_MODELINFERRESPONSE_INFEROUTPUTTENSOR"]._serialized_end = 2456
    _globals["_MODELINFERRESPONSE_INFEROUTPUTTENSOR_PARAMETERSENTRY"]._serialized_start = 1564
    _globals["_MODELINFERRESPONSE_INFEROUTPUTTENSOR_PARAMETERSENTRY"]._serialized_end = 1640
    _globals["_MODELINFERRESPONSE_PARAMETERSENTRY"]._serialized_start = 1564
    _globals["_MODELINFERRESPONSE_PARAMETERSENTRY"]._serialized_end = 1640
    _globals["_MODELSTREAMINFERRESPONSE"]._serialized_start = 2536
    _globals["_MODELSTREAMINFERRESPONSE"]._serialized_end = 2640
    _globals["_MODELCONFIGREQUEST"]._serialized_start = 2642
    _globals["_MODELCONFIGREQUEST"]._serialized_end = 2693
    _globals["_MODELCONFIGRESPONSE"]._serialized_start = 2695
    _globals["_MODELCONFIGRESPONSE"]._serialized_end = 2756
    _globals["_MODELSTATISTICSREQUEST"]._serialized_start = 2758
    _globals["_MODELSTATISTICSREQUEST"]._serialized_end = 2813
    _globals["_STATISTICDURATION"]._serialized_start = 2815
    _globals["_STATISTICDURATION"]._serialized_end = 2861
    _globals["_INFERSTATISTICS"]._serialized_start = 2864
    _globals["_INFERSTATISTICS"]._serialized_end = 3276
    _globals["_INFERBATCHSTATISTICS"]._serialized_start = 3279
    _globals["_INFERBATCHSTATISTICS"]._serialized_end = 3481
    _globals["_MEMORYUSAGE"]._serialized_start = 3483
    _globals["_MEMORYUSAGE"]._serialized_end = 3541
    _globals["_MODELSTATISTICS"]._serialized_start = 3544
    _globals["_MODELSTATISTICS"]._serialized_end = 3819
    _globals["_MODELSTATISTICSRESPONSE"]._serialized_start = 3821
    _globals["_MODELSTATISTICSRESPONSE"]._serialized_end = 3895
    _globals["_MODELREPOSITORYPARAMETER"]._serialized_start = 3898
    _globals["_MODELREPOSITORYPARAMETER"]._serialized_end = 4036
    _globals["_REPOSITORYINDEXREQUEST"]._serialized_start = 4038
    _globals["_REPOSITORYINDEXREQUEST"]._serialized_end = 4102
    _globals["_REPOSITORYINDEXRESPONSE"]._serialized_start = 4105
    _globals["_REPOSITORYINDEXRESPONSE"]._serialized_end = 4269
    _globals["_REPOSITORYINDEXRESPONSE_MODELINDEX"]._serialized_start = 4195
    _globals["_REPOSITORYINDEXRESPONSE_MODELINDEX"]._serialized_end = 4269
    _globals["_REPOSITORYMODELLOADREQUEST"]._serialized_start = 4272
    _globals["_REPOSITORYMODELLOADREQUEST"]._serialized_end = 4508
    _globals["_REPOSITORYMODELLOADREQUEST_PARAMETERSENTRY"]._serialized_start = 4422
    _globals["_REPOSITORYMODELLOADREQUEST_PARAMETERSENTRY"]._serialized_end = 4508
    _globals["_REPOSITORYMODELLOADRESPONSE"]._serialized_start = 4510
    _globals["_REPOSITORYMODELLOADRESPONSE"]._serialized_end = 4539
    _globals["_REPOSITORYMODELUNLOADREQUEST"]._serialized_start = 4542
    _globals["_REPOSITORYMODELUNLOADREQUEST"]._serialized_end = 4782
    _globals["_REPOSITORYMODELUNLOADREQUEST_PARAMETERSENTRY"]._serialized_start = 4422
    _globals["_REPOSITORYMODELUNLOADREQUEST_PARAMETERSENTRY"]._serialized_end = 4508
    _globals["_REPOSITORYMODELUNLOADRESPONSE"]._serialized_start = 4784
    _globals["_REPOSITORYMODELUNLOADRESPONSE"]._serialized_end = 4815
    _globals["_SYSTEMSHAREDMEMORYSTATUSREQUEST"]._serialized_start = 4817
    _globals["_SYSTEMSHAREDMEMORYSTATUSREQUEST"]._serialized_end = 4864
    _globals["_SYSTEMSHAREDMEMORYSTATUSRESPONSE"]._serialized_start = 4867
    _globals["_SYSTEMSHAREDMEMORYSTATUSRESPONSE"]._serialized_end = 5160
    _globals["_SYSTEMSHAREDMEMORYSTATUSRESPONSE_REGIONSTATUS"]._serialized_start = 4978
    _globals["_SYSTEMSHAREDMEMORYSTATUSRESPONSE_REGIONSTATUS"]._serialized_end = 5054
    _globals["_SYSTEMSHAREDMEMORYSTATUSRESPONSE_REGIONSENTRY"]._serialized_start = 5056
    _globals["_SYSTEMSHAREDMEMORYSTATUSRESPONSE_REGIONSENTRY"]._serialized_end = 5160
    _globals["_SYSTEMSHAREDMEMORYREGISTERREQUEST"]._serialized_start = 5162
    _globals["_SYSTEMSHAREDMEMORYREGISTERREQUEST"]._serialized_end = 5259
    _globals["_SYSTEMSHAREDMEMORYREGISTERRESPONSE"]._serialized_start = 5261
    _globals["_SYSTEMSHAREDMEMORYREGISTERRESPONSE"]._serialized_end = 5297
    _globals["_SYSTEMSHAREDMEMORYUNREGISTERREQUEST"]._serialized_start = 5299
    _globals["_SYSTEMSHAREDMEMORYUNREGISTERREQUEST"]._serialized_end = 5350
    _globals["_SYSTEMSHAREDMEMORYUNREGISTERRESPONSE"]._serialized_start = 5352
    _globals["_SYSTEMSHAREDMEMORYUNREGISTERRESPONSE"]._serialized_end = 5390
    _globals["_CUDASHAREDMEMORYSTATUSREQUEST"]._serialized_start = 5392
    _globals["_CUDASHAREDMEMORYSTATUSREQUEST"]._serialized_end = 5437
    _globals["_CUDASHAREDMEMORYSTATUSRESPONSE"]._serialized_start = 5440
    _globals["_CUDASHAREDMEMORYSTATUSRESPONSE"]._serialized_end = 5717
    _globals["_CUDASHAREDMEMORYSTATUSRESPONSE_REGIONSTATUS"]._serialized_start = 5547
    _globals["_CUDASHAREDMEMORYSTATUSRESPONSE_REGIONSTATUS"]._serialized_end = 5613
    _globals["_CUDASHAREDMEMORYSTATUSRESPONSE_REGIONSENTRY"]._serialized_start = 5615
    _globals["_CUDASHAREDMEMORYSTATUSRESPONSE_REGIONSENTRY"]._serialized_end = 5717
    _globals["_CUDASHAREDMEMORYREGISTERREQUEST"]._serialized_start = 5719
    _globals["_CUDASHAREDMEMORYREGISTERREQUEST"]._serialized_end = 5824
    _globals["_CUDASHAREDMEMORYREGISTERRESPONSE"]._serialized_start = 5826
    _globals["_CUDASHAREDMEMORYREGISTERRESPONSE"]._serialized_end = 5860
    _globals["_CUDASHAREDMEMORYUNREGISTERREQUEST"]._serialized_start = 5862
    _globals["_CUDASHAREDMEMORYUNREGISTERREQUEST"]._serialized_end = 5911
    _globals["_CUDASHAREDMEMORYUNREGISTERRESPONSE"]._serialized_start = 5913
    _globals["_CUDASHAREDMEMORYUNREGISTERRESPONSE"]._serialized_end = 5949
    _globals["_TRACESETTINGREQUEST"]._serialized_start = 5952
    _globals["_TRACESETTINGREQUEST"]._serialized_end = 6182
    _globals["_TRACESETTINGREQUEST_SETTINGVALUE"]._serialized_start = 6059
    _globals["_TRACESETTINGREQUEST_SETTINGVALUE"]._serialized_end = 6088
    _globals["_TRACESETTINGREQUEST_SETTINGSENTRY"]._serialized_start = 6090
    _globals["_TRACESETTINGREQUEST_SETTINGSENTRY"]._serialized_end = 6182
    _globals["_TRACESETTINGRESPONSE"]._serialized_start = 6185
    _globals["_TRACESETTINGRESPONSE"]._serialized_end = 6398
    _globals["_TRACESETTINGRESPONSE_SETTINGVALUE"]._serialized_start = 6059
    _globals["_TRACESETTINGRESPONSE_SETTINGVALUE"]._serialized_end = 6088
    _globals["_TRACESETTINGRESPONSE_SETTINGSENTRY"]._serialized_start = 6305
    _globals["_TRACESETTINGRESPONSE_SETTINGSENTRY"]._serialized_end = 6398
    _globals["_LOGSETTINGSREQUEST"]._serialized_start = 6401
    _globals["_LOGSETTINGSREQUEST"]._serialized_end = 6683
    _globals["_LOGSETTINGSREQUEST_SETTINGVALUE"]._serialized_start = 6486
    _globals["_LOGSETTINGSREQUEST_SETTINGVALUE"]._serialized_end = 6590
    _globals["_LOGSETTINGSREQUEST_SETTINGSENTRY"]._serialized_start = 6592
    _globals["_LOGSETTINGSREQUEST_SETTINGSENTRY"]._serialized_end = 6683
    _globals["_LOGSETTINGSRESPONSE"]._serialized_start = 6686
    _globals["_LOGSETTINGSRESPONSE"]._serialized_end = 6971
    _globals["_LOGSETTINGSRESPONSE_SETTINGVALUE"]._serialized_start = 6486
    _globals["_LOGSETTINGSRESPONSE_SETTINGVALUE"]._serialized_end = 6590
    _globals["_LOGSETTINGSRESPONSE_SETTINGSENTRY"]._serialized_start = 6879
    _globals["_LOGSETTINGSRESPONSE_SETTINGSENTRY"]._serialized_end = 6971
    _globals["_GRPCINFERENCESERVICE"]._serialized_start = 6974
    _globals["_GRPCINFERENCESERVICE"]._serialized_end = 8949
