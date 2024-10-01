# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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

import pynini
from pynini.lib import pynutil

from nemo_text_processing.text_normalization.hi.graph_utils import NEMO_NOT_QUOTE, GraphFst, delete_space, insert_space
from nemo_text_processing.text_normalization.hi.taggers.cardinal import CardinalFst
from nemo_text_processing.text_normalization.hi.taggers.decimal import DecimalFst
from nemo_text_processing.text_normalization.hi.utils import apply_fst, get_abs_path


class MoneyFst(GraphFst):
    """
    Finite state transducer for verbalizing money, e.g.
        money { integer_part: "बारह" currency: "रुपए" } -> बारह रुपए
        money { integer_part: "बारह" currency: "रुपए" fractional_part: "पचास" currency: "पैसे" } -> बारह रुपए पचास पैसे

    Args:
        cardinal: CardinalFst
        decimal: DecimalFst
        deterministic: if True will provide a single transduction option,
            for False multiple transduction are generated (used for audio-based normalization)
    """

    def __init__(self, cardinal: GraphFst, decimal: GraphFst):
        super().__init__(name="money", kind="verbalize")

        insert_paise = pynutil.insert("पैसे")

        currency = (
            pynutil.delete('currency: "') + pynini.closure(NEMO_NOT_QUOTE, 1) + pynutil.delete('" ') + insert_space
        )

        integer_part = (
            pynutil.delete('integer_part: "') + pynini.closure(NEMO_NOT_QUOTE, 1) + pynutil.delete('" ') + insert_space
        )

        fractional_part = (
            pynutil.delete('fractional_part: "')
            + pynini.closure(NEMO_NOT_QUOTE, 1)
            + pynutil.delete('" ')
            + insert_space
        )

        graph_integer = integer_part + delete_space + currency
        # graph_integer |= currency + delete_space + integer_part

        graph_interger_fraction = (
            integer_part + delete_space + currency + delete_space + fractional_part + delete_space + insert_paise
        )
        # graph_interger_fraction |= currency + delete_space + integer_part + delete_space + fractional_part + delete_space + insert_paise

        graph = graph_integer | graph_interger_fraction

        delete_tokens = self.delete_tokens(graph)
        self.fst = delete_tokens.optimize()


# cardinal = CardinalFst()
# decimal = DecimalFst(cardinal)
# money = MoneyFst(cardinal, decimal)
# input_text = 'money { currency: "रुपए"  integer_part: "उन्नीस"  }'
# input_text = 'money { integer_part: "उन्नीस" currency: "रुपए"  }'
# input_text = 'money { currency: "रुपए"  integer_part: "दो हज़ार"  fractional_part: "उन्नीस"  }'
# input_text = 'money { integer_part: "दो हज़ार" currency: "रुपए"  fractional_part: "उन्नीस"  }'
# input_text = 'money { currency: "पाउंड"  integer_part: "दो हज़ार" fractional_part: "उन्नीस"  }'
# input_text = 'money { integer_part: "दो हज़ार" currency: "पाउंड"  fractional_part: "उन्नीस" }'
# output = apply_fst(input_text, money.fst)
# print(output)
