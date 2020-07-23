"""Create Raga KB from a variety of resources
@author: Nikhil Pattisapu, iREL, IIIT-H.
"""


import json
import argparse
from collections import namedtuple
from tqdm import tqdm


class Raga:
    def __init__(self, name, melam, aro, ava, janaka_melam):
        self.name = name
        self.regional_name = name
        self.aro = aro.strip().split(',')
        self.ava = ava.strip().split(',')
        self.aro_swaras, self.ava_swaras = None, None
        self.aro_seq, self.ava_seq = None, None
        self.category = None
        self.swaras = list(set(self.aro + self.ava))
        self.melam_num = melam if melam != '' else None
        self.janaka_melam = janaka_melam if janaka_melam != '' else None
        self.janaka = None
        self.chakra = None
        self.chakra_num = None
        self.hind = None
        self.kritis = None
        self.songs = None
        self.alternates = None
        self.same_aro = None
        self.same_ava = None
        self.one_swara_diff = None
        self.varnams = None
        self.kritis = None

    def get_category(self, mapping):
        """Returns raga category"""
        aro_swara = {s[0] for s in self.aro}
        ava_swara = {s[0] for s in self.ava}
        aro_cat = mapping.get(str(len(aro_swara)), None)
        ava_cat = mapping.get(str(len(ava_swara)), None)
        if aro_cat is None or ava_cat is None:
            self.category = 'no_category'
        elif aro_cat == ava_cat:
            self.category = aro_cat
        else:
            self.category = aro_cat + "-" + ava_cat

    def get_same_arohana(self, raga_list):
        """Raga names with same arohana"""
        res = [raga.name for raga in raga_list if raga.aro == self.aro]
        self.same_aro = res

    def get_same_avarohana(self, raga_list):
        """Raga names with same avarohanam"""
        res = [raga.name for raga in raga_list if raga.ava == self.ava]
        self.same_ava = res

    def get_one_swara_diff(self, raga_list):
        """Return ragas which has exactly one note different"""
        res, res_num_kritis = [], []
        s1 = set(self.swaras)
        for r in raga_list:
            s2 = set(r.swaras)
            s3, s4 = s1.difference(s2), s2.difference(s1)
            if len(s3) > 1 or len(s4) > 1:
                continue
            elif len(s3) + len(s4) >= 1:
                res.append(r.name)
                n_kritis = 0 if r.kritis is None else len(r.kritis)
                res_num_kritis.append(n_kritis)
        res = [x for _, x in sorted(zip(res_num_kritis, res), reverse=True)]
        self.one_swara_diff = res[:5]

    def get_raga_swaras(self, mapping):
        """Get the swarasthanams in raga arohanam and avarohanam"""
        self.aro_swaras = [mapping[s][0] for s in self.aro]
        self.ava_swaras = [mapping[s][0] for s in self.ava]
        aro = ["s\'" if sw == 's.' else sw for sw in self.aro]
        ava = ["s\'" if sw == 's.' else sw for sw in self.ava]
        self.aro_seq = '|'.join([s.upper().strip() for s in aro])
        self.ava_seq = '|'.join([s.upper().strip() for s in ava])

    def get_songs(self, song_list):
        """Get movie songs set to this ragam"""
        self.songs = [[s.name, s.movie_name] for s in song_list
                      if s.raga == self.name]

    def get_kritis(self, kriti_list):
        """Get kritis set in this ragam"""
        self.kritis = [[k.name, k.composer, k.link] for k in kriti_list if 
                        k.raga == self.name]

    def get_varnams(self, varnam_list):
        """Get varnams set to this ragam"""
        self.varnams = [[v.name, v.composer, v.talam] for v in varnam_list
                        if v.raga == self.name]

    def get_hindustani_ragas(self, hind_list):
        """Get hindustani ragas corresponding to carnatic"""
        self.hind = [h.name for h in hind_list if h.raga == self.name]

    def get_chakra(self, chakra_list):
        """Get chakra info if melakarta ragam"""
        for c in chakra_list:
            if c.raga == self.name:
                self.chakra = c.name
                self.chakra_num = c.num
                break

    def get_janaka(self, chakra_list):
        """Get the name of the janaka ragam"""
        if self.janaka_melam is None:
            self.janaka = None
        else:
            for c in chakra_list:
                if c.melam == self.janaka_melam:
                    self.janaka = c.raga
                    break

    def get_alternate_names(self, alt_list):
        """Get alternate names of this raga (if any)"""
        self.alternates = [a.name for a in alt_list if a.raga == self.name]


