import math
import json
from copy import copy, deepcopy


class InputDataUtil:

    def __init__(self, default_rules, input_ponders, raw_input,
                 domain=(-1, 1), range=(-3, 5)):

        self.raw_input = [d for d in deepcopy(raw_input) if d['value'] != 0]
        self.rules = default_rules
        self.input_ponders = input_ponders
        self.domain = domain
        self.range = range
        self.particular_colors = self.list_particular_colors()

        self.rule_keys = ["layout", "colors", "symbols", "direct_rules", "particular_colors"]
        self.data = {}

        self.process_raw_input()

    # Simple proportional mapping, from one range to another
    @staticmethod
    def map_range(n, domain, range):
        return ((n - domain[0]) / (domain[1] - domain[0])) * (range[1] - range[0]) + range[0]

    # Specially designed exponential function
    # For mapping a pondered input value
    # Onto a factor in default rules
    def exponential_map(self, value, ponder, domain=None, range=None):
        if domain is None:
            domain = self.domain
        if range is None:
            range = self.range
        half_range = (range[1] - range[0]) / 2
        zero = range[1] - half_range
        pondered_range = (zero - ponder * half_range, zero + ponder * half_range)
        value = InputDataUtil.map_range(value, domain, pondered_range)
        result = math.exp(value) / math.e
        return result

    # Append particular colors
    # (granular ones within primary color groups)
    def list_particular_colors(self):
        particular_colors = []
        for primary in self.rules['colors']:
            for color in primary['variations']:
                particular_colors.append(color)
        return particular_colors

    # Check if inverse applies
    # Inverse value if ponder is negative
    def check_value(self, value, ponder):
        if ponder < 0:
            inverse = (self.domain[1], self.domain[0])
            return InputDataUtil.map_range(value, self.domain, inverse)
        else:
            return value

    # Adjust bipolar values from domain (-1, 1) onto range (0, 1)
    def adjust_to_half_range(self, value, type):
        if type == 'bipolar':
            half_range = (0, self.domain[1])
            return InputDataUtil.map_range(value, self.domain, half_range)
        else:
            return value

    # Create a pool of new filters
    # Getting ponders from input-ponders
    # for every record in raw data input
    def process_raw_input(self):
        for r in self.raw_input:
            ponders = self.input_ponders[r['key']]
            for pk in ponders.keys():
                for name in ponders[pk].keys():
                    v = self.check_value(r['value'], ponders[pk][name])
                    p = abs(ponders[pk][name])
                    if (pk, name) not in self.data:
                        self.data[(pk, name)] = {
                            'value': v,
                            'ponder_total': p,
                            'ponder_count': 1,
                            'type': r['type']
                        }
                    else:
                        vd = self.data[(pk, name)]['value']
                        ptd = self.data[(pk, name)]['ponder_total']
                        pc = self.data[(pk, name)]['ponder_count']
                        self.data[(pk, name)] = {
                            'value': (vd * ptd + v * p) / (ptd + p),
                            'ponder_total': ptd + p,
                            'ponder_count': pc + 1,
                            'type': r['type']
                        }

    # Calculating ponders for each rule
    def update_rules(self):
        for k in self.data.keys():
            key, name = k
            v = self.data[k]['value']
            p = self.data[k]['ponder_total'] / self.data[k]['ponder_count']
            if key == 'direct_rules':
                t = self.data[k]['type']
                v = self.adjust_to_half_range(v, t)
                self.rules[key][name] = v * p
                # self.rules[key][name] = (v + p) / 2
            elif key == 'particular_colors':
                # pass
                rule = [r for r in self.particular_colors if r['name'] == name][0]
                factor = self.exponential_map(v, p)
                rule['weight'] *= factor
            else:
                rule = [r for r in self.rules[key] if r['name'] == name][0]
                factor = self.exponential_map(v, p)
                rule['weight'] *= factor

        return self.rules


if __name__ == '__main__':
    rules_path = 'conf/flag-rules.json'
    symbols_path = 'conf/flag-symbols.json'
    rules = json.load(open(rules_path))
    symbols = json.load(open(symbols_path))
    rules['symbols'] = symbols['symbols']

    input_ponders_path = 'conf/input-ponders.json'
    input_ponders = json.load(open(input_ponders_path))

    dummy_input = [
        {"key": "warm", "value": 0.5, "type": "bipolar"},
        {"key": "complex", "value": 0.8, "type": "bipolar"},
        {"key": "anarchist", "value": 0, "type": "unipolar"},
        {"key": "african", "value": 0, "type": "unipolar"},
        {"key": "slavic", "value": 1, "type": "unipolar"},
        {"key": "corporate", "value": 0, "type": "unipolar"}
    ]
    # dummy_input = [
    #     {"key": "complex", "value": 0.1, "type": "bipolar"}
    # ]
    # dummy_input = [
    #     {"key": "warm", "value": 0.4, "type": "bipolar"},
    #     {"key": "slavic", "value": 1, "type": "unipolar"}
    # ]
    dummy_input = [
        {"key": "light", "value": 1, "type": "bipolar"}
    ]

    iu = InputDataUtil(default_rules=rules, input_ponders=input_ponders, raw_input=dummy_input)
    iu.update_rules()
    # iu.process_raw_input()
    # iu.update_rules()
