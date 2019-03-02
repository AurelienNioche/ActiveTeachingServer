from django.db import models

# Create your models here.


class Data(models.Model):

    user_id = models.IntegerField()
    t = models.IntegerField()
    question = models.IntegerField()
    reply = models.IntegerField()

    class Meta:

        db_table = 'task_data'
        app_label = 'task'


class User(models.Model):

    username = models.TextField(unique=True)
    gender = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    mother_tongue = models.TextField(blank=True, null=True)
    other_language = models.TextField(blank=True, null=True)
    registration_time = models.DateTimeField()

    class Meta:
        db_table = 'task_user'
        app_label = 'task'


class Kanjilist(models.Model):

    kanji = models.CharField(db_column='Kanji', max_length=255, blank=True, null=True)  # Field name made lowercase.
    meaning = models.CharField(max_length=255, blank=True, null=True)
    strokes = models.CharField(db_column='Strokes', max_length=255, blank=True, null=True)  # Field name made lowercase.
    grade = models.CharField(db_column='Grade', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kanji_classification = models.CharField(db_column='Kanji Classification', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    jlpt_test = models.CharField(db_column='JLPT-test', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    name_of_radical = models.CharField(db_column='Name of Radical', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    radical_freq_field = models.CharField(db_column='Radical Freq.', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    reading_within_joyo = models.CharField(db_column='Reading within Joyo', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reading_beyond_joyo = models.CharField(db_column='Reading beyond Joyo', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    of_on = models.CharField(db_column='of On', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    on_within_joyo = models.CharField(db_column='On within Joyo', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    kanji_id_in_nelson = models.CharField(db_column='Kanji ID in Nelson', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    of_meanings_of_on = models.CharField(db_column='of Meanings of On', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    translation_of_on = models.CharField(db_column='Translation of On', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    of_kun_within_joyo_with_inflections = models.CharField(db_column='of Kun within Joyo with inflections', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    of_kun_within_joyo_without_inflections = models.CharField(db_column='of Kun within Joyo without inflections', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    kun_within_joyo = models.CharField(db_column='Kun within Joyo', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    of_meanings_of_kun = models.CharField(db_column='of Meanings of Kun', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    translation_of_kun = models.CharField(db_column='Translation of Kun', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    year_of_inclusion = models.CharField(db_column='Year of Inclusion', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    kanji_frequency_with_proper_nouns = models.CharField(db_column='Kanji Frequency with Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acc_freq_on_with_proper_nouns = models.CharField(db_column='Acc. Freq. On with Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acc_freq_kun_with_proper_nouns = models.CharField(db_column='Acc. Freq. Kun with Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    on_ratio_with_proper_nouns = models.CharField(db_column='On Ratio with Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acc_freq_on_beyond_joyo_with_proper_nouns = models.CharField(db_column='Acc. Freq. On beyond Joyo with Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acc_freq_kun_beyond_joyo_with_proper_nouns = models.CharField(db_column='Acc. Freq. Kun beyond Joyo with Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acc_on_ratio_beyond_joyo_with_proper_nouns = models.CharField(db_column='Acc. On Ratio beyond Joyo with Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    kanji_frequency_without_proper_nouns = models.CharField(db_column='Kanji Frequency without Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acc_freq_on_without_proper_nouns = models.CharField(db_column='Acc. Freq. On without Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acc_freq_kun_without_proper_nouns = models.CharField(db_column='Acc. Freq. Kun without Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    on_ratio_without_proper_nouns = models.CharField(db_column='On Ratio without Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acc_freq_on_beyond_joyo_without_proper_nouns = models.CharField(db_column='Acc. Freq. On beyond Joyo without Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acc_freq_kun_beyond_joyo_without_proper_nouns = models.CharField(db_column='Acc. Freq. Kun beyond Joyo without Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    on_ratio_beyond_joyo_without_proper_nouns = models.CharField(db_column='On Ratio beyond Joyo without Proper Nouns', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    left_kanji_prod_field = models.CharField(db_column='Left Kanji Prod.', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    right_kanji_prod_field = models.CharField(db_column='Right Kanji Prod.', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    acc_freq_left_prod_field = models.CharField(db_column='Acc. Freq. Left Prod.', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    acc_freq_right_prod_field = models.CharField(db_column='Acc. Freq. Right Prod.', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    symmetry = models.CharField(db_column='Symmetry', max_length=255, blank=True, null=True)  # Field name made lowercase.
    left_entropy = models.CharField(db_column='Left Entropy', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    right_entropy = models.CharField(db_column='Right Entropy', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    left1sound = models.CharField(db_column='Left1sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    left1freq = models.CharField(db_column='Left1freq', max_length=255, blank=True, null=True)  # Field name made lowercase.
    left2sound = models.CharField(db_column='Left2sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    left2freq = models.CharField(db_column='Left2freq', max_length=255, blank=True, null=True)  # Field name made lowercase.
    left3sound = models.CharField(db_column='Left3sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    left3freq = models.CharField(db_column='Left3freq', max_length=255, blank=True, null=True)  # Field name made lowercase.
    left4sound = models.CharField(db_column='Left4sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    left4freq = models.CharField(db_column='Left4freq', max_length=255, blank=True, null=True)  # Field name made lowercase.
    left5sound = models.CharField(db_column='Left5sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    left5freq = models.CharField(db_column='Left5freq', max_length=255, blank=True, null=True)  # Field name made lowercase.
    left6sound = models.CharField(db_column='Left6sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    left6freq = models.CharField(db_column='Left6freq', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right1sound = models.CharField(db_column='Right1sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right1freq = models.CharField(db_column='Right1freq', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right2sound = models.CharField(db_column='Right2sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right2freq = models.CharField(db_column='Right2freq', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right3sound = models.CharField(db_column='Right3sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right3freq = models.CharField(db_column='Right3freq', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right4sound = models.CharField(db_column='Right4sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right4freq = models.CharField(db_column='Right4freq', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right5sound = models.CharField(db_column='Right5sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right5freq = models.CharField(db_column='Right5freq', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right6sound = models.CharField(db_column='Right6sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right6freq = models.CharField(db_column='Right6freq', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right7sound = models.CharField(db_column='Right7sound', max_length=255, blank=True, null=True)  # Field name made lowercase.
    right7freq = models.CharField(db_column='Right7freq', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'kanjilist'
        app_label = 'task'

