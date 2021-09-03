import math
import json
import copy


class InputUtil:

    def __init__(self, default_rules, input_factors, raw_input,
                 domain=(0, 1), range=(-3, 5)):

        self.rules = default_rules
        self.input_factors = input_factors
        self.raw_input = raw_input
        self.domain = domain
        self.range = range
        self.bipolar_domain = (domain[0] - (domain[1] - domain[0]), domain[1])
        self.directs_count = {}
        self.direct_threshold = (domain[1] - domain[0]) * 0.333 + domain[0]
        self.rule_keys = ["layout", "colors", "symbols"]
        self.data = {
            "layout": [],
            "colors": [],
            "symbols": []
        }
        self.process_raw_input()

    @staticmethod
    def map_range(n, domain, range):
        return ((n - domain[0]) / (domain[1] - domain[0])) * (range[1] - range[0]) + range[0]

    @staticmethod
    def exp_in(arg, domain, range, ponder):
        half_range = (range[1] - range[0]) / 2
        zero = range[1] - half_range
        pondered_range = (zero - ponder * half_range, zero + ponder * half_range)
        # arg = InputUtil.map_proportion(arg, domain[0], domain[1], range[0], range[1])
        arg = InputUtil.map_range(arg, domain, pondered_range)
        return math.exp(arg) / math.e

    def record_value(self, record):
        if record['type'] == "direct":
            return record['value']
        else:
            r = self.range_params[record['type']]
            return InputUtil.exp_in(record['value'], domain=self.domain, range=r)

    def filters4rule(self, rule, rule_key):
        values = []
        max_ponder = 0

        for d in self.data[rule_key]:
            if d['name'] == rule['name']:
                v = d['value']
                sp = d['strength_ponder']
                if sp > max_ponder:
                    values = [v]
                    max_ponder = sp
                elif sp == max_ponder:
                    values.append(v)

        if len(values) == 0:
            return None
        # rn = rule['name']
        # if rn == 'red' or rn == 'orange' or rn == 'green':
        #     print(f"\n{rn}")
        #     print(values)
        avg_value = sum(values) / len(values)
        factor = self.exp_in(avg_value, self.bipolar_domain, self.range, max_ponder)
        return factor

    def adjust_bipolar_records(self, d):
        if d['type'] == 'bipolar':
            d['value'] = InputUtil.map_range(d['value'], self.domain, self.bipolar_domain)

    def filter_input(self, record, input_filter, fk):
        for f in input_filter[fk]:
            d = {
                'name': f['name'],
                'strength_ponder': f['ponder'],
                'value': record['value'],
                'type': record['type']
            }
            if 'valence' in f and f['valence'] == 'inverse':
                rng = (self.domain[1], self.domain[0])
                d['value'] = InputUtil.map_range(d['value'], self.domain, rng)
            self.adjust_bipolar_records(d)
            dv = d['value']
            dsp = d['strength_ponder']
            exp_check = self.exp_in(dv, self.bipolar_domain, self.range, dsp)
            if exp_check != 1:
                self.data[fk].append(d)
            # dn = d['name']
            # if dn == 'red' or dn == 'orange' or dn == 'green':
            #     print(f"{dn}: {dv}, {dsp}, exp> {exp_check}")

    def process_directs(self, record):
        v, k, p = record['value'], record['key'], record['power']
        dr = self.rules['direct_rules']
        cnt = self.directs_count
        # print(f"{k}, {v}")
        if k not in cnt:
            # if v != dr[k]:
            dr[k] = v
            cnt[k] = p
        else:
            dr[k] = (cnt[k] * dr[k] + p * v) / (cnt[k] + p)
            cnt[k] += p

    # Create a pool of new filters
    def process_raw_input(self):
        fi = self.filter_input
        for record in self.raw_input:
            inf = self.input_factors[record['key']]
            for fk in inf.keys():
                if fk == 'direct_rules':
                    for dr_key in inf[fk].keys():
                        orig_value = copy.copy(record['value'])
                        self.adjust_bipolar_records(record)
                        # if record['value'] > self.direct_threshold:
                        if record['value'] != 0:
                            self.process_directs({
                                "key": dr_key,
                                "value": inf[fk][dr_key] * orig_value,
                                "power": abs(record['value'])
                            })
                else:
                    fi(record=record, input_filter=inf, fk=fk)

    # Adjust default rules according to filters
    def update_rules(self):
        for rk in self.rule_keys:
            for r in self.rules[rk]:
                filter = self.filters4rule(r, rk)
                if filter:
                    r['weight'] *= filter
                    # r['weight'] = 5 * filter
                    # r['weight'] = filter
        # print()
        # print(self.rules['direct_rules'])
        return self.rules


if __name__ == '__main__':
    rules_path = 'conf/flag-rules.json'
    symbols_path = 'conf/flag-symbols.json'
    rules = json.load(open(rules_path))
    symbols = json.load(open(symbols_path))
    rules['symbols'] = symbols['symbols']

    input_factors_path = 'conf/input-factors.json'
    input_factors = json.load(open(input_factors_path))

    dummy_input = [
        {"key": "warm", "value": 0.5, "type": "bipolar"},
        {"key": "complexity", "value": 0.6, "type": "direct"},
        {"key": "anarchist", "value": 1, "type": "unipolar"},
        {"key": "african", "value": 0, "type": "unipolar"},
        {"key": "slavic", "value": 0, "type": "unipolar"},
        {"key": "corporate", "value": 0, "type": "unipolar"}
    ]

    iu = InputUtil(default_rules=rules, input_factors=input_factors, raw_input=dummy_input)
    # iu.process_raw_input()
    iu.update_rules()
