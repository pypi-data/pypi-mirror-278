###
# #%L
# aiSSEMBLE::Test::MDA::Machine Learning::Machine Learning Training
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from abc import ABC, abstractmethod
from ...config.pipeline_config import PipelineConfig
from krausening.logging import LogManager
from onnxmltools.convert import convert_keras
from onnxmltools.utils import save_model
from os import path


class OnnxKerasModelConversionBase(ABC):
    """
    Base onnx model conversion post-action class.

    GENERATED CODE - DO NOT MODIFY (add your customizations in ExampleOnnxKerasConversion).

    Generated from: templates/post-action/model.conversion.base.py.vm
    """
    logger = LogManager.get_instance().get_logger('OnnxKerasModelConversionBase')


    def __init__(self) -> None:
        """
        Default constructor for a onnx model conversion post-action.
        """
        self._pipeline_config = PipelineConfig()


    @property
    def converted_model_file_directory(self) -> str:
        """
        The directory to save the converted model to.

        :return: the directory so save the converted model to
        """
        return self._pipeline_config.model_directory()


    @property
    def converted_model_file_name(self) -> str:
        """
        The file name to save the converted model as.

        :return: the file name to save the converted model as
        """
        return 'converted_keras_model.onnx'


    def _convert(self, source_model) -> any:
        """
        Performs the keras-to-onnx conversion on the source model and returns the converted model.

        :source_model: the model to perform the conversion on
        :return: the converted model
        """
        OnnxKerasModelConversionBase.logger.info('Performing onnx model conversion...')

        converted_model = convert_keras(
            source_model,
            custom_shape_calculators=self.custom_shape_calculators,
            custom_conversion_functions=self.custom_conversion_functions,
            name=self.name,
            target_opset=self.target_opset,
            channel_first_inputs=self.channel_first_inputs,
            default_batch_size=self.default_batch_size,
            initial_types=self.initial_types,
            doc_string=self.doc_string,
        )

        OnnxKerasModelConversionBase.logger.info('Converted keras model to onnx format')
        return converted_model


    def _save(self, converted_model) -> None:
        """
        Saves the converted onnx model.

        :converted_model: the converted model to save
        """
        OnnxKerasModelConversionBase.logger.info('Saving converted onnx model...')

        model_file_path = path.join(self.converted_model_file_directory, self.converted_model_file_name)
        save_model(converted_model, model_file_path)

        OnnxKerasModelConversionBase.logger.info('Saved converted onnx model to {}'.format(model_file_path))


    @property
    def custom_shape_calculators(self):
        """
        Optional custom_shape_calculators parameter for the keras-to-onnx conversion.

        :return: optional custom_shape_calculators parameter value
        """
        return None


    @property
    def custom_conversion_functions(self):
        """
        Optional custom_conversion_functions parameter for the keras-to-onnx conversion.

        :return: optional custom_conversion_functions parameter value
        """
        return None


    @property
    def name(self):
        """
        Optional name parameter for the keras-to-onnx conversion.

        :return: optional name parameter value
        """
        return None


    @property
    def target_opset(self):
        """
        Optional target_opset parameter for the keras-to-onnx conversion.

        :return: optional target_opset parameter value
        """
        return None


    @property
    def channel_first_inputs(self):
        """
        Optional channel_first_inputs parameter for the keras-to-onnx conversion.

        :return: optional channel_first_inputs parameter value
        """
        return None


    @property
    def default_batch_size(self):
        """
        Optional default_batch_size parameter for the keras-to-onnx conversion.

        :return: optional default_batch_size parameter value
        """
        return 1


    @property
    def initial_types(self):
        """
        Optional initial_types parameter for the keras-to-onnx conversion.

        :return: optional initial_types parameter value
        """
        return None


    @property
    def doc_string(self):
        """
        Optional doc_string parameter for the keras-to-onnx conversion.

        :return: optional doc_string parameter value
        """
        return ''


