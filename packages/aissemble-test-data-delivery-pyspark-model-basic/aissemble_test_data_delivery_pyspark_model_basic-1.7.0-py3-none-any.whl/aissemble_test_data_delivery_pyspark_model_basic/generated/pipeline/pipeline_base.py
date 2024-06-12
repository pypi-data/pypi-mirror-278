###
# #%L
# aiSSEMBLE::Test::MDA::Data Delivery Pyspark Basic
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from krausening.logging import LogManager

class PipelineBase:
    """
    Performs pipeline level process for PysparkDataDeliveryBasic.

    GENERATED CODE - DO NOT MODIFY

    Generated from: templates/pipeline.base.py.vm
    """

    _instance = None
    logger = LogManager.get_instance().get_logger('PipelineBase')


    def __new__(cls):
        """
        Create a singleton class for pipeline level process
        """
        if cls._instance is None:
            print("Creating the PipelineBase")
            cls._instance = super(PipelineBase, cls).__new__(cls)
        return cls._instance






