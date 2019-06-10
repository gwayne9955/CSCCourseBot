from collections import Counter


keywords = {
    'Tutoring and Clubs': ['tutor', 'club', 'clubs'],
    'CSSE Department Info': ['department', 'CSSE', 'advising', 'advisor'],
    'STAT Department Info': ['statistics', 'stats', 'STAT', 'department',
                             'advising', 'advisor'],
    'CSSE Instructors and Research Areas': ['research', 'professor', 'instructor', 'faculty',
                                            'grant', 'funding', 'CSC', 'CSSE', 'computer science'],
    'STAT Instructors and Research Areas': ['research', 'professor', 'instructor',
                                            'faculty', 'statistics', 'STAT'],
    'CSSE Majors, Minors, Concentrations, Curricula': ['CSSE', 'CSC', 'education',
                                                       'elective', 'computer science', 'software engineering',
                                                       'units', 'major', 'minor', 'program', 'concentration',
                                                       'flowchart', 'gpa'],
    'STAT Majors, Minors, Concentrations, Curricula': ['STAT', 'statistics', 'stats', 'electives'
                                                       'units', 'ge area', 'gpa', 'concentration'],
}


def best_team_estimate(query):
    query = query.lower()
    counter = Counter()
    for group, kws in keywords.items():
        for kw in kws:
            if kw.lower() in query:
                counter[group] += 1
    if len(counter) == 0:
        return None
    return counter.most_common(1)[0][0]
