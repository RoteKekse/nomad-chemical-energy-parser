#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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
#

from nomad.datamodel import EntryArchive
from nomad.parsing import MatchingParser

import os

from ce_nome_s import Bessy2_KMC2_XASFluorescence, Bessy2_KMC2_XASTransmission
from baseclasses.helper.utilities import create_archive, search_class, get_reference
from nomad.datamodel.metainfo.basesections import CompositeSystemReference

'''
This is a hello world style example for an example parser/converter.
'''


class XASParser(MatchingParser):
    def __init__(self):
        super().__init__(
            name='parsers/cenomegamry',
            code_name='CENOMEGAMRY',
            code_homepage='https://www.example.eu/',
            supported_compressions=[
                'gz',
                'bz2',
                'xz'])

    def parse(self, mainfile: str, archive: EntryArchive, logger):
        # Log a hello world, just to get us started. TODO remove from an actual
        # parser.

        measurement_base, measurement_name = os.path.split(mainfile)
        archive.metadata.entry_name = measurement_name

        if "tm" in measurement_name:
            xas_measurement = Bessy2_KMC2_XASTransmission()
        else:
            xas_measurement = Bessy2_KMC2_XASFluorescence()

        xas_measurement.data_file = measurement_name
        xas_measurement.name = measurement_name

        sample = search_class(archive, "CE_NOME_Sample")
        if sample is not None:
            upload_id, entry_id = sample["upload_id"], sample["entry_id"]
            xas_measurement.samples = [CompositeSystemReference(reference=get_reference(upload_id, entry_id))]

        # archive.data = cam_measurements
        if xas_measurement is not None:
            file_name = f'{measurement_name}.archive.json'
            create_archive(xas_measurement, archive, file_name)
