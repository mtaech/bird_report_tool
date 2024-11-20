# 观鸟记录对象

class BirdRecord:
    def __init__(self, id=None, url=None, serial_id=None, start_time=None, user=None,
                 location=None, number=None,status=None, is_done=None,is_red=None):
        self.id = id
        self.url = url
        self.serial_id = serial_id
        self.start_time = start_time
        self.user = user
        self.location = location
        self.number = number
        self.status = status
        self.is_done = is_done
        self.is_red = is_red


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
    def __init__(self, id=None, bird_no=None, bird_name=None, bird_latin_name=None, bird_eng_name=None, mu=None,
                 ke=None, num=None, record_no=None,has_pic = None,is_red = None):
        self.id = id
        self.bird_no = bird_no
        self.bird_name = bird_name
        self.bird_latin_name = bird_latin_name
        self.bird_eng_name = bird_eng_name
        self.mu = mu
        self.ke = ke
        self.num = num
        self.record_no = record_no
        self.has_pic = has_pic
        self.is_red = is_red

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
