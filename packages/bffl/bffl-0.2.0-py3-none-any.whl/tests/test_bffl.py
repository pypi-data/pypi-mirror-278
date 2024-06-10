import pytest
from bffl.bffl import uint, sint, struct, metastruct, decimal, utf8, svreg
from random import seed, randint, choice
from typing import Sequence, Iterator

def test_simple():
    u4t = uint(4)  # type
    u4 = u4t()  # bound field
    u4.n_ = 3  # raw int value

    assert repr(u4t) == 'uint(4)'
    assert repr(u4) == '<3>'
    assert u4.n_ == 3
    assert u4 == 3
    u4 += 2
    assert u4 == 5
    u4 *= 2
    assert u4 == 10
    u4 //= 2
    assert u4 == 5

    with pytest.raises(TypeError):
        u4 /= 2

def test_hex_bin():
    x = uint(35)()
    x.hex_ = 'f1234567f'
    assert x == 0x71234567f
    assert x.bin_ == '11100010010001101000101011001111111'
    assert x.hex_ == '71234567f'

    x.hex_ = '0xfL'
    assert x == 15

    x.bin_ = '0B111L'
    assert x.bin_ == '00000000000000000000000000000000111'

def test_struct():
    eric = struct('eric', [
        ("a", uint(3)),
        ("b", uint(4)),
    ])

    idle = struct('idle', [
        ('f', eric[10]),  # array of 10 eric elements
        ('c', uint(5)),
    ])

    foobar = struct('foobar', [
        ('a', uint(3, enum_={"alpha": 0, "beta": 1, "gamma": 2})),  # 3 bit integer with enum
        ('b', sint(4)),  # 4 bit integer
        ('bars', idle[5]),  # array of 5 bars
    ])

    f = foobar(0)
    f.a = 'beta'
    f.b = -1
    print(f"f['b'] = {f['b']}")

    assert f.b == -1

    with pytest.raises(KeyError):
        f['c']

    with pytest.raises(AttributeError):
        f.c

    assert repr(idle) == "struct('idle', [('f', eric[10]), ('c', uint(5))])"
    assert repr(eric) == "struct('eric', [('a', uint(3)), ('b', uint(4))])"

def test_class():
    class eric(metaclass=metastruct):
        a: uint(3)
        b: uint(4)

    assert repr(eric) == "struct('eric', [('a', uint(3)), ('b', uint(4))])"
    print (eric.classdef_)
    assert eric.classdef_ == '''class eric(metaclass=metastruct):
    a: uint(3)
    b: uint(4)

'''

def test_decimal():
    money = decimal(16, 2)(123.45)

    assert money == 123.45
    assert money.n_ == 12345
    assert money + 1.0 == 124.45

def test_expr():
    class seven_type(metaclass=metastruct):
        a: uint(3)
        b: uint(4)

    seven = seven_type()

    assert seven.a.expr_() == '(n >> 4 & 0x7)'
    assert seven.b.expr_() == '(n & 0xf)'

    ab = seven['a * b']

    seven.a = 5
    seven.b = 11

    assert seven.a == 5
    assert ab == 55

    assert ab.expr_() == '(n >> 4 & 0x7) * (n & 0xf)'
    assert ab.expr_() == '(n >> 4 & 0x7) * (n & 0xf)'

def test_unicode():
    s = utf8(10)()
    s.v_ = 'abc'
    assert s.v_ == 'abc'

def test_svreg():
    r = svreg(28)(0xabadbee)
    r2 = r[15:4]
    assert r2 == 0xbad
    r2.v_ = 0xead
    r[3:0] = 0xd
    assert r == 0xdeadbee

