# -*- coding: utf-8 -*-

class StudentModel:
    def __init__(self):
        self.students = []
    
    def add_student(self, student):
        student = student.copy()
        student['id'] = str(student['id'])
        for s in self.students:
            if s['id'] == student['id']:
                return False, "学号已存在"
        self.students.append(student)
        return True, "添加成功"
    
    def delete_student(self, student_id):
        student_id_str = str(student_id)
        found = False
        new_students = []
        for s in self.students:
            if str(s['id']) == student_id_str:
                found = True
            else:
                new_students.append(s)
        self.students = new_students
        if found:
            return True, "删除成功"
        return False, "未找到该学生"
    
    def update_student(self, student_id, new_data):
        student_id_str = str(student_id)
        for i, s in enumerate(self.students):
            if str(s['id']) == student_id_str:
                if str(new_data['id']) != student_id_str:
                    for other in self.students:
                        if str(other['id']) == str(new_data['id']) and other != s:
                            return False, "新学号已存在"
                self.students[i] = new_data
                return True, "更新成功"
        return False, "未找到该学生"
    
    def search_students(self, keyword):
        results = []
        for s in self.students:
            if keyword in s['id'] or keyword in s['name']:
                results.append(s)
        return results
    
    def get_all_students(self):
        return self.students
    
    def get_class_distribution(self):
        distribution = {}
        for s in self.students:
            class_name = s.get('class', '未分类')
            distribution[class_name] = distribution.get(class_name, 0) + 1
        return distribution
    
    def get_subject_averages(self, subjects):
        averages = {}
        for subject in subjects:
            total = 0.0
            count = 0
            for s in self.students:
                score = s.get('scores', {}).get(subject, '0')
                try:
                    total += float(score)
                    count += 1
                except ValueError:
                    pass
            if count > 0:
                averages[subject] = round(total / count, 2)
            else:
                averages[subject] = 0.0
        return averages
    
    def get_total_count(self):
        return len(self.students)