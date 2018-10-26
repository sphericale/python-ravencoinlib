# Copyright (C) 2018 The python-ravencoinlib developers
#
# This file is part of python-ravencoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-ravencoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from bitcoin.core.script import *

OP_RVN_ASSET = CScriptOp(0xc0)

OPCODE_NAMES.update({OP_RVN_ASSET: 'OP_RVN_ASSET'})
OPCODES_BY_NAME.update({'OP_RVN_ASSET': OP_RVN_ASSET})
