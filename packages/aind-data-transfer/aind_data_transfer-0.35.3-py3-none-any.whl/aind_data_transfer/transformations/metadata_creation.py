"""This module will have classes that handle mapping to metadata files."""
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Type

import aind_data_schema.base
import requests
from aind_data_schema.models.organizations import Organization
from aind_data_schema.models.modalities import Modality
from aind_data_schema.core.data_description import (
    Funding,
    RawDataDescription,
)
from aind_data_schema.core.procedures import Procedures
from aind_data_schema.core.processing import (
    DataProcess,
    PipelineProcess,
    Processing,
    ProcessName,
)
from aind_data_schema.core.subject import Subject
from aind_data_schema.models.pid_names import PIDName
from aind_metadata_service.client import AindMetadataServiceClient
from pydantic import ValidationError
from requests import Response
from requests.exceptions import ConnectionError, JSONDecodeError

from aind_data_transfer import __version__ as aind_data_transfer_version
from aind_data_transfer.config_loader.base_config import ModalityConfigs


class MetadataCreation(ABC):
    """Abstract class with convenient methods to handle metadata creation."""

    def __init__(self, model_obj: Optional[dict] = None):
        """
        Default class constructor.
        Parameters
        ----------
        model_obj : Optional[dict]
          The metadata as a dict object. We'll use this representation to
          avoid potential dependency conflicts from aind_data_schema. We can
          validate any of the incoming data using the version of
          aind_data_schema attached to aind_data_transfer.
        """
        self.model_obj = model_obj

    @staticmethod
    @abstractmethod
    def _model() -> Type[aind_data_schema.base.AindCoreModel]:
        """
        Returns
        -------
          Needs to return an AindCoreModel, such as Subject for example.
        """

    @property
    def output_filename(self):
        """Returns the default json file name for the model as defined in
        aind_data_schema."""
        return self._model().model_construct().default_filename()

    @classmethod
    def from_file(cls, file_location: Path):
        """
        Construct a MetadataCreation instance from a json file.
        Parameters
        ----------
        file_location : Path
          Location of the json file

        """
        with open(file_location) as f:
            contents = json.load(f)
        return cls(model_obj=contents)

    def validate_obj(self) -> bool:
        """
        Validate the model object. Logs a warning if the model_obj is not
        valid.
        Returns
        -------
        bool
          True if the model is valid. False otherwise.

        """
        try:
            self._model().model_validate(self.model_obj)
            logging.info("Model is valid.")
            return True
        except Exception as e:
            logging.warning(f"Validation Errors: {repr(e)}")
            return False

    def get_model(self):
        model = self._model()
        if self.validate_obj() is True:
            return model.model_validate(self.model_obj)
        else:
            return model.model_construct(**self.model_obj)

    def write_to_json(self, path: Path, suffix: str = None) -> None:
        """
        Write the model_obj to a json file. If the Path is a directory, it will
        use the output_filename method to generate the filename.
        Parameters
        ----------
        path : Path
          Location of where to save the json file. Can be a directory or file.

        Returns
        -------
        None

        """
        model = self.get_model()
        return model.write_standard_file(output_directory=path, suffix=suffix)


