#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
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

import os
import pytest

from pathlib import Path

from cos_utils.list_files import do_list
from cos_utils.upload_files import do_upload
from cos_utils.remove_files import do_remove


def test_env_settings():
    assert os.environ.get('aws_access_key_id') is not None
    assert os.environ.get('aws_secret_access_key') is not None
    assert os.environ.get('x_region_bucket_name') is not None


def require_empty_bucket():
    objects = do_list(os.environ['x_region_bucket_name'],
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])
    assert isinstance(objects, list)
    assert len(objects) == 0


def test_wipe_disabled():

    require_empty_bucket()

    source_path = Path(os.path.dirname(__file__)) / 'assets'
    pattern_1 = 'file*.txt'

    sources_1 = list(source_path.glob(pattern_1))

    spec = str(source_path / pattern_1)

    count = do_upload(os.environ['x_region_bucket_name'],
                      spec,
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])

    assert isinstance(count, int)
    assert count == len(sources_1)

    pattern_2 = 'data?.csv'

    sources_2 = list(source_path.glob(pattern_2))

    spec = str(source_path / pattern_2)

    count = do_upload(os.environ['x_region_bucket_name'],
                      spec,
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'],
                      wipe=False)

    assert isinstance(count, int)
    assert count == len(sources_2)

    objects = do_list(os.environ['x_region_bucket_name'],
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])

    assert isinstance(objects, list)
    assert len(objects) == len(sources_1) + len(sources_2)

    count = do_remove(os.environ['x_region_bucket_name'],
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])
    assert count == len(sources_1) + len(sources_2)

    require_empty_bucket()


def test_wipe_enabled():

    require_empty_bucket()

    source_path = Path(os.path.dirname(__file__)) / 'assets'
    pattern_1 = 'file*.txt'

    sources_1 = list(source_path.glob(pattern_1))

    spec = str(source_path / pattern_1)

    count = do_upload(os.environ['x_region_bucket_name'],
                      spec,
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'],
                      wipe=True)

    assert isinstance(count, int)
    assert count == len(sources_1)

    pattern_2 = 'data?.csv'

    sources_2 = list(source_path.glob(pattern_2))

    spec = str(source_path / pattern_2)

    count = do_upload(os.environ['x_region_bucket_name'],
                      spec,
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'],
                      wipe=True)

    assert isinstance(count, int)
    assert count == len(sources_2)

    objects = do_list(os.environ['x_region_bucket_name'],
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])

    assert isinstance(objects, list)
    assert len(objects) == len(sources_2)

    count = do_remove(os.environ['x_region_bucket_name'],
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])
    assert count == len(sources_2)

    require_empty_bucket()


if __name__ == '__main__':
    pytest.main([__file__])
