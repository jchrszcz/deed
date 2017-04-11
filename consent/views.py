from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
	form_model = models.Player
	form_fields = ['age', 'read', 'want']

	def before_next_page(self):
		self.participant.vars['age'] = self.player.age
		self.participant.vars['read'] = self.player.read
		self.participant.vars['want'] = self.player.want

class Exit(Page):
	def is_displayed(self):
		if self.participant.vars['age'] == "No":
			return True
		if self.participant.vars['read'] == 'No':
			return True
		if self.participant.vars['want'] == 'No':
			return True

page_sequence = [
	MyPage,
	Exit,
]
