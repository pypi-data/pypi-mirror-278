###
# #%L
# aiSSEMBLE::Test::MDA::Data Delivery Pyspark Basic
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from ...generated.step.abstract_pipeline_step import AbstractPipelineStep
from krausening.logging import LogManager
from abc import abstractmethod
from time import time_ns
from ..pipeline.pipeline_base import PipelineBase
from pathlib import Path
from policy_manager.configuration import PolicyConfiguration
from aiops_encrypt_policy import DataEncryptionPolicy, DataEncryptionPolicyManager
import os
from typing import List



class ExampleSyncStepBase(AbstractPipelineStep):
    """
    Performs scaffolding synchronous processing for ExampleSyncStep. Business logic is delegated to the subclass.

    GENERATED CODE - DO NOT MODIFY (add your customizations in ExampleSyncStep).

    Generated from: templates/data-delivery-pyspark/synchronous.processor.base.py.vm
    """

    logger = LogManager.get_instance().get_logger('ExampleSyncStepBase')
    step_phase = 'ExampleSyncStep'
    bomIdentifier = "Unspecified ExampleSyncStep BOM identifier"

    def __init__(self, data_action_type, descriptive_label):
        super().__init__(data_action_type, descriptive_label)



    def execute_step(self) -> None:
        """
        Executes this step.
        """
        start = time_ns()
        ExampleSyncStepBase.logger.info('START: step execution...')


        self.execute_step_impl()



        stop = time_ns()
        ExampleSyncStepBase.logger.info('COMPLETE: step execution completed in %sms' % ((stop - start) / 1000000))



    @abstractmethod
    def execute_step_impl(self) -> None:
        """
        This method performs the business logic of this step, 
        and should be implemented in ExampleSyncStep.
        """
        pass



