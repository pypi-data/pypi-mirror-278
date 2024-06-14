import re
import os

import petlja_api
from .task import Task
from . import logger

class Competition:
    def __init__(self, comp_dir, name=None, description=None):
        self.comp_dir = comp_dir
        self.id = Task.extract_id_from_dir(comp_dir)
        self.name = name
        self.description = description
        self.alias = re.sub(r"[^a-zA-Z0-9\-]", "", self.id).lower()

    @staticmethod
    def is_comp_dir(dir):
        return any(Task.is_task_dir(d) for d in os.listdir(dir))

    def publish(self):
        sess = petlja_api.login()

        update = False
        name = self.name if self.name else self.id
        try:
            comp_id = petlja_api.create_competition(sess, name, self.alias, self.description)
        except ValueError:
            update = True
            logger.info("Competition already created, updating problems")
            comp_id = petlja_api.get_competition_id(sess, self.alias)

        problem_names = []
        for problem_dir in os.listdir(self.comp_dir):
            if not Task.is_task_dir(problem_dir):
                continue
            prob = Task(problem_dir)
            prob_id = prob.publish(sess)
            petlja_api.add_problem(sess, comp_id, prob_id)
            problem_names.append(prob.title())
        
        if update:
            logger.info(f'Competition "{self.id}" updated')
        else:
            logger.info(f'Created competiton "{self.id}" with following problems: {problem_names}')
        