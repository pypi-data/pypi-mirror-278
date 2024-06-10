
# bffl
**Bit Fields For Lumberjacks**

![lumberjack](images/bffl800.png)

`bffl` is a high-performance bit field protocol framework for working with packed binary data. It's ideal for scenarios requiring precise control of bit arrangements, such as verilog interfaces and arbitrary bitfield manipulations. Your protocol is expressed concisely using compositions of ints, structs, arrays, and user-defined types.

## Comparison to [ctypes](https://docs.python.org/3/library/ctypes.html)

| Tool   | Model         | Primary Purpose                                       | Implementation  |
|--------|---------------|-------------------------------------------------------|-----------------|
| ctypes | C/C++ types   | Interface with C/C++ code, model C/C++ datatypes      | Python, C++     |
| bffl   | Bit fields    | Model arbitrary bit-aligned datatypes and interfaces  | Python          |

* Use `ctypes` for interfacing with C/C++.
* Use `bffl` for full control over bit-aligned binary protocols.
* Use both for combined functionality.

## Comparison to C++ Bitfields

C++ bitfields optimize for performance and byte alignment, often disregarding explicit bit control. `bffl` offers full control over bit allocation, making it ideal for protocol implementations and verilog.

```plaintext
// In C++, struct size is implicitly padded:
struct Example {
    uint8_t a : 5;
    uint8_t b : 13;
};  // Size may not be 18 bits due to padding

// In bffl:
class Example(metaclass=metastruct):
    a: uint(5)
    b: uint(13)
```

In `bffl`, structs are exactly the sum of their members' sizes, with no implicit padding. An array of 7 7-bit integers occupies precisely 49 bits (`uint(7)[7].size_ == 49`).

## Ease of Use

```python
raw_data_source = sequence_of_integers_from_somewhere()

class parrot_struct(metaclass=metastruct):
    status: uint(2, {'dead': 0, 'pining': 1, 'resting': 2})
    plumage_rgb: uint(5)[3]

death_enum = uint(3, {
    'vorpal_bunny': 0,
    'liverectomy': 1,
    'ni': 2,
    'question': 3,
    'mint': 4,
    'not_dead_yet': 5,
})

class knight_struct(metaclass=metastruct):
    name: utf8(20)
    cause_of_death: death_enum

class quest_struct(metaclass=metastruct):
    quest: uint(3, {'grail': 0, 'shrubbery': 1, 'meaning': 2, 'larch': 3, 'gourd': 4})
    knights: knight_struct[3]
    holy: uint(1)
    parrot: parrot_struct

def get_dead_parrot_quests(raw_data_source: Sequence[int]) -> Iterator[str]:
    data = quest_struct()
    status = data.parrot.status

    for data.n_ in raw_data_source:
        if status == 'dead':
            yield data.json_

for jstr in get_dead_parrot_quests(raw_data_source):
    print(jstr)
```

## Interoperability

Fields have read/write properties exposing data:
| Attribute | Description                              |
|-----------|------------------------------------------|
| `n_`      | Raw bits as an int (unbounded size)      |
| `v_`      | Data value as int, float, str, list, dict|
| `json_`   | Data value as a JSON string              |

## Performance

Performance is achieved by symbolic processing during interface allocation, reducing runtime overhead. A bound field computation typically involves a `shift-and` operation.

```python
class MyRegister(metaclass=metastruct):
    rtype: uint(2, enum_={'grail': 0, 'shrubbery': 1, 'meaning': 2, 'larch': 3})
    stuff: uint(3)
    junk: uint(1)

class MyProtocol(metaclass=metastruct):
    header: uint(5)
    a: MyRegister
    b: MyRegister
    c: MyRegister

def look_for_fives(datastream: Sequence[int]):
    buffer = MyProtocol()
    bstuff = buffer.b.stuff

    for n in datastream:
        buffer.n_ = n
        if bstuff == 5:
            handle_5()
```

## Trailing Underscore Convention

Non-field attributes use a trailing underscore, allowing full use of the field namespace.

## System Verilog Support

`bffl` uses Python semantics for indexing and slicing but includes `svreg` for System Verilog slice semantics.

```python
r = svreg(28)(0xabadbee)
r2 = r[15:4]
assert r2 == 0xbad
r2.v_ = 0xead
r[3:0] = 0xd
assert r == 0xdeadbee
```

## Related Projects

Here is a comparison grid of various bitfield-related libraries with verified licenses:

| **Library** | **Description** | **Primary Purpose** |
|-------------|-----------------|---------------------|
| **[bitvector](https://github.com/JnyJny/bitvector)** | Bit vector implementation with BitField descriptor for sub-byte bit addressing | Address and manipulate bits in integer words |
| **[bfield](https://pypi.org/project/bfield)** | Convenient bit fields for int subclasses | Define and manipulate bitfields |
| **[ctypes-bitfield](https://pypi.org/project/ctypes-bitfield/)** | Bitfields with ctypes integration | Interface with C/C++ bitfields |
| **[sparsebitfield](https://pypi.org/project/sparsebitfield/)** | Manage sparse sets of large integers | Efficiently manage large sets of bits | JavaScript |
| **[bitfield](https://github.com/stestagg/bitfield)** | Sparse sets of large integers optimized for sequential integers | Handle large, sparse integer sets |
| **[named_bitfield](https://github.com/not-napoleon/named_bitfield)** | Define named bitfields for easier access and manipulation | Named bitfields |
| **[bitstring](https://github.com/scott-griffiths/bitstring)** | Supports slicing and manipulating bit strings | Handle and manipulate bit strings |

