# -*- coding: utf-8 -*-

class SubjectModel:
    def __init__(self):
        self.subjects = []
    
    def add_subject(self, subject_name):
        subject_name = subject_name.strip()
        if not subject_name:
            return False, "学科名称不能为空"
        for s in self.subjects:
            if s == subject_name:
                return False, "学科已存在"
        self.subjects.append(subject_name)
        return True, "添加成功"
    
    def delete_subject(self, subject_name):
        subject_name = subject_name.strip()
        if subject_name in self.subjects:
            self.subjects.remove(subject_name)
            return True, "删除成功"
        return False, "未找到该学科"
    
    def get_all_subjects(self):
        return self.subjects
    
    def is_empty(self):
        return len(self.subjects) == 0