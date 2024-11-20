# 观鸟记录对象
class BirdRecord:
    def __init__(self):
        self.id = None
        self.url = None
        self.serial_id = None
        self.start_time = None
        self.end_time = None
        self.user = None
        self.location = None
        self.number = None
        self.status = None
        self.is_done = None

    def set_value(self, field, content):
        if field == "serial_id":
            self.serial_id = content
        elif field == "start_time":
            self.start_time = content
        elif field == "username":
            self.user = content
        elif field == "point_name":
            self.location = content
        elif field == "taxoncount":
            self.number = content
        elif field == "state":
            self.status = content

#观鸟记录明细对象
class RecordDetail:
    def __init__(self):
        self.id = None
        self.bird_no = None
        self.bird_name = None
        self.bird_latin_name = None
        self.bird_eng_name = None
        self.mu = None
        self.ke = None
        self.num = None
        self.record_no = None

    def set_value(self, field, content):
        if field == "taxon_id":
            self.bird_no = content
        elif field == "taxon_name":
            self.bird_name = content
        elif field == "latinname":
            self.bird_latin_name = content
        elif field == "englishname":
            self.bird_eng_name = content
        elif field == "taxonordername":
            self.mu = content
        elif field == "taxonfamilyname":
            self.ke = content
        elif field == "taxon_count":
            self.num = content
