class Record(object):

    def __init__(self, line):
        """
        line: main record from raw_rozpocet
        """
        self.gid = line[0]
        self.modul = None
        self.date = line[1]
        self.kap = line[10]
        self.odpa = line[2]
        self.pol = line[3]
        self.orj = line[4]
        self.org = line[5]
        self.dati = line[6]
        self.dal = line[7]
        self.ic = None
        self.partner = None
        self.pid = None
        self.evk = None
        self.evkt = None
        self.desc = None
        self.comment = line[8]

        self._parse_long_comment(line[9])

    @property
    def castka(self):
        return self.dal-self.dati

    def _parse_long_comment(self, text):
        arr = text.split('*')
        while len(arr) > 0:
            item = arr.pop()
            if not item:
                continue    # blank, skip can be empty string
            elif item.startswith('DUD-'):
                continue    # record divider
            elif item.startswith('IC-'):
                self.ic = item[3:][:-1].rstrip(';').rstrip(' ')
            elif item.startswith('DICT-'):
                self.partner = item.strip()[5:][:-1]
            elif item.startswith('PID-'):
                self.pid = item.strip()[4:][:-1]
            elif item.startswith('EVK-'):
                self.evk = item.strip()[4:][:-1]
                self.modul = self.evk[0:3]
            elif item.startswith('EVKT-'):
                self.evkt = item.strip()[5:].rstrip(';')
            elif item.strip():
                self.desc = item.strip()

    def __str__(self):
        return """<gid: {gid}, date: {date}, pol: {pol}, partner: {partner}>""".format(
            gid=self.gid, date=self.date, pol=self.pol, partner=self.partner)
