from datadashr.config import *


class Pipeline:
    def __init__(self, **kwargs):
        """
        Initializes a pipeline with the given steps and context.
        :param kwargs:
        """
        self.steps = []
        self.context = kwargs

    def add_step(self, step):
        """
        Adds a step to the pipeline.
        :param step:
        :return:
        """
        try:
            self.steps.append(step)
        except Exception as e:
            logger.error(f"Error adding step: {e}")

    def run(self):
        """
        Runs the pipeline.
        :return:
        """
        try:
            for step in self.steps:
                if self.context.get('verbose'):
                    logger.info(f"Running step: {step.name}")
                step.execute(self.context)
                # Log del contesto dopo ogni step per debug
                if self.context.get('verbose'):
                    logger.info(f"Context after {step.name}: {self.context}")
                if self.context.get('skip_sandbox'):
                    break
            return self.context
        except Exception as e:
            logger.error(f"Error running pipeline: {e}")
            return None
