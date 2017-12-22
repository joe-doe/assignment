class Validator(object):

    def __init__(self, input_file):
        self.input_file = input_file
        self.flash_message = "OK"

    def is_post_name_correct(self, request):
        return_value = True
        if 'file' not in request.files:
            return_value = False
            self.flash_message = "No file part in post"
        return return_value

    def is_empty_filename(self, uploaded_file):
        return_value = False
        if uploaded_file.filename == '':
            return_value = True
            self.flash_message = "No selected file"
        return return_value

    def is_file_type_allowed(self, uploaded_file):
        return_value = True
        if not uploaded_file or not self.is_tar(uploaded_file):
            return_value = False
            self.flash_message = "No tar.gz file"
        return return_value

    def is_tar(self, uploaded_file):
        return True