class ServiceMetadataCreation(MetadataCreation):
    """Abstract class for metadata pulled from aind_metadata_service"""

    def __init__(self, model_obj: Optional[dict] = None):
        """
        Default class constructor.
        Parameters
        ----------
        model_obj : Optional[dict]
          The metadata as a dict object. We'll use this representation to
          avoid potential dependency conflicts from aind_data_schema. We can
          validate any of the incoming data using the version of
          aind_data_schema attached to aind_data_transfer.
        """
        super().__init__(model_obj=model_obj)

    @staticmethod
    @abstractmethod
    def _get_service_response(
        subject_id: str,
        ams_client: AindMetadataServiceClient,
    ) -> Response:
        """
        Abstract method to retrieve metadata from the service.
        Parameters
        ----------
        subject_id : str
          ID of the subject we want to get metadata for.
        ams_client : AindMetadataServiceClient
          A client to connect to aind_metadata_service.

        Returns
        -------
        Response
          Has a status code and json contents.

        """

    @classmethod
    def from_service(cls, subject_id: str, domain: str):
        """
        Build the class from data pulled from aind_metadata_service.
        Parameters
        ----------
        subject_id : str
          ID of the subject we want to get metadata for.
        domain : str
          Domain name for aind_metadata_service

        """
        ams_client = AindMetadataServiceClient(domain=domain)
        try:
            response = cls._get_service_response(
                subject_id=subject_id, ams_client=ams_client
            )
            response_json = response.json()
            status_code = response.status_code
            # Everything is okay
            if status_code == 200:
                contents = response_json["data"]
            # Multiple items were found
            elif status_code == 300:
                logging.warning(f"{cls.__name__}: {response_json['message']}")
                contents = response_json["data"][0]
            # The data retrieved is invalid
            elif status_code == 406:
                logging.warning(f"{cls.__name__}: {response_json['message']}")
                contents = response_json["data"]
            # Connected to the service, but no data was found
            elif status_code == 404:
                logging.warning(f"{cls.__name__}: {response_json['message']}")
                contents = json.loads(cls._model().model_construct().model_dump_json())
            # A serious error happened. Build a default model.
            else:
                logging.error(f"{cls.__name__}: {response_json['message']}")
                contents = json.loads(cls._model().model_construct().model_dump_json())
        except (ConnectionError, JSONDecodeError) as e:
            logging.error(
                f"{cls.__name__}: An error occurred connecting to metadata "
                f"service: {e}"
            )
            contents = json.loads(cls._model().model_construct().model_dump_json())
        return cls(model_obj=contents)


class SubjectMetadata(ServiceMetadataCreation):
    """Class to manage building the subject metadata"""

    @staticmethod
    def _model() -> Type[aind_data_schema.base.AindCoreModel]:
        """AindDataSchema model"""
        return Subject

    @staticmethod
    def _get_service_response(
        subject_id: str, ams_client: AindMetadataServiceClient
    ) -> Response:
        """
        Method to retrieve metadata from the service.
        Parameters
        ----------
        subject_id : str
          ID of the subject we want to get metadata for.
        ams_client : AindMetadataServiceClient
          A client to connect to aind_metadata_service.

        Returns
        -------
        Response
          Has a status code and json contents.

        """
        return ams_client.get_subject(subject_id)


class ProceduresMetadata(ServiceMetadataCreation):
    """Class to manage building the procedures metadata"""

    @staticmethod
    def _model() -> Type[aind_data_schema.base.AindCoreModel]:
        """AindDataSchema model"""
        return Procedures

    @staticmethod
    def _get_service_response(
        subject_id: str, ams_client: AindMetadataServiceClient
    ) -> Response:
        """
        Method to retrieve metadata from the service.
        Parameters
        ----------
        subject_id : str
          ID of the subject we want to get metadata for.
        ams_client : AindMetadataServiceClient
          A client to connect to aind_metadata_service.

        Returns
        -------
        Response
          Has a status code and json contents.

        """
        return ams_client.get_procedures(subject_id)


