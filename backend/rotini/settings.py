# pylint: disable=unused-import, wildcard-import, unused-wildcard-import
import os

IS_CI = os.getenv("ROTINI_CI")
IS_TEST = os.getenv("ROTINI_TEST")

if IS_CI is not None:
    from envs.ci import *
elif IS_TEST is not None:
    from envs.test import *
else:
    from envs.local import *
