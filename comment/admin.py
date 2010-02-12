from django.contrib import admin
from models import * 

admin.site.register(SecretComment)
admin.site.register(DiscussionComment)
admin.site.register(Proposal)
admin.site.register(ProposalComment)
admin.site.register(ProposalEndorsement)