class ProcessingMetadata(MetadataCreation):
    """Class to manage building the processing metadata"""

    @staticmethod
    def _model() -> Type[aind_data_schema.base.AindCoreModel]:
        """AindDataSchema model"""
        return Processing

    @classmethod
    def from_inputs(
        cls,
        process_name: ProcessName,
        start_date_time: datetime,
        end_date_time: datetime,
        input_location: str,
        output_location: str,
        code_url: str,
        parameters: dict,
        processor_full_name: str,
        notes: Optional[str] = None,
    ):
        """
        Build a ProcessingMetadata instance using some basic parameters.
        Parameters
        ----------
        process_name : ProcessName
          Name of the process
        start_date_time : datetime
          Start date and time of the process
        end_date_time : datetime
          End date and time of the process
        input_location : str
          Location of the files that are being processed
        output_location : str
          Location of the files that are being processed
        code_url : str
          Location of the processing code
        parameters : dict
          Parameters used in the process
        processor_full_name : str
          Name of entity responsible for data processing
        notes : Optional[str]
          Optional notes. Defaults to None.

        """
        data_processing_instance = DataProcess(
            name=process_name.value,
            software_version=aind_data_transfer_version,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            input_location=input_location,
            output_location=output_location,
            code_url=code_url,
            parameters=parameters,
            notes=notes,
        )
        pipeline_process_instance = PipelineProcess(
            data_processes=[data_processing_instance],
            processor_full_name=processor_full_name,
        )
        processing_instance = Processing(
            processing_pipeline=pipeline_process_instance
        )
        # Do this to use enum strings instead of classes in dict representation
        contents = json.loads(processing_instance.model_dump_json())
        return cls(model_obj=contents)

    @classmethod
    def from_modalities_configs(
        cls,
        modality_configs: List[ModalityConfigs],
        start_date_time: datetime,
        end_date_time: datetime,
        output_location: str,
        code_url: str,
        processor_full_name: str,
        notes: Optional[str] = None,
    ):
        """
        Build a ProcessingMetadata instance using some basic parameters.
        Parameters
        ----------
        modality_configs : List[ModalityConfigs]
          List of modality configs
        start_date_time : datetime
          Start date and time of the process
        end_date_time : datetime
          End date and time of the process
        output_location : str
          Location of the files that are being processed
        code_url : str
          Location of the processing code
        processor_full_name : str
          Name of entity responsible for data processing
        notes : Optional[str]
          Optional notes. Defaults to None.

        """
        data_processes = []
        for modality_config in modality_configs:
            if modality_config.compress_raw_data == True:
                process_name = ProcessName.COMPRESSION
                data_processing_instance = DataProcess(
                    name=process_name.value,
                    software_version=aind_data_transfer_version,
                    start_date_time=start_date_time,
                    end_date_time=end_date_time,
                    input_location=str(modality_config.source),
                    output_location=output_location,
                    code_url=code_url,
                    parameters=modality_config.dict(),
                    notes=notes,
                )
                data_processes.append(data_processing_instance)
        pipeline_process_instance = PipelineProcess(
            data_processes=data_processes,
            processor_full_name=processor_full_name,
        )
        processing_instance = Processing(
            processing_pipeline=pipeline_process_instance
        )
        # Do this to use enum strings instead of classes in dict representation
        contents = json.loads(processing_instance.model_dump_json())
        return cls(model_obj=contents)


class RawDataDescriptionMetadata(MetadataCreation):
    """Class to handle the creation of the raw data description metadata
    file."""

    @staticmethod
    def _model() -> Type[aind_data_schema.base.AindCoreModel]:
        """AindDataSchema model"""
        return RawDataDescription

    @classmethod
    def from_inputs(
            cls,
            ams_domain: str,
            project_name: str,
            name: str,
            modality: List[Modality],
            institution: Optional[Organization] = Organization.AIND,
    ):
        """
        Build a RawDataDescriptionMetadata instance using some basic
        parameters.
        Parameters
        ----------
        ams_domain: str
          Domain of aind_metadata_service.
        project_name: str
          Name of the project being funded
        name : str
          Name of the raw data
        modality : List[Modality]
          Modalities of experiment data
        institution : Optional[Institution]
          Primary Institution. Defaults to AIND.

        """

        ams_response = requests.get(
            "/".join([ams_domain, "funding", project_name])
        )
        if ams_response.status_code == 200:
            funding_info = [ams_response.json().get("data")]
        elif ams_response.status_code == 300:
            funding_info = ams_response.json().get("data")
        else:
            funding_info = []
        investigators = set()
        for f in funding_info:
            project_fundees = f.get("fundee", "").split(",")
            pid_names = [PIDName(name=p).model_dump_json() for p in project_fundees]
            if project_fundees is not [""]:
                investigators.update(pid_names)
        investigators = [PIDName.model_validate_json(i) for i in investigators]
        investigators.sort(key=lambda x: x.name)

        basic_settings = RawDataDescription.parse_name(name=name)
        try:
            data_description_instance = RawDataDescription(
                name=name,
                institution=institution,
                modality=modality,
                funding_source=funding_info,
                investigators=investigators,
                project_name=project_name,
                **basic_settings,
            )
        except ValidationError:
            data_description_instance = RawDataDescription.model_construct(
                name=name,
                institution=institution,
                modality=modality,
                funding_source=funding_info,
                investigators=investigators,
                project_name=project_name,
                **basic_settings,
            )

        contents = json.loads(data_description_instance.model_dump_json())
        return cls(model_obj=contents)
