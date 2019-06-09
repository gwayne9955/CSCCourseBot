import os
import sys
cur_path = os.getcwd()
sys.path.insert(0, '/'.join(cur_path.split('/')[:-1]))

from storage.DBProxy import DBProxy


def main():
    proxy = DBProxy()
    sql = "INSERT INTO questions (question, answer, groupId) " \
          "VALUES (%s, %s, %s)"
    groupId = "H1"

    with open("questions.txt", 'r') as f:
        questionstr = f.read()

    questions = questionstr.split('\n')
    for question in questions:
        question_list = question.split('|')
        if len(question_list) == 3:
            q = question_list[1].strip()
            answer = question_list[2].strip()
            data = (q, answer, groupId)
            #print("Question: {}".format(q))
            #print("Answer: {}".format(answer))
            #print("Group ID: {}".format(groupId))
            proxy.store(sql, data)

    proxy.disconnect()


if __name__ == "__main__":
    main()
