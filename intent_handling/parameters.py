

def safe_get(d, key):
    return d[key] if key in d else None


class Parameters:
    def __init__(self, d):
        self.class_name = safe_get(d, 'CLASS_NAME')
        self.quarter = safe_get(d, 'QUARTER')
        if self.quarter is not None:
            self.quarter = ''.join(c for c in self.quarter if c not in '!?.,')
        self.class_qualification = safe_get(d, 'CLASS_QUALIFICATION')
        self.department_abbreviation = safe_get(d, 'DEPARTMENT_ABBREVIATION')
        self.subject_matter = safe_get(d, 'SUBJECT_MATTER')
        self.ge_area = safe_get(d, 'GE_AREA')
        self.course_level = safe_get(d, 'COURSE_LEVEL')
