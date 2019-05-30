from parser.prereqparser import *
import unittest


class PrereqParserTests(unittest.TestCase):
    def test101(self):
        string = 'Appropriate Math Placement Level; ' \
                 'or MATH 117 with a grade of C- or better; ' \
                 'or MATH 118 with a grade of C- or better; ' \
                 'or consent of instructor.'
        prereqs = parse_prepreqs(string)
        expected = [PrerequisiteDisjunction([
            'Appropriate Math Placement Level',
            CourseCompletion(CourseCode('MATH', 117),
                             CourseCompletionRequirement.C_MINUS_OR_BETTER),
            CourseCompletion(CourseCode('MATH', 118),
                             CourseCompletionRequirement.C_MINUS_OR_BETTER),
            ConsentOfInstructor()
        ])]
        self.assertEqual(prereqs, expected)

    def test108(self):
        string = 'MATH 118 (or equivalent) with a grade of C- or better, ' \
                 'significant experience in computer programming, ' \
                 'and consent of instructor.'
        prereqs = parse_prepreqs(string)
        expected = [
            CourseCompletion(CourseCode('MATH', 118),
                             CourseCompletionRequirement.C_MINUS_OR_BETTER),
            'significant experience in computer programming',
            ConsentOfInstructor()
        ]
        self.assertEqual(prereqs, expected)

    def test123(self):
        string = 'Basic computer literacy.'
        prereqs = parse_prepreqs(string)
        expected = ['Basic computer literacy']
        self.assertEqual(prereqs, expected)

    def test200(self):
        string = 'Consent of instructor.'
        prereqs = parse_prepreqs(string)
        expected = [ConsentOfInstructor()]
        self.assertEqual(prereqs, expected)

    def test202(self):
        # TODO: does the final 'or' mean 1) one of the three,
        #  or 2) the first two together or the last one?
        string = 'CPE/CSC 101 with a grade of C- or better; ' \
                 'MATH 141 or MATH 221 with a grade of C- or better; ' \
                 'or consent of instructor.'
        prereqs = parse_prepreqs(string)

    def test203(self):
        string = 'CPE/CSC 202 with a grade of C- or better or consent of instructor.'
        prereqs = parse_prepreqs(string)
        expected = [CourseCompletion(CourseCode('CPE/CSC', 202),
                                     CourseCompletionRequirement.C_MINUS_OR_BETTER_OR_CONSENT_OF_INSTRUCTOR)]
        self.assertEqual(prereqs, expected)

    def test209(self):
        string = 'CSC/CPE 101 or CSC/CPE 108 with a grade of C- or better, or consent of instructor.'
        prereqs = parse_prepreqs(string)
        expected = [PrerequisiteDisjunction([
            CourseCompletion(CourseCode('CSC/CPE', 101),
                             CourseCompletionRequirement.C_MINUS_OR_BETTER),
            CourseCompletion(CourseCode('CSC/CPE', 108),
                             CourseCompletionRequirement.C_MINUS_OR_BETTER),
            ConsentOfInstructor()
        ])]
        self.assertEqual(prereqs, expected)

    def test225(self):
        string = 'CSC/CPE 202.'
        prereqs = parse_prepreqs(string)
        expected = [CourseCompletion(CourseCode('CSC/CPE', 202), None)]
        self.assertEqual(prereqs, expected)

    def test231(self):
        string = 'MATH 142; PHYS 121 or PHYS 131 or PHYS 141.'
        prereqs = parse_prepreqs(string)
        expected = [
            CourseCompletion(CourseCode('MATH', 142), None),
            PrerequisiteDisjunction([
                CourseCompletion(CourseCode('PHYS', 121), None),
                CourseCompletion(CourseCode('PHYS', 131), None),
                CourseCompletion(CourseCode('PHYS', 141), None)
            ])
        ]
        self.assertEqual(prereqs, expected)

    def test290(self):
        # TODO: expected behavior?
        string = 'Open to undergraduate students and consent of instructor.'
        prereqs = parse_prepreqs(string)

    def test300(self):
        string = 'CSC/CPE 357 and junior standing.'
        prereqs = parse_prepreqs(string)
        expected = [
            CourseCompletion(CourseCode('CSC/CPE', 357), None),
            ClassStanding.JUNIOR
        ]
        self.assertEqual(prereqs, expected)

    def test302(self):
        string = 'Junior standing; ' \
                 'completion of GE Area A with grades of C- or better; ' \
                 'completion of GE Area B1 with a grade of C- or better in at least one of the courses;' \
                 ' and completion of GE Areas B2, B3, and B4.'
        prereqs = parse_prepreqs(string)
        expected = [
            ClassStanding.JUNIOR,
            GEAreaCompletion('A', CourseCompletionRequirement.C_MINUS_OR_BETTER),
            GEAreaCompletion('B1', CourseCompletionRequirement.C_MINUS_OR_BETTER),
            GEAreaCompletion('B2', None),
            GEAreaCompletion('B3', None),
            GEAreaCompletion('B4', None)
        ]
        self.assertEqual(prereqs, expected)


if __name__ == '__main__':
    unittest.main()
