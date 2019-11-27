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

import hashlib
import os
import pytest
import tempfile

from pathlib import Path

from cos_utils.download_files import do_download
from cos_utils.list_files import do_list
from cos_utils.upload_files import do_upload
from cos_utils.remove_files import do_remove


def identical_files(file1, file2):

    with open(file1, 'rb') as file_1:
        data_1 = file_1.read()
    with open(file2, 'rb') as file_2:
        data_2 = file_2.read()
    return hashlib.sha256(data_1).hexdigest() == \
        hashlib.sha256(data_2).hexdigest()


def test_env_settings():
    assert os.environ.get('aws_access_key_id') is not None
    assert os.environ.get('aws_secret_access_key') is not None
    assert os.environ.get('x_region_bucket_name') is not None


def test_empty_bucket():
    objects = do_list(os.environ['x_region_bucket_name'],
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])
    assert isinstance(objects, list)
    assert len(objects) == 0


def test_file_no_wildcard():

    test_empty_bucket()

    source_path = Path(os.path.dirname(__file__)) / 'assets'
    pattern = 'file1.txt'

    sources = list(source_path.glob(pattern))

    spec = str(source_path / pattern)

    count = do_upload(os.environ['x_region_bucket_name'],
                      spec,
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])
    assert isinstance(count, int)
    assert count == len(sources)

    objects = do_list(os.environ['x_region_bucket_name'],
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])
    assert isinstance(objects, list)
    assert len(objects) == len(sources)
    for i in range(len(sources) - 1):
        assert str(sources[i].name) in objects

    tempdir = tempfile.mkdtemp()

    count = do_download(os.environ['x_region_bucket_name'],
                        pattern,
                        os.environ['aws_access_key_id'],
                        os.environ['aws_secret_access_key'],
                        tempdir)
    assert isinstance(count, int)
    assert count == len(sources)

    for source in sources:
        file = str(source)
        assert identical_files(file, str(Path(tempdir) / source.name))
        os.remove(str(Path(tempdir) / source.name))

    count = do_remove(os.environ['x_region_bucket_name'],
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])
    assert count == len(sources)

    test_empty_bucket()


def test_file_wildcard():

    test_empty_bucket()

    source_path = Path(os.path.dirname(__file__)) / 'assets'
    pattern = 'file*.txt'

    sources = list(source_path.glob(pattern))

    spec = str(source_path / pattern)

    count = do_upload(os.environ['x_region_bucket_name'],
                      spec,
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])
    assert isinstance(count, int)
    assert count == len(sources)

    objects = do_list(os.environ['x_region_bucket_name'],
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])
    assert isinstance(objects, list)
    assert len(objects) == len(sources)
    for i in range(len(sources) - 1):
        assert str(sources[i].name) in objects

    tempdir = tempfile.mkdtemp()

    count = do_download(os.environ['x_region_bucket_name'],
                        pattern,
                        os.environ['aws_access_key_id'],
                        os.environ['aws_secret_access_key'],
                        tempdir)
    assert isinstance(count, int)
    assert count == len(sources)

    for source in sources:
        file = str(source)
        assert identical_files(file, str(Path(tempdir) / source.name))
        os.remove(str(Path(tempdir) / source.name))

    count = do_remove(os.environ['x_region_bucket_name'],
                      os.environ['aws_access_key_id'],
                      os.environ['aws_secret_access_key'])
    assert count == len(sources)

    test_empty_bucket()


if __name__ == '__main__':
    print(Path('.'))
    pytest.main([__file__])
