# -*- coding: utf-8 -*-

#   Copyright (c) 2010-2014, MIT Probabilistic Computing Project
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import requests
import json
import warnings
from pkg_resources import parse_version

from bayeslite.version import __version__

def version_check():
    """Check bayeslite version against remote server.

    Warn, with `warnings.warn`, if the server reports the version not
    current.
    """
    SERVICE = 'https://projects.csail.mit.edu/probcomp/bayesdb/bayeslite.version'

    # arg: {'package':'bayeslite','version':'something','build':'something-else'}
    # response: {'version':'0.5','url':'http://probcomp.org/bayesdb/release'}
    payload = {
        'package': 'bayeslite',
        'version': __version__,
    }
    headers = {
        'User-Agent': 'bayeslite %s' % (__version__,),
    }

    try:
        # TODO: It would be nice to be async about this. Set 1 second timeout.
        r = requests.get(SERVICE, params=payload, timeout=1, headers=headers)
        if (r.status_code == 200 and
            parse_version(__version__) < parse_version(r.json()['version'])):
            msg = '''
                Bayeslite is not up to date. You are running %s, version %s is available.
                See %s
                ''' % (__version__, r.json()['version'], r.json()['url'])
            warnings.warn(msg)
    except Exception:
        # Silently eat exceptions.
        pass