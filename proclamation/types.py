#!/usr/bin/env python3 -i
# Copyright 2020 Collabora, Ltd.
#
# SPDX-License-Identifier: Apache-2.0

FRONT_MATTER_DELIMITER = "---"


class Reference:
    """A simple class storing the information about a reference."""

    def __init__(self, ref_service, item_type, number, service_params):
        """Construct a Reference from a parsed reference string."""
        super().__init__()
        self.ref_service = ref_service
        """Service associated with reference: something like GitHub or GitLab,
        perhaps."""

        self.item_type = item_type
        """Item type, like issue, mr, pr."""

        self.number = number
        """Reference number."""

        self.service_params = service_params
        """A list/tuple of any additional parameters associated with the
        service."""

    def as_tuple(self):
        """Return all contents as a tuple for use in sets and maps.

        Required of all classes that are to be used as a reference,
        for de-duplication.
        """
        return (self.ref_service, self.item_type, self.number,
                tuple(self.service_params))


class ReferenceFactoryBase:
    """The base class for a "reference factory".

    If you choose to customize this functionality, inherit from it.
    Otherwise, use it as-is.

    Reference factories may (this one does) use the Reference class from this
    module, but it's not required.
    Whatever suits you best is fine as long as it works with your template.

    References are things like ticket numbers, issue numbers, merge/pull
    request numbers, etc. This portion of the system is left fairly flexible
    since there are almost as many project administration structures as there
    are projects.
    """

    def __init__(self):
        """Construct factory."""
        self.extensions_to_drop = set(('md', 'rst', 'txt'))

    def split_on_dot_and_drop_ext(self, s):
        """Return the .-delimited portions of a name/ref, excluding a file extension.

        A utility function likely to be used in factories resembling this one.
        """
        elts = s.split(".")
        if elts[-1] in self.extensions_to_drop:
            elts.pop()
        return elts

    def parse(self, s):
        """Turn a string into a reference or None.

        May override or extend.
        """
        ref_tuple = self.split_on_dot_and_drop_ext(s)
        if ref_tuple[0] not in ("gh", "gl"):
            # warn?
            return None

        if len(ref_tuple) < 3:
            # warn?
            return None

        return Reference(ref_service=ref_tuple[0],
                         item_type=ref_tuple[1],
                         number=ref_tuple[-1],
                         service_params=ref_tuple[2:-1])


class Chunk:
    """A single CHANGES/NEWS entry, provided as text to insert into the templates.

    A chunk comes from a file or stream.

    The chunk filename is parsed to provide one reference. Optionally, an
    extremely small subset of "YAML front matter" can be used to list
    additional references in the chunk file contents. Delimit the front matter
    with --- both before and after, and place one reference per line (with or
    without leading -) between those delimiters.
    """

    def __init__(self, filename, reference, ref_factory=None, io=None):
        """Construct a chunk.

        Filename is used to open the file, if io is not provided.
        ref_factory parses "reference" strings (referring to PR/MR/issue) into
        a reference object.
        A default is provided.
        For testing or advanced stuff, pass a file handle or something like
        StringIO to io, in which case filename is not used.
        """
        super().__init__()
        self.filename = filename
        self.text = ""
        self.io = io
        self.ref = reference
        self.refs = []
        self.known_refs = set()
        self._insert_ref(reference)
        if ref_factory is None:
            ref_factory = ReferenceFactoryBase()
        self._ref_factory = ref_factory

    def _insert_ref(self, reference):
        ref_tuple = reference.as_tuple()
        if ref_tuple not in self.known_refs:
            self.refs.append(reference)
            self.known_refs.add(ref_tuple)

    def add_ref(self, s):
        """Parse a string as a reference and add it to this chunk."""
        ref_tuple = self._ref_factory.parse(s)
        if not ref_tuple:
            return
        self._insert_ref(ref_tuple)

    def _parse_front_matter(self, fp):
        while 1:
            line = fp.readline().strip()
            if line == FRONT_MATTER_DELIMITER:
                break
            if line.startswith("- "):
                line = line[2:]
            line = line.strip()
            self.add_ref(line)

    def _parse_io(self, fp):
        first_line = fp.readline()
        if first_line.strip() == FRONT_MATTER_DELIMITER:
            self._parse_front_matter(fp)
        while 1:
            line = fp.readline()
            if not line:
                break
            self.text += line

    def parse_file(self):
        """Open the file and parse content, and front matter if any.

        If io was provided at construction time, that is parsed instead.
        """
        if self.io is not None:
            self._parse_io(self.io)
            return
        with open(str(self.filename), 'r', encoding='utf-8') as fp:
            self._parse_io(fp)


class Section:
    """A section is a component/aspect of a project.

    Changes for a Section are (potentially) separated out in the news file.
    For example, sections might include "Drivers", "UI", etc.
    """

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.chunks = []
        self.files = []

    def populate_from_directory(self, directory, ref_factory):
        """Iterate through a directory, trying to parse each filename as a reference.

        Files that parse properly are assumed to be chunks,
        and a Chunk object is instantiated for them.
        """
        for chunk_name in directory.iterdir():
            chunk_ref = ref_factory.parse(chunk_name.name)
            if not chunk_ref:
                # Actually not a chunk, skipping
                print("Not actually a chunk", chunk_name)
                continue
            self.chunks.append(Chunk(chunk_name, chunk_ref, ref_factory))

        for chunk in self.chunks:
            chunk.parse_file()

    @property
    def chunk_filenames(self):
        """Return a generator of filenames for all chunks added."""
        return (chunk.filename for chunk in self.chunks)