def test_readme_parrot():
    class parrot_struct(metaclass=metastruct):
        status: uint(2, {'dead': 0, 'pining': 1, 'resting': 2})
        plumage_rgb: uint(5)[3]

    death_enum = uint(3, {
        'vorpal_bunny': 0,
        'liverectomy': 1,
        'ni': 2,
        'question': 3,
        'mint': 4,
        'not dead yet': 5,
    })

    class knight_struct(metaclass=metastruct):
        name: utf8(20)
        cause_of_death: death_enum

    class quest_struct(metaclass=metastruct):
        quest: uint(3, enum_={'grail': 0, 'shrubbery': 1, 'meaning': 2, 'larch': 3, 'gourd': 4})
        knights: knight_struct[3]
        holy: uint(1)
        parrot: parrot_struct

    def print_sequence_of_integers():
        # these values are copied into hard-coded sequence_of_integers_from_somewhere
        seed(123)
        n = 2 ** quest_struct.size_
        q = quest_struct()

        names = [
            'Arthur', 'Issac Newton', 'Eric', 'Who Says Ni', 'Galahad', 'Lancelot',
            'Gawain', 'Percivale', 'Lionell', 'Tristram de Lyones', 'Gareth', 'Bedivere',
            'Bleoberis', 'Lacotemale Taile', 'Lucan', 'Palomedes', 'Lamorak',
            'Bors de Ganis', 'Safer', 'Pelleas', 'Kay', 'Ector de Maris', 'Dagonet',
            'Degore', 'Brunor le Noir', 'Lebius Desconneu', 'Alymere', 'Mordred',
            ]

        def choose_rand_enum(e):
            e.n_ = choice(list(e.enum_.values()))

        for _ in range(20):
            q.n_ = randint(0, n - 1)
            choose_rand_enum(q.quest)
            for j in range(q.knights.dim_):
                q.knights[j].name = 'Sir ' + choice(names)
                choose_rand_enum(q.knights[j].cause_of_death)

            print(q.n_)

    print('these integers are hard-coded in the test source code:')
    print_sequence_of_integers()

    def sequence_of_integers_from_somewhere():
        for x in [
            136519861221482844227583755426074287711102134274182720406254310407122869324862182390685480704600099678090395489112320354608503214182607262610507104236390,
            136519861218840611014476543051013447017969399067845404362039300167677532456907194303278576397412154799717262654059495913444002642178463241671021877724812,
            1812495852463926470557404969397984963655211493614900264923784741225328355890024083938550432665241448023468699363929607467214043886445298245246916756472069,
            974507856840989822151138784043013698051490805096840245674278542159472480811366324692401114447570553520061910902784081021358943124936198588054735126534971,
            1393501854649811457637850349466044744724791987432969716304082295943173228785101173283062646673271788345911242085491003930728028337944001659969773259810340,
            1393501854652484927060048262403605298903998826353482630122308601621678468793361125285798669287682418433530801876443522487849924558156776074789925016446723,
            974507856844419442879146593663303962985077574054564482551187246580286316905173966209488569010988658173156031008784407946915045690374335241530806914440876,
            1812495852468509706957497187362033899640539853218292209355922713887406323571764286544701473108499707173635403438847770696157832960115369300143179687836286,
            974507856839105298276162068272112053241061805539457423250221098097795315642075729557247737814541508192252240464380632539208422339362029591799921321496357,
            1812495852462402105894334743840535132956575737466779631784159799395243325556764502913069793316851236934587713336246112260891929469380182043366433418806342,
            136519861221494758817803215815851229568653001618173853319370461445166622145208470418165551363936953281085878730214049680611094023414165031638213798671898,
            974507856838719800330769707352382335545478213250485309092636009037690336196280060999658784103037301583450819469167848919298659165129999778731524633163916,
            1812495852464709417698027255582704519971372186420224419653416846142804876806303755351023991319511159697233635889220423798951844045121476709300502784631441,
            1393501854649796490355333304531892075012186706503603307038334936322044043777384164754844718049684524331061309251929211829677172904457358940357250241262928,
            1812495852460502649717021585725824766495916888397043928260446767556521220293374271236545387610337324605827844699517267092617177507412643871490756451822893,
            974507856840230665496740929661452254171550309319561378606869071405648621528892225099196640768677945064141701428500658702323185789715633132773324927192035,
            1393501854650959089099541386632811521469159944748310611691873693122705122955873739403929132632976010696476876872117745066665023675146120354350546811206161,
            136519861217697462587482478662456585278500603966002572537008852941669592805656400847850357198216494895792281043296054183693999834113129880333503635037163,
            1393501854653601258624733835166587682088070659292164290743568325770473922887708005159603324342096693392505913339314298066304793015299223554462200732265192,
            555513859032194888213288120422874346097718054323360069900033887762477850518362374394731179917355208231548290603415138115265854038383692771944888988181810,
        ]: yield x

    def get_dead_parrot_quests(raw_data_source: Sequence[int]) -> Iterator[str]:
        '''yields a sequence of json quests where the parrot is dead'''
        data = quest_struct()

        # fields can be assigned outside the loop for speed and convenience
        status = data.parrot.status

        for data.n_ in raw_data_source:
            if status == 'dead':
                yield data.json_

    raw_data_source = sequence_of_integers_from_somewhere()

    jstrs = []
    for jstr in get_dead_parrot_quests(raw_data_source):
        print(jstr)
        jstrs.append(jstr)

    assert len(jstrs) == 4
    assert jstrs[0] == '{"quest": "meaning", "knights": [{"name": "Sir Gareth", "cause_of_death": "mint"}, {"name": "Sir Bleoberis", "cause_of_death": "vorpal_bunny"}, {"name": "Sir Degore", "cause_of_death": "question"}], "holy": 0, "parrot": {"status": "dead", "plumage_rgb": [6, 25, 27]}}'
