#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sqldoc.config import config


def test_serialize_deserialize_config(tmpdir):
    output_path = os.path.join(str(tmpdir), 'output.yaml')
    job = config.template_job()
    with open(output_path, 'w') as output_file:
        config.generate_template(output_file, job)
    with open(output_path, 'r') as output_file:
        deserialized_job = config.load(output_file)

    assert config.generate_template(None, job) == config.generate_template(None, deserialized_job)
