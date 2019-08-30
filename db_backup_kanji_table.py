import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "ActiveTeachingServer.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from teaching_material.db_operation import backup_kanji_table

backup_kanji_table()

# # import googletrans
# # from translate import Translator
# #
# # def _ask_user_for_replacement(word, proposition=None):
# #
# #     while True:
# #         if proposition:
# #             new_word = proposition.capitalize()
# #         else:
# #             new_word = input("Which word I should use in replacement?")
# #             print("Thanks!")
# #         reply = input(f"Do you confirm the replacement of '{word}' "
# #                       f"by '{new_word}' (y/n)?")
# #         if reply in ('y', 'yes', 'ok'):
# #             print("Replacement registered!")
# #             return new_word
# #         else:
# #             proposition = None
# #
# #
# # from teaching_material.models import Kanji
# #
# #
# # entries = Kanji.objects.all().order_by('index')
# #
# # # tr = googletrans.Translator()
# #
# # translator = Translator(to_lang="de")
# #
# # for e in entries:
# #     m = e.meaning
# #     # if m in ('Kiyo', 'Kaoru'):
# #     #     m2 = translator.translate(m)
# #     #     print(m2)
# #     #     m = _ask_user_for_replacement(m)
# #
# #     # for s in ("A ", "To ", "The "):
# #     #     if s in m:
# #     #         m = _ask_user_for_replacement(m, proposition=m.replace(s, ""))
# #
# #     m2 = translator.translate(m)
# #     m2 = m2.capitalize()
# #     if m == m2:
# #         while True:
# #             reply = input(f"Do want to replace '{m}' (y/n)?")
# #             if reply in ('y', 'yes', 'ok'):
# #                 m = _ask_user_for_replacement(m)
# #                 break
# #             elif reply in ('n', 'no'):
# #                 print("No replacement")
# #                 break
# #
# #     e.meaning = m
# #     e.save()
# from user_data.models import Question
# import pickle
# from teaching_material.selection import id_meaning
#
# # old_meaning = list(pickle.load(open('old_meaning.p', 'rb')))
#
#
# entries = Question.objects.all()
#
#
# for e in entries:
#
#     e.reply = id_meaning[e.reply]
#     new_replies = []
#     for m_idx in e.possible_replies:
#         new_replies.append(id_meaning[m_idx])
#     e.possible_replies = new_replies
#     e.save()

