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
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x12model_config.proto\x12\tinference"\x96\x01\n\x10ModelRateLimiter\x127\n\tresources\x18\x01'
    b" \x03(\x0b2$.inference.ModelRateLimiter.Resource\x12\x10\n\x08priority\x18\x02"
    b" \x01(\r\x1a7\n\x08Resource\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06global\x18\x02"
    b' \x01(\x08\x12\r\n\x05count\x18\x03 \x01(\r"\x87\x04\n\x12ModelInstanceGroup\x12\x0c\n\x04name\x18\x01'
    b' \x01(\t\x120\n\x04kind\x18\x04 \x01(\x0e2".inference.ModelInstanceGroup.Kind\x12\r\n\x05count\x18\x02'
    b" \x01(\x05\x121\n\x0crate_limiter\x18\x06 \x01(\x0b2\x1b.inference.ModelRateLimiter\x12\x0c\n\x04gpus\x18\x03"
    b" \x03(\x05\x12H\n\x11secondary_devices\x18\x08"
    b" \x03(\x0b2-.inference.ModelInstanceGroup.SecondaryDevice\x12\x0f\n\x07profile\x18\x05"
    b" \x03(\t\x12\x0f\n\x07passive\x18\x07 \x01(\x08\x12\x13\n\x0bhost_policy\x18\t"
    b" \x01(\t\x1a\x9c\x01\n\x0fSecondaryDevice\x12O\n\x04kind\x18\x01"
    b" \x01(\x0e2A.inference.ModelInstanceGroup.SecondaryDevice.SecondaryDeviceKind\x12\x11\n\tdevice_id\x18\x02"
    b' \x01(\x03"%\n\x13SecondaryDeviceKind\x12\x0e\n\nKIND_NVDLA\x10\x00"A\n\x04Kind\x12\r\n\tKIND_AUTO\x10\x00\x12\x0c\n\x08KIND_GPU\x10\x01\x12\x0c\n\x08KIND_CPU\x10\x02\x12\x0e\n\nKIND_MODEL\x10\x03"#\n\x12ModelTensorReshape\x12\r\n\x05shape\x18\x01'
    b' \x03(\x03"\xb2\x02\n\nModelInput\x12\x0c\n\x04name\x18\x01 \x01(\t\x12&\n\tdata_type\x18\x02'
    b" \x01(\x0e2\x13.inference.DataType\x12,\n\x06format\x18\x03"
    b" \x01(\x0e2\x1c.inference.ModelInput.Format\x12\x0c\n\x04dims\x18\x04 \x03(\x03\x12.\n\x07reshape\x18\x05"
    b" \x01(\x0b2\x1d.inference.ModelTensorReshape\x12\x17\n\x0fis_shape_tensor\x18\x06"
    b" \x01(\x08\x12\x1a\n\x12allow_ragged_batch\x18\x07 \x01(\x08\x12\x10\n\x08optional\x18\x08"
    b' \x01(\x08";\n\x06Format\x12\x0f\n\x0bFORMAT_NONE\x10\x00\x12\x0f\n\x0bFORMAT_NHWC\x10\x01\x12\x0f\n\x0bFORMAT_NCHW\x10\x02"\xb2\x01\n\x0bModelOutput\x12\x0c\n\x04name\x18\x01'
    b" \x01(\t\x12&\n\tdata_type\x18\x02 \x01(\x0e2\x13.inference.DataType\x12\x0c\n\x04dims\x18\x03"
    b" \x03(\x03\x12.\n\x07reshape\x18\x05"
    b" \x01(\x0b2\x1d.inference.ModelTensorReshape\x12\x16\n\x0elabel_filename\x18\x04"
    b' \x01(\t\x12\x17\n\x0fis_shape_tensor\x18\x06 \x01(\x08"\xd9\x02\n\nBatchInput\x12(\n\x04kind\x18\x01'
    b" \x01(\x0e2\x1a.inference.BatchInput.Kind\x12\x13\n\x0btarget_name\x18\x02 \x03(\t\x12&\n\tdata_type\x18\x03"
    b" \x01(\x0e2\x13.inference.DataType\x12\x14\n\x0csource_input\x18\x04"
    b' \x03(\t"\xcd\x01\n\x04Kind\x12\x17\n\x13BATCH_ELEMENT_COUNT\x10\x00\x12#\n\x1fBATCH_ACCUMULATED_ELEMENT_COUNT\x10\x01\x12-\n)BATCH_ACCUMULATED_ELEMENT_COUNT_WITH_ZERO\x10\x02\x12$\n'
    b' BATCH_MAX_ELEMENT_COUNT_AS_SHAPE\x10\x03\x12\x14\n\x10BATCH_ITEM_SHAPE\x10\x04\x12\x1c\n\x18BATCH_ITEM_SHAPE_FLATTEN\x10\x05"\x8f\x01\n\x0bBatchOutput\x12\x13\n\x0btarget_name\x18\x01'
    b" \x03(\t\x12)\n\x04kind\x18\x02 \x01(\x0e2\x1b.inference.BatchOutput.Kind\x12\x14\n\x0csource_input\x18\x03"
    b' \x03(\t"*\n\x04Kind\x12"\n\x1eBATCH_SCATTER_WITH_INPUT_SHAPE\x10\x00"\x90\x02\n\x12ModelVersionPolicy\x126\n\x06latest\x18\x01'
    b" \x01(\x0b2$.inference.ModelVersionPolicy.LatestH\x00\x120\n\x03all\x18\x02"
    b" \x01(\x0b2!.inference.ModelVersionPolicy.AllH\x00\x12:\n\x08specific\x18\x03"
    b" \x01(\x0b2&.inference.ModelVersionPolicy.SpecificH\x00\x1a\x1e\n\x06Latest\x12\x14\n\x0cnum_versions\x18\x01"
    b" \x01(\r\x1a\x05\n\x03All\x1a\x1c\n\x08Specific\x12\x10\n\x08versions\x18\x01"
    b' \x03(\x03B\x0f\n\rpolicy_choice"\xfd\r\n\x17ModelOptimizationPolicy\x127\n\x05graph\x18\x01'
    b" \x01(\x0b2(.inference.ModelOptimizationPolicy.Graph\x12B\n\x08priority\x18\x02"
    b" \x01(\x0e20.inference.ModelOptimizationPolicy.ModelPriority\x125\n\x04cuda\x18\x03"
    b" \x01(\x0b2'.inference.ModelOptimizationPolicy.Cuda\x12X\n\x16execution_accelerators\x18\x04"
    b" \x01(\x0b28.inference.ModelOptimizationPolicy.ExecutionAccelerators\x12R\n\x13input_pinned_memory\x18\x05"
    b" \x01(\x0b25.inference.ModelOptimizationPolicy.PinnedMemoryBuffer\x12S\n\x14output_pinned_memory\x18\x06"
    b" \x01(\x0b25.inference.ModelOptimizationPolicy.PinnedMemoryBuffer\x12&\n\x1egather_kernel_buffer_threshold\x18\x07"
    b" \x01(\r\x12\x16\n\x0eeager_batching\x18\x08 \x01(\x08\x1a\x16\n\x05Graph\x12\r\n\x05level\x18\x01"
    b" \x01(\x05\x1a\xba\x05\n\x04Cuda\x12\x0e\n\x06graphs\x18\x01 \x01(\x08\x12\x18\n\x10busy_wait_events\x18\x02"
    b" \x01(\x08\x12E\n\ngraph_spec\x18\x03"
    b" \x03(\x0b21.inference.ModelOptimizationPolicy.Cuda.GraphSpec\x12\x1a\n\x12output_copy_stream\x18\x04"
    b" \x01(\x08\x1a\xa4\x04\n\tGraphSpec\x12\x12\n\nbatch_size\x18\x01 \x01(\x05\x12K\n\x05input\x18\x02"
    b" \x03(\x0b2<.inference.ModelOptimizationPolicy.Cuda.GraphSpec.InputEntry\x12W\n\x11graph_lower_bound\x18\x03"
    b" \x01(\x0b2<.inference.ModelOptimizationPolicy.Cuda.GraphSpec.LowerBound\x1a\x14\n\x05Shape\x12\x0b\n\x03dim\x18\x01"
    b" \x03(\x03\x1a\xdf\x01\n\nLowerBound\x12\x12\n\nbatch_size\x18\x01 \x01(\x05\x12V\n\x05input\x18\x02"
    b" \x03(\x0b2G.inference.ModelOptimizationPolicy.Cuda.GraphSpec.LowerBound.InputEntry\x1ae\n\nInputEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12F\n\x05value\x18\x02"
    b" \x01(\x0b27.inference.ModelOptimizationPolicy.Cuda.GraphSpec.Shape:\x028\x01\x1ae\n\nInputEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12F\n\x05value\x18\x02"
    b" \x01(\x0b27.inference.ModelOptimizationPolicy.Cuda.GraphSpec.Shape:\x028\x01\x1a\xa4\x03\n\x15ExecutionAccelerators\x12g\n\x19gpu_execution_accelerator\x18\x01"
    b" \x03(\x0b2D.inference.ModelOptimizationPolicy.ExecutionAccelerators.Accelerator\x12g\n\x19cpu_execution_accelerator\x18\x02"
    b" \x03(\x0b2D.inference.ModelOptimizationPolicy.ExecutionAccelerators.Accelerator\x1a\xb8\x01\n\x0bAccelerator\x12\x0c\n\x04name\x18\x01"
    b" \x01(\t\x12h\n\nparameters\x18\x02"
    b" \x03(\x0b2T.inference.ModelOptimizationPolicy.ExecutionAccelerators.Accelerator.ParametersEntry\x1a1\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x028\x01\x1a$\n\x12PinnedMemoryBuffer\x12\x0e\n\x06enable\x18\x01"
    b' \x01(\x08"I\n\rModelPriority\x12\x14\n\x10PRIORITY_DEFAULT\x10\x00\x12\x10\n\x0cPRIORITY_MAX\x10\x01\x12\x10\n\x0cPRIORITY_MIN\x10\x02"\xdb\x01\n\x10ModelQueuePolicy\x12A\n\x0etimeout_action\x18\x01'
    b" \x01(\x0e2).inference.ModelQueuePolicy.TimeoutAction\x12$\n\x1cdefault_timeout_microseconds\x18\x02"
    b" \x01(\x04\x12\x1e\n\x16allow_timeout_override\x18\x03 \x01(\x08\x12\x16\n\x0emax_queue_size\x18\x04"
    b' \x01(\r"&\n\rTimeoutAction\x12\n\n\x06REJECT\x10\x00\x12\t\n\x05DELAY\x10\x01"\x9b\x03\n\x14ModelDynamicBatching\x12\x1c\n\x14preferred_batch_size\x18\x01'
    b" \x03(\x05\x12$\n\x1cmax_queue_delay_microseconds\x18\x02 \x01(\x04\x12\x19\n\x11preserve_ordering\x18\x03"
    b" \x01(\x08\x12\x17\n\x0fpriority_levels\x18\x04 \x01(\x04\x12\x1e\n\x16default_priority_level\x18\x05"
    b" \x01(\x04\x129\n\x14default_queue_policy\x18\x06"
    b" \x01(\x0b2\x1b.inference.ModelQueuePolicy\x12W\n\x15priority_queue_policy\x18\x07"
    b" \x03(\x0b28.inference.ModelDynamicBatching.PriorityQueuePolicyEntry\x1aW\n\x18PriorityQueuePolicyEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\x04\x12*\n\x05value\x18\x02"
    b' \x01(\x0b2\x1b.inference.ModelQueuePolicy:\x028\x01"\x8b\n\n\x15ModelSequenceBatching\x12A\n\x06direct\x18\x03'
    b" \x01(\x0b2/.inference.ModelSequenceBatching.StrategyDirectH\x00\x12A\n\x06oldest\x18\x04"
    b" \x01(\x0b2/.inference.ModelSequenceBatching.StrategyOldestH\x00\x12&\n\x1emax_sequence_idle_microseconds\x18\x01"
    b" \x01(\x04\x12D\n\rcontrol_input\x18\x02"
    b" \x03(\x0b2-.inference.ModelSequenceBatching.ControlInput\x125\n\x05state\x18\x05"
    b" \x03(\x0b2&.inference.ModelSequenceBatching.State\x1a\xb1\x02\n\x07Control\x12;\n\x04kind\x18\x01"
    b" \x01(\x0e2-.inference.ModelSequenceBatching.Control.Kind\x12\x18\n\x10int32_false_true\x18\x02"
    b" \x03(\x05\x12\x17\n\x0ffp32_false_true\x18\x03 \x03(\x02\x12\x17\n\x0fbool_false_true\x18\x05"
    b" \x03(\x08\x12&\n\tdata_type\x18\x04"
    b' \x01(\x0e2\x13.inference.DataType"u\n\x04Kind\x12\x1a\n\x16CONTROL_SEQUENCE_START\x10\x00\x12\x1a\n\x16CONTROL_SEQUENCE_READY\x10\x01\x12\x18\n\x14CONTROL_SEQUENCE_END\x10\x02\x12\x1b\n\x17CONTROL_SEQUENCE_CORRID\x10\x03\x1aW\n\x0cControlInput\x12\x0c\n\x04name\x18\x01'
    b" \x01(\t\x129\n\x07control\x18\x02"
    b" \x03(\x0b2(.inference.ModelSequenceBatching.Control\x1a\x8a\x01\n\x0cInitialState\x12&\n\tdata_type\x18\x01"
    b" \x01(\x0e2\x13.inference.DataType\x12\x0c\n\x04dims\x18\x02 \x03(\x03\x12\x13\n\tzero_data\x18\x03"
    b" \x01(\x08H\x00\x12\x13\n\tdata_file\x18\x04 \x01(\tH\x00\x12\x0c\n\x04name\x18\x05"
    b" \x01(\tB\x0c\n\nstate_data\x1a\xac\x01\n\x05State\x12\x12\n\ninput_name\x18\x01"
    b" \x01(\t\x12\x13\n\x0boutput_name\x18\x02 \x01(\t\x12&\n\tdata_type\x18\x03"
    b" \x01(\x0e2\x13.inference.DataType\x12\x0c\n\x04dims\x18\x04 \x03(\x03\x12D\n\rinitial_state\x18\x05"
    b" \x03(\x0b2-.inference.ModelSequenceBatching.InitialState\x1aX\n\x0eStrategyDirect\x12$\n\x1cmax_queue_delay_microseconds\x18\x01"
    b" \x01(\x04\x12 \n\x18minimum_slot_utilization\x18\x02"
    b" \x01(\x02\x1a\x90\x01\n\x0eStrategyOldest\x12\x1f\n\x17max_candidate_sequences\x18\x01"
    b" \x01(\x05\x12\x1c\n\x14preferred_batch_size\x18\x02 \x03(\x05\x12$\n\x1cmax_queue_delay_microseconds\x18\x03"
    b" \x01(\x04\x12\x19\n\x11preserve_ordering\x18\x04"
    b' \x01(\x08B\x11\n\x0fstrategy_choice"\xf6\x02\n\x0fModelEnsembling\x12-\n\x04step\x18\x01'
    b" \x03(\x0b2\x1f.inference.ModelEnsembling.Step\x1a\xb3\x02\n\x04Step\x12\x12\n\nmodel_name\x18\x01"
    b" \x01(\t\x12\x15\n\rmodel_version\x18\x02 \x01(\x03\x12@\n\tinput_map\x18\x03"
    b" \x03(\x0b2-.inference.ModelEnsembling.Step.InputMapEntry\x12B\n\noutput_map\x18\x04"
    b" \x03(\x0b2..inference.ModelEnsembling.Step.OutputMapEntry\x12\x17\n\x0fmodel_namespace\x18\x05"
    b" \x01(\t\x1a/\n\rInputMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02"
    b" \x01(\t:\x028\x01\x1a0\n\x0eOutputMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02"
    b' \x01(\t:\x028\x01"&\n\x0eModelParameter\x12\x14\n\x0cstring_value\x18\x01'
    b' \x01(\t"\xd9\x02\n\x0bModelWarmup\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x12\n\nbatch_size\x18\x02'
    b' \x01(\r\x122\n\x06inputs\x18\x03 \x03(\x0b2".inference.ModelWarmup.InputsEntry\x12\r\n\x05count\x18\x04'
    b" \x01(\r\x1a\x97\x01\n\x05Input\x12&\n\tdata_type\x18\x01"
    b" \x01(\x0e2\x13.inference.DataType\x12\x0c\n\x04dims\x18\x02 \x03(\x03\x12\x13\n\tzero_data\x18\x03"
    b" \x01(\x08H\x00\x12\x15\n\x0brandom_data\x18\x04 \x01(\x08H\x00\x12\x19\n\x0finput_data_file\x18\x05"
    b" \x01(\tH\x00B\x11\n\x0finput_data_type\x1aK\n\x0bInputsEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12+\n\x05value\x18\x02"
    b' \x01(\x0b2\x1c.inference.ModelWarmup.Input:\x028\x01".\n\x0fModelOperations\x12\x1b\n\x13op_library_filename\x18\x01'
    b' \x03(\t"+\n\x16ModelTransactionPolicy\x12\x11\n\tdecoupled\x18\x01'
    b' \x01(\x08"\xe6\x01\n\x15ModelRepositoryAgents\x126\n\x06agents\x18\x01'
    b" \x03(\x0b2&.inference.ModelRepositoryAgents.Agent\x1a\x94\x01\n\x05Agent\x12\x0c\n\x04name\x18\x01"
    b" \x01(\t\x12J\n\nparameters\x18\x02"
    b" \x03(\x0b26.inference.ModelRepositoryAgents.Agent.ParametersEntry\x1a1\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01"
    b' \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x028\x01"$\n\x12ModelResponseCache\x12\x0e\n\x06enable\x18\x01'
    b' \x01(\x08"\xb2\n\n\x0bModelConfig\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08platform\x18\x02'
    b" \x01(\t\x12\x0f\n\x07backend\x18\x11 \x01(\t\x125\n\x0eversion_policy\x18\x03"
    b" \x01(\x0b2\x1d.inference.ModelVersionPolicy\x12\x16\n\x0emax_batch_size\x18\x04"
    b" \x01(\x05\x12$\n\x05input\x18\x05 \x03(\x0b2\x15.inference.ModelInput\x12&\n\x06output\x18\x06"
    b" \x03(\x0b2\x16.inference.ModelOutput\x12*\n\x0bbatch_input\x18\x14"
    b" \x03(\x0b2\x15.inference.BatchInput\x12,\n\x0cbatch_output\x18\x15"
    b" \x03(\x0b2\x16.inference.BatchOutput\x128\n\x0coptimization\x18\x0c"
    b' \x01(\x0b2".inference.ModelOptimizationPolicy\x12;\n\x10dynamic_batching\x18\x0b'
    b" \x01(\x0b2\x1f.inference.ModelDynamicBatchingH\x00\x12=\n\x11sequence_batching\x18\r \x01(\x0b2"
    b" .inference.ModelSequenceBatchingH\x00\x129\n\x13ensemble_scheduling\x18\x0f"
    b" \x01(\x0b2\x1a.inference.ModelEnsemblingH\x00\x125\n\x0einstance_group\x18\x07"
    b" \x03(\x0b2\x1d.inference.ModelInstanceGroup\x12\x1e\n\x16default_model_filename\x18\x08"
    b" \x01(\t\x12H\n\x12cc_model_filenames\x18\t"
    b" \x03(\x0b2,.inference.ModelConfig.CcModelFilenamesEntry\x12;\n\x0bmetric_tags\x18\n"
    b" \x03(\x0b2&.inference.ModelConfig.MetricTagsEntry\x12:\n\nparameters\x18\x0e"
    b" \x03(\x0b2&.inference.ModelConfig.ParametersEntry\x12,\n\x0cmodel_warmup\x18\x10"
    b" \x03(\x0b2\x16.inference.ModelWarmup\x124\n\x10model_operations\x18\x12"
    b" \x01(\x0b2\x1a.inference.ModelOperations\x12C\n\x18model_transaction_policy\x18\x13"
    b" \x01(\x0b2!.inference.ModelTransactionPolicy\x12A\n\x17model_repository_agents\x18\x17 \x01(\x0b2"
    b" .inference.ModelRepositoryAgents\x125\n\x0eresponse_cache\x18\x18"
    b" \x01(\x0b2\x1d.inference.ModelResponseCache\x1a7\n\x15CcModelFilenamesEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x028\x01\x1a1\n\x0fMetricTagsEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x028\x01\x1aL\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01"
    b" \x01(\t\x12(\n\x05value\x18\x02"
    b" \x01(\x0b2\x19.inference.ModelParameter:\x028\x01B\x13\n\x11scheduling_choice*\xfa\x01\n\x08DataType\x12\x10\n\x0cTYPE_INVALID\x10\x00\x12\r\n\tTYPE_BOOL\x10\x01\x12\x0e\n\nTYPE_UINT8\x10\x02\x12\x0f\n\x0bTYPE_UINT16\x10\x03\x12\x0f\n\x0bTYPE_UINT32\x10\x04\x12\x0f\n\x0bTYPE_UINT64\x10\x05\x12\r\n\tTYPE_INT8\x10\x06\x12\x0e\n\nTYPE_INT16\x10\x07\x12\x0e\n\nTYPE_INT32\x10\x08\x12\x0e\n\nTYPE_INT64\x10\t\x12\r\n\tTYPE_FP16\x10\n\x12\r\n\tTYPE_FP32\x10\x0b\x12\r\n\tTYPE_FP64\x10\x0c\x12\x0f\n\x0bTYPE_STRING\x10\r\x12\r\n\tTYPE_BF16\x10\x0eB\x13Z\x11go-nvcf-worker/pbb\x06proto3"
)
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "model_config_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b"Z\x11go-nvcf-worker/pb"
    _MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC_LOWERBOUND_INPUTENTRY._options = None
    _MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC_LOWERBOUND_INPUTENTRY._serialized_options = b"8\x01"
    _MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC_INPUTENTRY._options = None
    _MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC_INPUTENTRY._serialized_options = b"8\x01"
    _MODELOPTIMIZATIONPOLICY_EXECUTIONACCELERATORS_ACCELERATOR_PARAMETERSENTRY._options = None
    _MODELOPTIMIZATIONPOLICY_EXECUTIONACCELERATORS_ACCELERATOR_PARAMETERSENTRY._serialized_options = b"8\x01"
    _MODELDYNAMICBATCHING_PRIORITYQUEUEPOLICYENTRY._options = None
    _MODELDYNAMICBATCHING_PRIORITYQUEUEPOLICYENTRY._serialized_options = b"8\x01"
    _MODELENSEMBLING_STEP_INPUTMAPENTRY._options = None
    _MODELENSEMBLING_STEP_INPUTMAPENTRY._serialized_options = b"8\x01"
    _MODELENSEMBLING_STEP_OUTPUTMAPENTRY._options = None
    _MODELENSEMBLING_STEP_OUTPUTMAPENTRY._serialized_options = b"8\x01"
    _MODELWARMUP_INPUTSENTRY._options = None
    _MODELWARMUP_INPUTSENTRY._serialized_options = b"8\x01"
    _MODELREPOSITORYAGENTS_AGENT_PARAMETERSENTRY._options = None
    _MODELREPOSITORYAGENTS_AGENT_PARAMETERSENTRY._serialized_options = b"8\x01"
    _MODELCONFIG_CCMODELFILENAMESENTRY._options = None
    _MODELCONFIG_CCMODELFILENAMESENTRY._serialized_options = b"8\x01"
    _MODELCONFIG_METRICTAGSENTRY._options = None
    _MODELCONFIG_METRICTAGSENTRY._serialized_options = b"8\x01"
    _MODELCONFIG_PARAMETERSENTRY._options = None
    _MODELCONFIG_PARAMETERSENTRY._serialized_options = b"8\x01"
    _globals["_DATATYPE"]._serialized_start = 8189
    _globals["_DATATYPE"]._serialized_end = 8439
    _globals["_MODELRATELIMITER"]._serialized_start = 34
    _globals["_MODELRATELIMITER"]._serialized_end = 184
    _globals["_MODELRATELIMITER_RESOURCE"]._serialized_start = 129
    _globals["_MODELRATELIMITER_RESOURCE"]._serialized_end = 184
    _globals["_MODELINSTANCEGROUP"]._serialized_start = 187
    _globals["_MODELINSTANCEGROUP"]._serialized_end = 706
    _globals["_MODELINSTANCEGROUP_SECONDARYDEVICE"]._serialized_start = 483
    _globals["_MODELINSTANCEGROUP_SECONDARYDEVICE"]._serialized_end = 639
    _globals["_MODELINSTANCEGROUP_SECONDARYDEVICE_SECONDARYDEVICEKIND"]._serialized_start = 602
    _globals["_MODELINSTANCEGROUP_SECONDARYDEVICE_SECONDARYDEVICEKIND"]._serialized_end = 639
    _globals["_MODELINSTANCEGROUP_KIND"]._serialized_start = 641
    _globals["_MODELINSTANCEGROUP_KIND"]._serialized_end = 706
    _globals["_MODELTENSORRESHAPE"]._serialized_start = 708
    _globals["_MODELTENSORRESHAPE"]._serialized_end = 743
    _globals["_MODELINPUT"]._serialized_start = 746
    _globals["_MODELINPUT"]._serialized_end = 1052
    _globals["_MODELINPUT_FORMAT"]._serialized_start = 993
    _globals["_MODELINPUT_FORMAT"]._serialized_end = 1052
    _globals["_MODELOUTPUT"]._serialized_start = 1055
    _globals["_MODELOUTPUT"]._serialized_end = 1233
    _globals["_BATCHINPUT"]._serialized_start = 1236
    _globals["_BATCHINPUT"]._serialized_end = 1581
    _globals["_BATCHINPUT_KIND"]._serialized_start = 1376
    _globals["_BATCHINPUT_KIND"]._serialized_end = 1581
    _globals["_BATCHOUTPUT"]._serialized_start = 1584
    _globals["_BATCHOUTPUT"]._serialized_end = 1727
    _globals["_BATCHOUTPUT_KIND"]._serialized_start = 1685
    _globals["_BATCHOUTPUT_KIND"]._serialized_end = 1727
    _globals["_MODELVERSIONPOLICY"]._serialized_start = 1730
    _globals["_MODELVERSIONPOLICY"]._serialized_end = 2002
    _globals["_MODELVERSIONPOLICY_LATEST"]._serialized_start = 1918
    _globals["_MODELVERSIONPOLICY_LATEST"]._serialized_end = 1948
    _globals["_MODELVERSIONPOLICY_ALL"]._serialized_start = 1950
    _globals["_MODELVERSIONPOLICY_ALL"]._serialized_end = 1955
    _globals["_MODELVERSIONPOLICY_SPECIFIC"]._serialized_start = 1957
    _globals["_MODELVERSIONPOLICY_SPECIFIC"]._serialized_end = 1985
    _globals["_MODELOPTIMIZATIONPOLICY"]._serialized_start = 2005
    _globals["_MODELOPTIMIZATIONPOLICY"]._serialized_end = 3794
    _globals["_MODELOPTIMIZATIONPOLICY_GRAPH"]._serialized_start = 2535
    _globals["_MODELOPTIMIZATIONPOLICY_GRAPH"]._serialized_end = 2557
    _globals["_MODELOPTIMIZATIONPOLICY_CUDA"]._serialized_start = 2560
    _globals["_MODELOPTIMIZATIONPOLICY_CUDA"]._serialized_end = 3258
    _globals["_MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC"]._serialized_start = 2710
    _globals["_MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC"]._serialized_end = 3258
    _globals["_MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC_SHAPE"]._serialized_start = 2909
    _globals["_MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC_SHAPE"]._serialized_end = 2929
    _globals["_MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC_LOWERBOUND"]._serialized_start = 2932
    _globals["_MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC_LOWERBOUND"]._serialized_end = 3155
    _globals["_MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC_LOWERBOUND_INPUTENTRY"]._serialized_start = 3054
    _globals["_MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC_LOWERBOUND_INPUTENTRY"]._serialized_end = 3155
    _globals["_MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC_INPUTENTRY"]._serialized_start = 3054
    _globals["_MODELOPTIMIZATIONPOLICY_CUDA_GRAPHSPEC_INPUTENTRY"]._serialized_end = 3155
    _globals["_MODELOPTIMIZATIONPOLICY_EXECUTIONACCELERATORS"]._serialized_start = 3261
    _globals["_MODELOPTIMIZATIONPOLICY_EXECUTIONACCELERATORS"]._serialized_end = 3681
    _globals["_MODELOPTIMIZATIONPOLICY_EXECUTIONACCELERATORS_ACCELERATOR"]._serialized_start = 3497
    _globals["_MODELOPTIMIZATIONPOLICY_EXECUTIONACCELERATORS_ACCELERATOR"]._serialized_end = 3681
    _globals["_MODELOPTIMIZATIONPOLICY_EXECUTIONACCELERATORS_ACCELERATOR_PARAMETERSENTRY"]._serialized_start = 3632
    _globals["_MODELOPTIMIZATIONPOLICY_EXECUTIONACCELERATORS_ACCELERATOR_PARAMETERSENTRY"]._serialized_end = 3681
    _globals["_MODELOPTIMIZATIONPOLICY_PINNEDMEMORYBUFFER"]._serialized_start = 3683
    _globals["_MODELOPTIMIZATIONPOLICY_PINNEDMEMORYBUFFER"]._serialized_end = 3719
    _globals["_MODELOPTIMIZATIONPOLICY_MODELPRIORITY"]._serialized_start = 3721
    _globals["_MODELOPTIMIZATIONPOLICY_MODELPRIORITY"]._serialized_end = 3794
    _globals["_MODELQUEUEPOLICY"]._serialized_start = 3797
    _globals["_MODELQUEUEPOLICY"]._serialized_end = 4016
    _globals["_MODELQUEUEPOLICY_TIMEOUTACTION"]._serialized_start = 3978
    _globals["_MODELQUEUEPOLICY_TIMEOUTACTION"]._serialized_end = 4016
    _globals["_MODELDYNAMICBATCHING"]._serialized_start = 4019
    _globals["_MODELDYNAMICBATCHING"]._serialized_end = 4430
    _globals["_MODELDYNAMICBATCHING_PRIORITYQUEUEPOLICYENTRY"]._serialized_start = 4343
    _globals["_MODELDYNAMICBATCHING_PRIORITYQUEUEPOLICYENTRY"]._serialized_end = 4430
    _globals["_MODELSEQUENCEBATCHING"]._serialized_start = 4433
    _globals["_MODELSEQUENCEBATCHING"]._serialized_end = 5724
    _globals["_MODELSEQUENCEBATCHING_CONTROL"]._serialized_start = 4758
    _globals["_MODELSEQUENCEBATCHING_CONTROL"]._serialized_end = 5063
    _globals["_MODELSEQUENCEBATCHING_CONTROL_KIND"]._serialized_start = 4946
    _globals["_MODELSEQUENCEBATCHING_CONTROL_KIND"]._serialized_end = 5063
    _globals["_MODELSEQUENCEBATCHING_CONTROLINPUT"]._serialized_start = 5065
    _globals["_MODELSEQUENCEBATCHING_CONTROLINPUT"]._serialized_end = 5152
    _globals["_MODELSEQUENCEBATCHING_INITIALSTATE"]._serialized_start = 5155
    _globals["_MODELSEQUENCEBATCHING_INITIALSTATE"]._serialized_end = 5293
    _globals["_MODELSEQUENCEBATCHING_STATE"]._serialized_start = 5296
    _globals["_MODELSEQUENCEBATCHING_STATE"]._serialized_end = 5468
    _globals["_MODELSEQUENCEBATCHING_STRATEGYDIRECT"]._serialized_start = 5470
    _globals["_MODELSEQUENCEBATCHING_STRATEGYDIRECT"]._serialized_end = 5558
    _globals["_MODELSEQUENCEBATCHING_STRATEGYOLDEST"]._serialized_start = 5561
    _globals["_MODELSEQUENCEBATCHING_STRATEGYOLDEST"]._serialized_end = 5705
    _globals["_MODELENSEMBLING"]._serialized_start = 5727
    _globals["_MODELENSEMBLING"]._serialized_end = 6101
    _globals["_MODELENSEMBLING_STEP"]._serialized_start = 5794
    _globals["_MODELENSEMBLING_STEP"]._serialized_end = 6101
    _globals["_MODELENSEMBLING_STEP_INPUTMAPENTRY"]._serialized_start = 6004
    _globals["_MODELENSEMBLING_STEP_INPUTMAPENTRY"]._serialized_end = 6051
    _globals["_MODELENSEMBLING_STEP_OUTPUTMAPENTRY"]._serialized_start = 6053
    _globals["_MODELENSEMBLING_STEP_OUTPUTMAPENTRY"]._serialized_end = 6101
    _globals["_MODELPARAMETER"]._serialized_start = 6103
    _globals["_MODELPARAMETER"]._serialized_end = 6141
    _globals["_MODELWARMUP"]._serialized_start = 6144
    _globals["_MODELWARMUP"]._serialized_end = 6489
    _globals["_MODELWARMUP_INPUT"]._serialized_start = 6261
    _globals["_MODELWARMUP_INPUT"]._serialized_end = 6412
    _globals["_MODELWARMUP_INPUTSENTRY"]._serialized_start = 6414
    _globals["_MODELWARMUP_INPUTSENTRY"]._serialized_end = 6489
    _globals["_MODELOPERATIONS"]._serialized_start = 6491
    _globals["_MODELOPERATIONS"]._serialized_end = 6537
    _globals["_MODELTRANSACTIONPOLICY"]._serialized_start = 6539
    _globals["_MODELTRANSACTIONPOLICY"]._serialized_end = 6582
    _globals["_MODELREPOSITORYAGENTS"]._serialized_start = 6585
    _globals["_MODELREPOSITORYAGENTS"]._serialized_end = 6815
    _globals["_MODELREPOSITORYAGENTS_AGENT"]._serialized_start = 6667
    _globals["_MODELREPOSITORYAGENTS_AGENT"]._serialized_end = 6815
    _globals["_MODELREPOSITORYAGENTS_AGENT_PARAMETERSENTRY"]._serialized_start = 3632
    _globals["_MODELREPOSITORYAGENTS_AGENT_PARAMETERSENTRY"]._serialized_end = 3681
    _globals["_MODELRESPONSECACHE"]._serialized_start = 6817
    _globals["_MODELRESPONSECACHE"]._serialized_end = 6853
    _globals["_MODELCONFIG"]._serialized_start = 6856
    _globals["_MODELCONFIG"]._serialized_end = 8186
    _globals["_MODELCONFIG_CCMODELFILENAMESENTRY"]._serialized_start = 7981
    _globals["_MODELCONFIG_CCMODELFILENAMESENTRY"]._serialized_end = 8036
    _globals["_MODELCONFIG_METRICTAGSENTRY"]._serialized_start = 8038
    _globals["_MODELCONFIG_METRICTAGSENTRY"]._serialized_end = 8087
    _globals["_MODELCONFIG_PARAMETERSENTRY"]._serialized_start = 8089
    _globals["_MODELCONFIG_PARAMETERSENTRY"]._serialized_end = 8165
