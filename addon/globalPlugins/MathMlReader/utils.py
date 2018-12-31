# coding: utf-8
# Access8Math: Allows access math content written by MathML in NVDA
# Copyright (C) 2017-2018 Tseng Woody <tsengwoody.tw@gmail.com>
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.

import config

def convert_bool(s):
	if s in ['True', 'true',]:
		return True
	elif s in ['False', 'false',]:
		return False
