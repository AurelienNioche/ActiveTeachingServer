import numpy as np

class Selection:
    def __init__(self, model):
        self.model = model

        # Retrieve elements from the database
        try:
            values, meaning = \
                np.array(

                    self.model.objects.values_list('value', 'meaning').order_by('index')
                ).T
        except Exception as e:
            raise RuntimeError("Cannot load the database content:" + str(e))

        self.values = values
        self.meaning = meaning

        self.unique_meaning, idx, inverse = np.unique(self.meaning,
                                                 return_index=True,
                                                 return_inverse=True)

        self.id_value = np.arange(len(self.values))
        self.id_meaning = self.id_value[idx][inverse]

    def total_number_of_items(self):
        return self.model.objects.count()

    def get_string_representation(self, id_question, id_possible_replies):
        question = self.values[id_question]
        possible_replies = [self.meaning[i] for i in id_possible_replies]
        return question, possible_replies

    def get_id(self):
        return self.id_value, self.id_meaning
