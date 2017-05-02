from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class PaymentInfo(Page):
	form_model = models.Player
	form_fields = ['turkid']

	def vars_for_template(self):
		return {'total':self.participant.payoff_plus_participation_fee()}

class End(Page):
	pass

page_sequence = [PaymentInfo, End]
