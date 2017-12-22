class Validator(object):

    def __init__(self, input_file):
        self.input_file = input_file

    def post_got_files(self, request):
        return False if 'file' not in request.files else True