def read_psv(name, first=False):
    """returns list of lists"""
    res = [i.strip().split('|') for i in open(name, 'r').readlines()]
    return res[1:] if first else res


def transliterate(trans, item):
    """Transliterates string, list of strings and list of list of strings"""
    if isinstance(item, str):
        return trans.get(item, item)
    if isinstance(item, list) and len(item) > 0:
        if isinstance(item[0], str):
            return [trans.get(i, i) for i in item]
        if isinstance(item[0], list):
            return [[trans.get(i, i) for i in first] for first in item]
    return item


def transliterate_raga(raga, trans):
    """Returns the raga KB in transliterated format"""
    raga.regional_name = transliterate(trans, raga.regional_name)
    raga.janaka = transliterate(trans, raga.janaka)
    raga.aro_swaras = transliterate(trans, raga.aro_swaras)
    raga.ava_swaras = transliterate(trans, raga.ava_swaras)
    raga.category = transliterate(trans, raga.category)
    raga.chakra = transliterate(trans, raga.chakra)
    raga.hind = transliterate(trans, raga.hind)
    raga.kritis = transliterate(trans, raga.kritis)
    raga.songs = transliterate(trans, raga.songs)
    raga.alternates = transliterate(trans, raga.alternates)
    raga.varnams = transliterate(trans, raga.varnams)
    raga.same_aro = transliterate(trans, raga.same_aro)
    raga.same_ava = transliterate(trans, raga.same_ava)
    raga.one_swara_diff = transliterate(trans, raga.one_swara_diff)
    return raga


# Define the required Namespaces
Ragas = namedtuple('Ragas', ["name", "melam", "aro", "ava", "janaka_melam"])
Kriti = namedtuple('Kriti', ["raga", "name", "composer", "link"])
Song = namedtuple('Song', ["name", "movie_name", "raga"])
Varnam = namedtuple('Varnam', ["name", "raga", "composer", "talam"])
HindRag = namedtuple('HindRag', ["name", "thaat", "raga"])
Chakra = namedtuple('Chakra', ["name", "num", "melam", "raga"])
Alternate = namedtuple('Alternate', ["name", "raga"])


parser = argparse.ArgumentParser()
parser.add_argument('--ragas', required=True, type=str)
parser.add_argument('--kritis', required=True, type=str)
parser.add_argument('--songs', required=True, type=str)
parser.add_argument('--varnams', required=True, type=str)
parser.add_argument('--hind_ragas', required=True, type=str)
parser.add_argument('--chakras', required=True, type=str)
parser.add_argument('--alternate_names', required=True, type=str)
parser.add_argument('--transliteration', required=True, type=str)
parser.add_argument('--config', required=True, type=str)
parser.add_argument('--result', required=True, type=str)
args = parser.parse_args()


ragas = [Raga(*Ragas(*tuple(k))) for k in read_psv(args.ragas, True)]
kritis = [Kriti(*tuple(k)) for k in read_psv(args.kritis, True)]
songs = [Song(*tuple(s)) for s in read_psv(args.songs)]
varnams = [Varnam(*tuple(v)) for v in read_psv(args.varnams)]
hind_ragas = [HindRag(*tuple(h)) for h in read_psv(args.hind_ragas)]
chakras = [Chakra(*tuple(c)) for c in read_psv(args.chakras)]
alternates = [Alternate(*tuple(a)) for a in read_psv(args.alternate_names)]
config = json.load(open(args.config, 'r'))
trans_dict = {k: v for k, v in read_psv(args.transliteration)}
map_config = config['map']
cat_config = config['category']


for ix in tqdm(range(len(ragas))):
    ragas[ix].get_kritis(kritis)
    ragas[ix].get_raga_swaras(map_config)
    ragas[ix].get_songs(songs)
    ragas[ix].get_varnams(varnams)
    ragas[ix].get_hindustani_ragas(hind_ragas)
    ragas[ix].get_alternate_names(alternates)
    ragas[ix].get_chakra(chakras)
    ragas[ix].get_janaka(chakras)
    other_ragas = [r for idx, r in enumerate(ragas) if idx != ix]
    ragas[ix].get_same_arohana(other_ragas)
    ragas[ix].get_same_avarohana(other_ragas)
    ragas[ix].get_one_swara_diff(other_ragas)
    ragas[ix].get_category(cat_config)
    ragas[ix] = transliterate_raga(ragas[ix], trans_dict)


with open(args.result, 'w', encoding="utf-8") as rf:
    json.dump([ob.__dict__ for ob in ragas], rf, ensure_ascii=False)
