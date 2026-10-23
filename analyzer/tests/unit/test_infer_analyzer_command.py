# -------------------------------------------------------------------------
#
#  Part of the CodeChecker project, under the Apache License v2.0 with
#  LLVM Exceptions. See LICENSE for license information.
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
# -------------------------------------------------------------------------

import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

from codechecker_analyzer.analyzers.infer.analyzer import Infer
from codechecker_analyzer.analyzers.infer.config_handler import \
    InferConfigHandler


class AnalyzerCommandInferTest(unittest.TestCase):
    def test_single_job(self):
        """
        Infer must be started with a single job, because the parallelism is
        already controlled by CodeChecker's --jobs.
        """
        cfg_handler = InferConfigHandler()
        build_action = SimpleNamespace(
            original_command="gcc -c main.c", lang='c')
        with tempfile.TemporaryDirectory() as workspace, \
                mock.patch.object(Infer, 'analyzer_binary',
                                  return_value='infer'):
            result_handler = SimpleNamespace(
                workspace=workspace, buildaction_hash='hash')
            cmd = Infer(cfg_handler, build_action) \
                .construct_analyzer_cmd(result_handler)

        self.assertEqual(cmd[cmd.index('--jobs') + 1], '1')
        self.assertLess(cmd.index('--jobs'), cmd.index('--'))
