PROFILE_ID = 'profile-cpskin.menu:default'


def upgrade_1000_to_1001(context):
    context.runImportStepFromProfile(PROFILE_ID, 'viewlets')
