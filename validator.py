import os
from werkzeug.utils import secure_filename


class Validator(object):

    def __init__(self, request, uploaded_file):
        self.request = request
        self.uploaded_file = uploaded_file
        self.sanitized_filename = secure_filename(uploaded_file.filename)
        self.flash_message = ""
        self.is_validation_pass = True

        self.do_validate()

    def do_validate(self):
        check_functions_list = [self.is_post_name_correct,
                                self.is_not_empty_filename,
                                self.is_file_type_allowed]
        for check in check_functions_list:
            if self.is_validation_pass:
                check()
            else:
                break
        if self.is_validation_pass:
            self.save_uploaded_file()

    def get_results(self):
        return self.is_validation_pass, self.flash_message

    def is_post_name_correct(self):
        if 'file' not in self.request.files:
            self.is_validation_pass = False
            self.flash_message = "No file part in post"

    def is_not_empty_filename(self):
        if self.uploaded_file.filename == '':
            self.is_validation_pass = False
            self.flash_message = "No selected file"

    def is_file_type_allowed(self):
        if not self.uploaded_file or not self.is_tar():
            self.is_validation_pass = False
            self.flash_message = "No tar.gz file"

    def is_tar(self):
        return True

    def save_uploaded_file(self):
        self.uploaded_file.save(os.path.join('/tmp/', self.sanitized_filename))
